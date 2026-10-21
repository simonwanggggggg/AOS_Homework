
from pathlib import Path
import csv
import matplotlib

# Save charts without requiring a GUI window
matplotlib.use("Agg")

import matplotlib.pyplot as plt


METRICS = {
    "page_faults": "Page Faults",
    "interrupts": "Interrupts",
    "disk_writes": "Disk Writes"
}

STYLES = {
    "FIFO": ("#2563eb", "o"),
    "MFU": ("#f97316", "s"),
    "Enhanced Second-Chance": ("#16a34a", "^"),
    "Custom Algorithm V2": ("#dc2626", "D")
}


def plot_results(results):
    """
    Generate 9 comparison charts and CSV data files.

    results[reference_name][algorithm_name] contains
    dictionaries with:
        frames, page_faults, interrupts, disk_writes
    """

    # Use a path relative to this Python file
    output_dir = Path(__file__).resolve().parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    for ref_name, algorithms in results.items():

        # Save experimental data as CSV
        csv_path = output_dir / f"{ref_name}_results.csv"

        with csv_path.open(
            "w", newline="", encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow([
                "Reference",
                "Algorithm",
                "Frames",
                "Page Faults",
                "Interrupts",
                "Disk Writes"
            ])

            for algo_name, records in algorithms.items():
                for record in records:
                    writer.writerow([
                        ref_name,
                        algo_name,
                        record["frames"],
                        record["page_faults"],
                        record["interrupts"],
                        record["disk_writes"]
                    ])

        # Generate charts for three performance metrics
        for metric, ylabel in METRICS.items():

            fig, ax = plt.subplots(figsize=(9, 5.5))

            for algo_name, records in algorithms.items():

                frames = [r["frames"] for r in records]
                values = [r[metric] for r in records]

                color, marker = STYLES.get(
                    algo_name, (None, "o")
                )

                ax.plot(
                    frames,
                    values,
                    label=algo_name,
                    color=color,
                    marker=marker,
                    linewidth=2,
                    markersize=5
                )

            ax.set_title(
                f"{ref_name} Reference String - {ylabel}",
                fontsize=14
            )

            ax.set_xlabel("Number of Frames")
            ax.set_ylabel(ylabel)
            ax.set_xticks(range(10, 101, 10))

            ax.grid(
                True,
                linestyle="--",
                alpha=0.35
            )

            ax.legend()
            fig.tight_layout()

            filename = f"{ref_name}_{metric}.png"
            filepath = output_dir / filename

            fig.savefig(filepath, dpi=200)
            plt.close(fig)

            print(f"Saved: {filepath}")

    print("\nAll charts and CSV files saved!")
