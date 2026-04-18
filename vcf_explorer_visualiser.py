"""
VCF Explorer: vcf_explorer_visualiser.py

"""
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 

import vcf_explorer_config as config

logger = logging.getLogger(__name__)

def plot_filter_types(
    filter_counts: pd.Series, 
    figsize: tuple[int, int], 
    output_dir: Path,
    vcf_name: str
) -> None:

    """
    Plot a bar chart of variant filter type counts.

    Plots the top 15 filter types on a log-scaled y-axis. The plot is saved
    to output_dir and displayed.

    Args:
        filter_counts (pd.Series): Value counts for the FILTER column, as
            returned in the stats dictionary from calculate_stats().
        figsize (tuple[int, int]): Figure dimensions as (width, height) in inches.
        output_dir (Path): Directory where the plot will be saved. Created if
            it does not already exist.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=figsize)
    filter_counts[:15].plot.bar().set_yscale("log")
    plt.xlabel("FILTER type")
    plt.xticks(rotation=45)
    plt.ylabel("Count")
    plt.title(f"Filter Counts: {vcf_name}")
    plt.tight_layout()

    filename = output_dir /  "filter_types.png"
    logger.info(f"Saving file: {filename.name}, to directory: {output_dir}")
    plt.savefig(filename)
    plt.show()

def plot_variant_density(
    positions: list[int], 
    counts: list[int], 
    figsize: tuple[int, int], 
    output_dir: Path,
    vcf_name: str
) -> None:

    """
    Plot variant density across the chromosome as a line chart.

    Filters out windows with zero variants before plotting. A dashed red line
    marks the mean variant count across all non-zero windows. The plot is
    saved to output_dir and displayed.

    Args:
        positions (list[int]): Window midpoint positions, as returned by
            calculate_variant_density().
        counts (list[int]): Variant counts per window, as returned by
            calculate_variant_density().
        figsize (tuple[int, int]): Figure dimensions as (width, height) in inches.
        output_dir (Path): Directory where the plot will be saved. Created if
            it does not already exist.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    zipped = [(pos, cnt) for pos, cnt in zip(positions, counts) if cnt > 0]
    pos, cnt = zip(*zipped)

    plt.figure(figsize=figsize)
    plt.plot(pos, cnt, linewidth=0.6, color="darkgreen")
    plt.axhline(y=np.mean(cnt), color="red", linestyle="--", linewidth=2, 
                                                label=f"Mean: {np.mean(cnt):.2f}")
    plt.xlabel("Variant Position")
    plt.ylabel(f"Number of Variants per {config.STEP_SIZE}")
    plt.grid(alpha=0.3)
    plt.ylim(bottom=0)
    plt.title(f"Variant Density Across {vcf_name}")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.legend()

    filename = output_dir /  "variant_density.png"
    logger.info(f"Saving file: {filename.name}, to directory: {output_dir}")
    plt.savefig(filename)
    plt.show()

def plot_qual_score(
    scores: int, 
    figsize: tuple[int, int], 
    output_dir: Path,
    vcf_name: str
) -> None:
    """
    Plot a histogram of variant quality scores.

    Bins scores into 150 intervals. A dashed red line marks the median
    quality score. The plot is saved to output_dir and displayed.

    Args:
        scores (list): Quality scores extracted from the QUAL column, as
            returned by extract_qual().
        figsize (tuple[int, int]): Figure dimensions as (width, height) in inches.
        output_dir (Path): Directory where the plot will be saved. Created if
            it does not already exist.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=figsize)
    plt.hist(scores, bins=150)
    plt.axvline(np.median(scores), color="red", linestyle="--", linewidth=2, 
                                                    label=f"Median: {np.median(scores)}")
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.title(f"Quality Scores: {vcf_name}")
    plt.tight_layout()
    plt.legend()
    
    filename = output_dir / "quality_scores.png"
    logger.info(f"Saving file: {filename.name}, to directory: {output_dir}")
    plt.savefig(filename)
    plt.show()