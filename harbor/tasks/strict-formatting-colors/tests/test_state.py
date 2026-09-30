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
    assert data.get("values") == [10, 20, 15]
    assert data.get("categories") == ["A", "B", "C"]
