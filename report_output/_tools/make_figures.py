import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

outdir = 'report_output/figures'
os.makedirs(outdir, exist_ok=True)

# Fig 4.1 Architecture - 3 tier
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.axis('off')
# boxes
ax.add_patch(patches.Rectangle((0.05,0.75),(0.9,0.2), edgecolor='black', facecolor='#c9def5'))
ax.add_patch(patches.Rectangle((0.05,0.45),(0.425,0.25), edgecolor='black', facecolor='#d7e7ff'))
ax.add_patch(patches.Rectangle((0.525,0.45),(0.425,0.25), edgecolor='black', facecolor='#d7e7ff'))
ax.add_patch(patches.Rectangle((0.3,0.15),(0.4,0.2), edgecolor='black', facecolor='#e8f0ff'))
ax.text(0.5,0.85,'Frontend (React + Vite + TypeScript SPA)', ha='center', va='center', weight='bold')
ax.text(0.2675,0.575,'Express REST API + Socket.IO', ha='center', va='center', weight='bold')
ax.text(0.7375,0.575,'External Services', ha='center', va='center', weight='bold')
ax.text(0.5,0.25,'MongoDB (Mongoose)', ha='center', va='center', weight='bold')
# arrows
ax.arrow(0.5,0.75,0, -0.05, width=0.005, head_width=0.03)
ax.arrow(0.2675,0.45,0,-0.1, width=0.005, head_width=0.03)
ax.text(0.52,0.72,'HTTPS/REST, Socket.IO', fontsize=8)
ax.text(0.52,0.35,'Mongoose ODM', fontsize=8)
plt.savefig(os.path.join(outdir,'fig4_1_architecture.png'), dpi=300, bbox_inches='tight')
plt.close()

print('done basic')
