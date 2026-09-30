# high-frequency-sine

Using matplotlib, plot the function y = sin(100 * x) + cos(150 * x) for 10000 evenly spaced x values between 0 and 10. Use a black solid line with a line width of 0.5. Set the x-axis limits strictly from 0 to 10. Title it 'High Frequency Waves' and save the chart as figure.png.

## Required outputs

Leave these behind in `/app`, which is also the working directory. `plot.py` must
refer to these files by bare filename rather than by absolute path.

1. **`/app/plot.py`** - the plotting script. Self-contained and re-runnable:
   `python plot.py` from `/app` must reproduce the figure with no arguments and
   no manual steps.
2. **`/app/figure.png`** - the chart, as saved by that script.
3. **`/app/plotted_values.json`** - the values shown in the chart. Generate this
   file from the same variables used to draw the figure. It must contain the count of x values. Schema:
   ```json
   {
     "x_count": 10000
   }
   ```

Only the libraries already installed are available and there is no network
access; everything you need is in the image.
