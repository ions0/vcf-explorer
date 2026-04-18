"""
VCF Explorer: vcf_explorer_analysis.py

"""
import logging

import pandas as pd
from pathlib import Path

from vcf_explorer_io import load_vcf
import vcf_explorer_config as config

logger = logging.getLogger(__name__)

def calculate_stats(vcf_df:pd.DataFrame) -> dict:
    """
    Calculate summary statistics for a VCF DataFrame.

    Args:
        vcf_df (pd.DataFrame): DataFrame loaded from a VCF file.

    Returns:
        dict: A dictionary containing:
            - shape (tuple): Row and column counts.
            - missing (pd.Series): Missing value counts per column.
            - desc (pd.DataFrame): Descriptive statistics for numeric columns.
            - filter_counts (pd.Series): Value counts for the FILTER column.
            - snp_counts (int): Number of SNPs (single base REF and ALT).
            - indel_counts (int): Number of indels (multi-base REF and ALT).

    Raises:
        ValueError: If the DataFrame is None or empty.
    """

    if vcf_df is None:
        logger.error("DataFrame is invalid.")
        raise ValueError("DataFrame is invalid. Exiting.")

    if vcf_df.empty:
        logger.error("DataFrame is empty.")
        raise ValueError("DataFrame is empty. Exiting.")

    vcf_shape = vcf_df.shape
    vcf_missing = vcf_df.isnull().sum()
    vcf_desc = vcf_df.describe()
    vcf_filter_counts = vcf_df["FILTER"].value_counts()
    vcf_snp_counts = (((vcf_df['REF'].str.len() == 1) &
                                (vcf_df["ALT"].str.len() == 1)).sum())
    vcf_indel_counts = (((vcf_df['REF'].str.len() > 1) &
                                        (vcf_df["ALT"].str.len() > 1)).sum())

    return {
        "shape": vcf_shape,
        "missing": vcf_missing,
        "desc": vcf_desc,
        "filter_counts": vcf_filter_counts,
        "snp_counts": vcf_snp_counts,
        "indel_counts": vcf_indel_counts
    }

def extract_qual(vcf_df: pd.DataFrame) -> list[int]:
    """
    Extract quality scores from the QUAL column of a VCF DataFrame.

    Args:
        vcf_df (pd.DataFrame): DataFrame loaded from a VCF file.

    Returns:
        list: Quality scores from the QUAL column.

    Raises:
        ValueError: If the DataFrame is None or empty.
    """

    if vcf_df is None:
        logger.error("DataFrame is invalid.")
        raise ValueError("DataFrame is invalid. Exiting.")

    if vcf_df.empty:
        logger.error("DataFrame is empty.")
        raise ValueError("DataFrame is empty. Exiting.")

    qual_scores = [x for x in vcf_df["QUAL"]]
    return qual_scores

def calculate_variant_density(
    vcf_df: pd.DataFrame,
    vcf_length: int,
    window_size: int = config.WINDOW_SIZE,
    step: int = config.STEP_SIZE
) -> tuple[list[int], list[int]]:

    """
    Calculate variant density across a chromosome using a sliding window.

    Counts the number of variants whose POS falls within each window,
    stepping across the chromosome from position 0 to vcf_length.

    Args:
        vcf_df (pd.DataFrame): DataFrame loaded from a VCF file.
        vcf_length (int): Total length of the chromosome (typically POS.max()).
        window_size (int): Width of the sliding window in base pairs. Defaults to config.WINDOW_SIZE.
        step (int): Step size between windows in base pairs. Defaults to config.STEP_SIZE.

    Returns:
        tuple[list[int], list[int]]: A tuple of (positions, counts) where:
            - positions: Midpoint of each window.
            - counts: Number of variants within each window.

    Raises:
        ValueError: If window_size exceeds vcf_length, or if POS contains non-numeric values.
    """

    if vcf_df.empty:
        raise ValueError("DataFrame is empty. Exiting.")

    if window_size > vcf_length:
        logger.error("Window size larger than vcf")
        raise ValueError("Error: Window size larger than VCF length, exiting.")

    if not pd.api.types.is_numeric_dtype(vcf_df["POS"]):
        logger.error("POS contains non-numerical values.")
        raise TypeError("POS contains non-numerical values. Exiting.")

    density = []
    positions = []

    for i in range(0, vcf_length - window_size + 1, step):
        window_start = i
        window_end = i + window_size

        count = len(vcf_df[(vcf_df["POS"] >= window_start) & 
                           (vcf_df["POS"] < window_end)])

        density.append(count)
        positions.append(window_start + window_size // 2)

        i += step

        # Safety to prevent infinite loop if step=0 (shouldn't happen)
        if step <= 0:
            break

    return positions, density