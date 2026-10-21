import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

outdir = 'report_output/figures'
os.makedirs(outdir, exist_ok=True)
fig, ax = plt.subplots(figsize=(6.5,4.5))
ax.axis('off')
ax.add_patch(patches.Rectangle((0.05,0.7),(0.9,0.12), edgecolor='black', facecolor='#c9def5'))
ax.add_patch(patches.Rectangle((0.05,0.45),(0.38,0.15), edgecolor='black', facecolor='#d7e7ff'))
ax.add_patch(patches.Rectangle((0.57,0.45),(0.38,0.15), edgecolor='black', facecolor='#d7e7ff'))
ax.add_patch(patches.Rectangle((0.3,0.2),(0.4,0.12), edgecolor='black', facecolor='#e8f0ff'))
ax.text(0.5,0.76,'Frontend (React + Vite + TypeScript SPA)', ha='center', va='center', weight='bold')
ax.text(0.24,0.525,'Express REST API + Socket.IO', ha='center', va='center', weight='bold')
ax.text(0.76,0.525,'External Services', ha='center', va='center', weight='bold')
ax.text(0.5,0.26,'MongoDB (Mongoose)', ha='center', va='center', weight='bold')
ax.annotate('', xy=(0.24,0.45), xytext=(0.5,0.32), arrowprops=dict(arrowstyle='->'))
ax.annotate('', xy=(0.76,0.45), xytext=(0.5,0.32), arrowprops=dict(arrowstyle='->'))
ax.annotate('', xy=(0.5,0.7), xytext=(0.24,0.6), arrowprops=dict(arrowstyle='->'))
ax.annotate('', xy=(0.5,0.7), xytext=(0.76,0.6), arrowprops=dict(arrowstyle='->'))
plt.savefig(os.path.join(outdir,'fig4_1_architecture.png'), dpi=300, bbox_inches='tight')
plt.close()
print('ok')
