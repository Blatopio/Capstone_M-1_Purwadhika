import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(16, 10), facecolor="#1E1E2E")

gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.55, wspace=0.4)

# Our first card — top left slot
ax = fig.add_subplot(gs[0, 0])        # row 0, column 0
ax.set_facecolor("#4C9BE822")          # light blue background
ax.text(0.5, 0.65, "550", ha='center', va='center',
        fontsize=13, fontweight='bold', color="#4C9BE8",
        transform=ax.transAxes)
ax.text(0.5, 0.2, "Total Transactions", ha='center', va='center',
        fontsize=8, color='#AAAAAA',
        transform=ax.transAxes)
ax.set_xticks([])
ax.set_yticks([])

plt.show()