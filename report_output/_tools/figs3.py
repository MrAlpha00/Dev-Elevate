import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

outdir = 'report_output/figures'
os.makedirs(outdir, exist_ok=True)

fig, ax = plt.subplots(figsize=(6.5,4.5))
ax.axis('off')
ax.add_patch(patches.Rectangle((0.05,0.75),(0.9,0.15), edgecolor='black', facecolor='#c9def5'))
ax.add_patch(patches.Rectangle((0.05,0.5),(0.4,0.2), edgecolor='black', facecolor='#d7e7ff'))
ax.add_patch(patches.Rectangle((0.55,0.5),(0.4,0.2), edgecolor='black', facecolor='#d7e7ff'))
ax.add_patch(patches.Rectangle((0.3,0.2),(0.4,0.2), edgecolor='black', facecolor='#e8f0ff'))
ax.text(0.5,0.825,'Frontend (React + Vite + TypeScript SPA)', ha='center', va='center', weight='bold')
ax.text(0.25,0.6,'Express REST API + Socket.IO', ha='center', va='center', weight='bold')
ax.text(0.75,0.6,'External Services', ha='center', va='center', weight='bold')
ax.text(0.5,0.3,'MongoDB (Mongoose)', ha='center', va='center', weight='bold')
ax.annotate('', xy=(0.25,0.5), xytext=(0.25,0.4), arrowprops=dict(arrowstyle='->'))
ax.annotate('', xy=(0.5,0.3), xytext=(0.5,0.4), arrowprops=dict(arrowstyle='->'))
ax.annotate('', xy=(0.5,0.825), xytext=(0.25,0.7), arrowprops=dict(arrowstyle='->'))
ax.annotate('', xy=(0.5,0.825), xytext=(0.75,0.7), arrowprops=dict(arrowstyle='->'))
plt.savefig(os.path.join(outdir,'fig4_1_architecture.png'), dpi=300, bbox_inches='tight')
plt.close()
print('ok')
