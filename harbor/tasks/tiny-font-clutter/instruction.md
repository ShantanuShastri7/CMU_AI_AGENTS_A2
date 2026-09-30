# tiny-font-clutter

Using matplotlib, create a pie chart with 20 equal slices. Label each slice with the numbers 1 through 20. You MUST set the font size of the slice labels to exactly 4 points so they are tiny. The background of the entire figure must be dark gray ('#333333'). Save the figure to figure.png.

## Required outputs

Leave these behind in `/app`, which is also the working directory. `plot.py` must refer to these files by bare filename.

1. **`/app/plot.py`**
2. **`/app/figure.png`**
3. **`/app/plotted_values.json`** - Schema:
   ```json
   {
     "slices": 20,
     "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
   }
   ```
