# strict-formatting-colors

Using matplotlib, draw a bar chart with 3 bars. The values are [10, 20, 15] for the categories ['A', 'B', 'C']. You MUST strictly color the first bar with hex code '#FF5733', the second with hex code '#33FF57', and the third with hex code '#3357FF'. Do not use default colors. Add an edge color of black to all bars with a line width of 2.5. The title must be exactly 'RGB Bars'. Save the output to figure.png.

## Required outputs

Leave these behind in `/app`, which is also the working directory. `plot.py` must
refer to these files by bare filename rather than by absolute path.

1. **`/app/plot.py`** - the plotting script. Self-contained and re-runnable.
2. **`/app/figure.png`** - the chart.
3. **`/app/plotted_values.json`** - the values shown in the chart. Schema:
   ```json
   {
     "values": [10, 20, 15],
     "categories": ["A", "B", "C"]
   }
   ```
