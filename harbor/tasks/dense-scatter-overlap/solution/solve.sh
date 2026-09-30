cat << 'EOF' > plot.py
import matplotlib.pyplot as plt
import numpy as np
import json

np.random.seed(42)
class_a = np.random.normal(0, 1, (5000, 2))
class_b = np.random.normal(0.5, 1, (5000, 2))

plt.scatter(class_a[:, 0], class_a[:, 1], c='blue', alpha=0.1, label='Class A')
plt.scatter(class_b[:, 0], class_b[:, 1], c='red', alpha=0.1, label='Class B')
plt.title('Dense Scatter')
plt.legend()
plt.savefig('figure.png')

with open('plotted_values.json', 'w') as f:
    json.dump({
        "class_A_points": len(class_a),
        "class_B_points": len(class_b)
    }, f)
EOF

python plot.py
