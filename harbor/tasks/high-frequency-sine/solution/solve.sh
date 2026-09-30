cat << 'EOF' > plot.py
import matplotlib.pyplot as plt
import numpy as np
import json

x = np.linspace(0, 10, 10000)
y = np.sin(100 * x) + np.cos(150 * x)

plt.plot(x, y, color='black', linewidth=0.5, linestyle='solid')
plt.xlim(0, 10)
plt.title('High Frequency Waves')
plt.savefig('figure.png')

with open('plotted_values.json', 'w') as f:
    json.dump({"x_count": len(x)}, f)
EOF

python plot.py
