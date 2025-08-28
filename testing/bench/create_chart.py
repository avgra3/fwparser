import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from constants import CSV_NAME, DELIMITER


def make_df() -> pd.DataFrame:
    df = pd.read_csv(CSV_NAME, sep=DELIMITER, header=0)
    df_grouped = (
        df[
            [
                "function_name",
                "generated_rows",
                "execution_time_seconds",
                "cpu_name",
                "cpu_count",
            ]
        ]
        .groupby(
            by=["function_name", "generated_rows", "cpu_name", "cpu_count"],
            group_keys=False,
        )
        .mean()
    )

    pivot_df = df_grouped.pivot_table(
        index=["generated_rows"],
        columns=["function_name", "cpu_count"],
        values="execution_time_seconds",
    )
    return pivot_df


def make_chart(df: pd.DataFrame) -> None:
    df.plot.barh(rot=0, figsize=(15, 5))
    plt.title("Multiprocessing vs Single Process")
    plt.ylabel("Lines Parsed")
    plt.xlabel("execution time (seconds)")
    plt.legend(loc="center right")

    plot_name = Path.cwd() / "Benchmark_Results" / "Results.png"
    plt.savefig(
        plot_name,
        transparent=None,
        dpi="figure",
        format=None,
        metadata=None,
        bbox_inches=None,
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
