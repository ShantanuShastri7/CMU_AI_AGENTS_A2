cat << 'EOF' > plot.py
import matplotlib.pyplot as plt
import json

slices = [1] * 20
labels = list(range(1, 21))

fig, ax = plt.subplots()
fig.patch.set_facecolor('#333333')
ax.pie(slices, labels=labels, textprops={'fontsize': 4})

plt.savefig('figure.png')

with open('plotted_values.json', 'w') as f:
    json.dump({"slices": len(slices), "labels": labels}, f)
EOF

python plot.py
