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
    assert data.get("class_A_points") == 5000, f"Expected 5000, got {data.get('class_A_points')}"
    assert data.get("class_B_points") == 5000, f"Expected 5000, got {data.get('class_B_points')}"
