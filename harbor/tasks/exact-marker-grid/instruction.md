# exact-marker-grid

Using matplotlib, create a 2x2 grid of subplots sharing the x and y axes. In all 4 subplots, plot the points (1,1), (2,4), (3,9). You MUST use a completely different marker in each subplot: a star ('*') in the top-left, a pentagon ('p') in the top-right, a hexagon ('h') in the bottom-left, and a diamond ('D') in the bottom-right. The markers must have size 100. Save the figure to figure.png.

## Required outputs

Leave these behind in `/app`, which is also the working directory. `plot.py` must refer to these files by bare filename.

1. **`/app/plot.py`**
2. **`/app/figure.png`**
3. **`/app/plotted_values.json`** - Schema:
   ```json
   {
     "points": [[1, 1], [2, 4], [3, 9]]
   }
   ```
