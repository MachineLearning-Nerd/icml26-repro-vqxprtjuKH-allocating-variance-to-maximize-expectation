"""Generate the five evidence-bearing figures for the public report."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


COLORS = {
    "VERIFIED": "#16805c",
    "FALSIFIED": "#ad3f31",
    "BLOCKED": "#73777f",
    "blue": "#2775b6",
    "gold": "#d59624",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def finish(figure: plt.Figure, path: Path) -> None:
    figure.tight_layout()
    figure.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def verdict_overview(output: Path) -> None:
    claims = ["Claim 1", "Claim 2", "Claim 3", "Claim 4", "Claim 5", "Claim 6"]
    statuses = [
        "VERIFIED",
        "FALSIFIED",
        "VERIFIED",
        "FALSIFIED",
        "VERIFIED",
        "BLOCKED",
    ]
    figure, axis = plt.subplots(figsize=(9.2, 3.8))
    axis.barh(
        range(len(claims)),
        [1] * len(claims),
        color=[COLORS[status] for status in statuses],
        height=0.62,
    )
    axis.set_yticks(range(len(claims)), claims)
    axis.invert_yaxis()
    axis.set_xlim(0, 1)
    axis.set_xticks([])
    for index, status in enumerate(statuses):
        axis.text(0.5, index, status, ha="center", va="center", color="white", weight="bold")
    axis.set_title("Claim-by-claim evidence verdicts (not live judge points)", loc="left", weight="bold")
    for spine in axis.spines.values():
        spine.set_visible(False)
    finish(figure, output / "headline_verdicts.png")


def claim1_scaling(data_root: Path, output: Path) -> None:
    rows = [
        row
        for row in read_csv(data_root / "claim1_algorithm1.csv")
        if row["kind"] == "scaling"
    ]
    n_values = [int(row["n"]) for row in rows]
    runtimes = [float(row["runtime_seconds"]) for row in rows]
    candidates = [int(row["candidate_count"]) for row in rows]
    figure, left = plt.subplots(figsize=(8.2, 4.7))
    right = left.twinx()
    left.plot(n_values, runtimes, "o-", color=COLORS["blue"], linewidth=2.3, label="runtime")
    right.plot(n_values, candidates, "s--", color=COLORS["gold"], linewidth=2.0, label="candidates")
    left.set_xscale("log", base=2)
    left.set_yscale("log")
    right.set_yscale("log")
    left.set_xlabel("number of variables n")
    left.set_ylabel("runtime (seconds)", color=COLORS["blue"])
    right.set_ylabel("enumerated candidates", color=COLORS["gold"])
    left.grid(alpha=0.25, which="both")
    left.set_title("Algorithm 1: fixed-ε scaling to n=512", loc="left", weight="bold")
    finish(figure, output / "claim1_scaling.png")


def claim3_scaling(data_root: Path, output: Path) -> None:
    rows = [
        row
        for row in read_csv(data_root / "claim3_algorithm3.csv")
        if row["kind"] == "scaling"
    ]
    n_values = [int(row["n"]) for row in rows]
    runtimes = [float(row["runtime_seconds"]) for row in rows]
    figure, axis = plt.subplots(figsize=(8.2, 4.7))
    axis.plot(n_values, runtimes, "o-", color=COLORS["blue"], linewidth=2.3)
    axis.set_xscale("log", base=2)
    axis.set_yscale("log")
    axis.set_xlabel("number of variables n")
    axis.set_ylabel("runtime (seconds)")
    axis.grid(alpha=0.25, which="both")
    axis.set_title("Algorithm 3: sparse explicit inputs to n=16,384", loc="left", weight="bold")
    finish(figure, output / "claim3_scaling.png")


def claim5_nonzero(data_root: Path, output: Path) -> None:
    rows = read_csv(data_root / "claim5_nonzero_cases.csv")
    epsilon = [eval(row["epsilon"], {"__builtins__": {}}, {}) for row in rows]
    observed = [float(row["expected_positive_max"]) for row in rows]
    bound = [float(row["explicit_upper_bound"]) for row in rows]
    figure, axis = plt.subplots(figsize=(8.2, 4.7))
    axis.plot(epsilon, bound, "o-", color=COLORS["gold"], linewidth=2.3, label="explicit proof bound")
    axis.plot(epsilon, observed, "s-", color=COLORS["blue"], linewidth=2.3, label="nonzero stress family")
    axis.set_xscale("log", base=2)
    axis.invert_xaxis()
    axis.set_xlabel("ε (smaller →)")
    axis.set_ylabel("expected positive maximum")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False)
    axis.set_title("Lemma 2.1: nonzero variances remain below the bound", loc="left", weight="bold")
    finish(figure, output / "claim5_nonzero_bound.png")


def claim6_digitization(data_root: Path, output: Path) -> None:
    rows = read_csv(data_root / "claim6_digitized_payoff.csv")
    figure, axis = plt.subplots(figsize=(8.2, 4.7))
    for name, color in (("independent", COLORS["blue"]), ("negative", COLORS["gold"])):
        selected = [row for row in rows if row["series"] == name]
        p_values = [float(row["p"]) for row in selected]
        pixel_y = [float(row["pixel_y"]) for row in selected]
        # Image y grows downward; negate only to show the displayed upward payoff.
        axis.plot(p_values, [-value for value in pixel_y], "o-", linewidth=2.3, label=name, color=color)
    axis.set_xlabel("edge probability p")
    axis.set_ylabel("digitized vertical position (higher is larger)")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False)
    axis.set_title("Figure 1 digitization supports shape, not regeneration", loc="left", weight="bold")
    finish(figure, output / "claim6_digitized_curves.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("space_candidate/raw"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    verdict_overview(args.output)
    claim1_scaling(args.data_root, args.output)
    claim3_scaling(args.data_root, args.output)
    claim5_nonzero(args.data_root, args.output)
    claim6_digitization(args.data_root, args.output)


if __name__ == "__main__":
    main()
