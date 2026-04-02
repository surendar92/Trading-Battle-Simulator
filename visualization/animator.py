import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

COLORS = ["#00BFFF", "#FF6600", "#FF3333"]

def animate_equity_curves(equity_df, title="Algorithmic Trading Battle Simulator", interval=30, step=2):

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor("#0d0d0d")
    ax.set_facecolor("#0d0d0d")

    # styling
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("#00BFFF")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

    ax.set_title(title, fontsize=15, fontweight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Portfolio Value ($)", fontsize=11)

    # create one empty line per strategy
    lines = {}
    for i, col in enumerate(equity_df.columns):
        line, = ax.plot([], [], label=col, color=COLORS[i], linewidth=2)
        lines[col] = line

    ax.legend(facecolor="#1a1a1a", edgecolor="#444444", labelcolor="white")

    # fix axis limits upfront
    ax.set_xlim(equity_df.index[0], equity_df.index[-1])
    ax.set_ylim(equity_df.min().min() * 0.98, equity_df.max().max() * 1.02)

    plt.tight_layout()

    # frames = list of ending indices
    frames = list(range(2, len(equity_df), step)) + [len(equity_df)]

    def update(frame_end):
        subset = equity_df.iloc[:frame_end]
        for col, line in lines.items():
            line.set_data(subset.index, subset[col])
        return list(lines.values())

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=interval,
        blit=True,
        repeat=False
    )

    plt.show()