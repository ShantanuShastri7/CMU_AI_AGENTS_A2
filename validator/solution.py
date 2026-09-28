"""The student validator implementation for Part 2.

Implements the two proposed changes from Part 1:
1. Deterministic figure verification for execution_failure:
   - If no valid figure exists or the image cannot be decoded, immediately report execution_failure.
   - If a valid figure exists and decodes properly, rule out non-generation execution failure.
   - Terminal short-circuiting: when execution_failure occurs, avoid querying downstream visual/chart checks.
2. Structured semantic parsing / robust prompt polarity:
   - Ensures execution checks are grounded in factual failure rather than affirmative prefix parsing.
   - Preserves visual and readability evaluation for runs with valid figures.
"""

from __future__ import annotations

import base64
import io
import warnings
from pathlib import Path
from typing import Any

from openai import BadRequestError
from PIL import Image, UnidentifiedImageError

from validator.model import complete, detokenize, tokenize
from validator.prediction import Error, ErrorFamily
from validator.runner import Run

CONTEXT_FRACTION = 0.5
MAX_OUTPUT_TOKENS = 250
OMISSION = "\n[... omitted to fit model context ...]\n"
COMPACTION_NOTE = "\nSome evidence may be omitted. Do not treat omissions as agent errors.\n"
IMAGE_DOWNSCALE_FACTOR = 0.7
MIN_IMAGE_LONG_SIDE = 64


def _excerpt(text: str, tokens: list[int], limit: int) -> str:
    """Retain the beginning and end, including the run's final actions."""
    if len(tokens) <= limit:
        return text
    head = limit // 2
    tail = limit - head
    return (
        (detokenize(tokens[:head]) if head else "")
        + OMISSION
        + (detokenize(tokens[-tail:]) if tail else "")
    )


def _compact(trajectory: str, inputs: str, fixed_prompt: str) -> tuple[str, str]:
    trajectory_info = tokenize(trajectory)
    context = trajectory_info.get("max_model_len")
    if type(context) is not int or context <= 0:
        raise RuntimeError("Validator server did not report a valid max_model_len")
    trajectory_tokens = trajectory_info["tokens"]
    input_tokens = tokenize(inputs)["tokens"]
    fixed_tokens = tokenize(fixed_prompt + COMPACTION_NOTE + OMISSION * 2)["tokens"]
    budget = int(context * CONTEXT_FRACTION) - len(fixed_tokens) - MAX_OUTPUT_TOKENS
    if budget < 0:
        raise RuntimeError("Task instructions exceed the baseline's context budget")
    total = len(trajectory_tokens) + len(input_tokens)
    trajectory_budget = budget * len(trajectory_tokens) // max(total, 1)
    return (
        _excerpt(trajectory, trajectory_tokens, trajectory_budget),
        _excerpt(inputs, input_tokens, budget - trajectory_budget),
    )


def _downscale(data: bytes) -> bytes | None:
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            width, height = image.size
            mode = image.mode
    except (UnidentifiedImageError, OSError, ValueError):
        return None
    longest = max(width, height)
    if longest <= MIN_IMAGE_LONG_SIDE:
        return None
    scale = max(MIN_IMAGE_LONG_SIDE / longest, IMAGE_DOWNSCALE_FACTOR)
    new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
    if new_size == (width, height):
        return None
    with Image.open(io.BytesIO(data)) as image:
        if mode not in ("RGB", "RGBA", "L"):
            image = image.convert("RGB")
        resized = image.resize(new_size, Image.LANCZOS)
    buffer = io.BytesIO()
    resized.save(buffer, format="PNG")
    return buffer.getvalue()


def _context_overflow(error: BadRequestError) -> bool:
    message = str(error).lower()
    return any(
        phrase in message
        for phrase in (
            "context_length_exceeded",
            "maximum context length",
            "maximum model length",
            "maximum input length",
        )
    )


def _ask(run: Run, family: ErrorFamily, question: str) -> list[Error]:
    inputs = "\n".join(
        f"{name}:\n{path.read_text(errors='replace')}" for name, path in run.inputs.items()
    )
    trajectory = str(run.messages)
    image_bytes = run.figure.read_bytes() if run.figure else None

    def make_prompt(shown_trajectory: str, shown_inputs: str) -> str:
        return f"""{question}
Answer YES or NO, then explain briefly.

Task: {run.instructions}
Trajectory: {shown_trajectory}
Input files: {shown_inputs or '(none)'}
"""

    def ask(prompt: str, image: bytes | None) -> dict:
        content = [{"type": "text", "text": prompt}]
        if image is not None:
            encoded = base64.b64encode(image).decode()
            content.append(
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
            )
        return complete([{"role": "user", "content": content}], max_tokens=MAX_OUTPUT_TOKENS)

    try:
        response = ask(make_prompt(trajectory, inputs), image_bytes)
    except BadRequestError as error:
        if not _context_overflow(error):
            raise
        warnings.warn(
            f"Run {run.run_id} ({family.value}): model context exceeded; "
            f"retrying with text capped at {CONTEXT_FRACTION:.0%} of server context.",
            stacklevel=2,
        )
        shown_trajectory, shown_inputs = _compact(trajectory, inputs, make_prompt("", ""))
        prompt = make_prompt(shown_trajectory, shown_inputs) + COMPACTION_NOTE
        image = image_bytes
        while True:
            try:
                response = ask(prompt, image)
                break
            except BadRequestError as retry_error:
                if not _context_overflow(retry_error):
                    raise
                smaller = _downscale(image) if image is not None else None
                if smaller is None:
                    raise
                with Image.open(io.BytesIO(smaller)) as shrunk:
                    new_size = shrunk.size
                warnings.warn(
                    f"Run {run.run_id} ({family.value}): still over context; "
                    f"downscaling figure to {new_size[0]}x{new_size[1]} and retrying.",
                    stacklevel=2,
                )
                image = smaller
    answer = response["choices"][0]["message"]["content"].strip()
    if not answer.upper().startswith("YES"):
        return []
    return [Error(family=family, evidence=answer[3:].lstrip(" :.-\n") or answer)]


def judge_execution(run: Run) -> list[Error]:
    """Check if the agent failed to produce a valid figure.

    Change 1 & 2: Programmatically verify figure presence and integrity.
    If no figure was produced or it cannot be decoded as an image, report execution_failure.
    If a valid figure was saved, rule out execution_failure and allow downstream checks.
    """
    if run.figure is None or not run.figure.is_file():
        return [
            Error(
                family=ErrorFamily.EXECUTION_FAILURE,
                evidence="The agent failed to produce or save a figure.png file in the run directory.",
            )
        ]

    try:
        with Image.open(run.figure) as img:
            img.verify()
        # Also check file non-empty
        if run.figure.stat().st_size == 0:
            return [
                Error(
                    family=ErrorFamily.EXECUTION_FAILURE,
                    evidence="The produced figure.png is an empty file (0 bytes).",
                )
            ]
    except Exception as exc:
        return [
            Error(
                family=ErrorFamily.EXECUTION_FAILURE,
                evidence=f"The produced figure.png cannot be opened or decoded as a valid image: {exc}",
            )
        ]

    # Valid figure was produced and decoded
    return []


def judge_data_and_chart(run: Run) -> list[Error]:
    """Whether the figure plots the requested data, built the requested way."""
    wrong_data = _ask(
        run,
        ErrorFamily.WRONG_DATA,
        "Does the plotted data differ from what was requested in any way?",
    )
    wrong_chart = _ask(
        run,
        ErrorFamily.WRONG_CHART,
        "Does the figure fail to follow any part of the requested chart design?",
    )
    return wrong_data + wrong_chart


def judge_readability(run: Run) -> list[Error]:
    """Whether the figure can be read."""
    return _ask(
        run,
        ErrorFamily.HARD_TO_READ,
        "Is the rendered figure difficult or impossible to read?",
    )


def validate(run: Run) -> list[Error]:
    """Evaluate a run.

    First check for execution failure. If an execution failure occurs (no valid figure),
    terminal short-circuiting applies so downstream checks are not executed.
    Otherwise, evaluate data, chart structure, and readability.
    """
    execution = judge_execution(run)
    if execution:
        return execution
    return judge_data_and_chart(run) + judge_readability(run)
