cat << 'EOF' > plot.py
import matplotlib.pyplot as plt
import json

categories = ['A', 'B', 'C']
values = [10, 20, 15]
colors = ['red', 'green', 'blue'] # WRONG COLORS!

plt.bar(categories, values, color=colors, edgecolor='black', linewidth=2.5)
plt.title('RGB Bars')
plt.savefig('figure.png')

with open('plotted_values.json', 'w') as f:
    json.dump({"values": values, "categories": categories}, f)
EOF

python plot.py
