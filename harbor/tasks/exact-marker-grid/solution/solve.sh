cat << 'EOF' > plot.py
import matplotlib.pyplot as plt
import json

points = [[1, 1], [2, 4], [3, 9]]
x = [p[0] for p in points]
y = [p[1] for p in points]

fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)

axs[0, 0].scatter(x, y, marker='*', s=100)
axs[0, 1].scatter(x, y, marker='p', s=100)
axs[1, 0].scatter(x, y, marker='h', s=100)
axs[1, 1].scatter(x, y, marker='D', s=100)

plt.savefig('figure.png')

with open('plotted_values.json', 'w') as f:
    json.dump({"points": points}, f)
EOF

python plot.py
