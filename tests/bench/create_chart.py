from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .constants import CSV_NAME, DELIMITER


def make_df() -> pd.DataFrame:
    df = pd.read_csv(CSV_NAME, sep=DELIMITER, header=0)

    pivot_df = pd.pivot_table(
        df,
        index=["cpu_count"],  # , "generated_rows"],
        columns=["function_name"],
        values="execution_time_seconds",
        aggfunc="mean",
    )
    return pivot_df


def make_chart(df: pd.DataFrame) -> None:
    df.plot.bar(rot=0, figsize=(10, 5), table=False, width=1.0)
    plt.title("Multiprocessing vs Single Process")
    plt.xlabel("CPU Cores")
    plt.ylabel("Execution Time (seconds)")
    plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.0, 0.75),
        title="Function",
    )

    plot_name = Path.cwd() / "Benchmark_Results" / "Results.png"
    plt.savefig(
        plot_name,
        transparent=None,
        dpi="figure",
        format=None,
        metadata=None,
        bbox_inches="tight",
        pad_inches=0.1,
        facecolor="auto",
        edgecolor="auto",
        backend=None,
    )


def main():
    df = make_df()
    make_chart(df=df)


if __name__ == "__main__":
    main()
