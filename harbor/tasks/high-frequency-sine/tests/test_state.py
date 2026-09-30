import json
import pytest
from pathlib import Path
from PIL import Image

def test_figure_exists():
    fig = Path("/app/figure.png")
    assert fig.is_file(), "figure.png is missing"
    with Image.open(fig) as img:
        img.verify()

def test_plotted_values():
    path = Path("/app/plotted_values.json")
    assert path.is_file(), "plotted_values.json is missing"
    data = json.loads(path.read_text())
    assert data.get("x_count") == 10000, f"Expected 10000, got {data.get('x_count')}"
