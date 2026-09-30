# dense-scatter-overlap

Using matplotlib, generate a scatter plot with two classes. Class A is 5000 points drawn from a normal distribution with mean (0,0) and standard deviation 1. Class B is 5000 points drawn from a normal distribution with mean (0.5, 0.5) and standard deviation 1. Plot Class A in blue with an alpha of 0.1, and Class B in red with an alpha of 0.1. Add a legend, title 'Dense Scatter', and save as figure.png.

## Required outputs

Leave these behind in `/app`, which is also the working directory. `plot.py` must
refer to these files by bare filename rather than by absolute path.

1. **`/app/plot.py`** - the plotting script. Self-contained and re-runnable:
   `python plot.py` from `/app` must reproduce the figure with no arguments and
   no manual steps.
2. **`/app/figure.png`** - the chart, as saved by that script.
3. **`/app/plotted_values.json`** - the values shown in the chart. Generate this
   file from the same variables used to draw the figure. It must contain the number of points generated for each class. Schema:
   ```json
   {
     "class_A_points": 5000,
     "class_B_points": 5000
   }
   ```

Only the libraries already installed are available and there is no network
access; everything you need is in the image.
