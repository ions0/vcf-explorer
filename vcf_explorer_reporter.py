"""
VCF Explorer: vcf_explorer_reporter.py

"""
import pandas as pd

def print_stats(vcf_dict: dict) -> None:
    """
    Print summary statistics from a VCF stats dictionary to stdout.

    Args:
        vcf_dict (dict): Statistics dictionary returned by calculate_stats(),
            containing the following keys:
                - shape (tuple): Row and column counts.
                - missing (pd.Series): Missing value counts per column.
                - desc (pd.DataFrame): Descriptive statistics for numeric columns.
                - filter_counts (pd.Series): Value counts for the FILTER column.
                - snp_counts (int): Number of SNPs.
                - indel_counts (int): Number of indels.
    """
    
    print(f"\nSHAPE: {vcf_dict["shape"]}")
    print(f"\nMISSING VALUES: \n{vcf_dict["missing"]}")
    print(f"\nDESCRIPTION: {vcf_dict["desc"]}")
    print(f"\nFILTER COUNTS: {vcf_dict["filter_counts"]}")
    print(f"\nSNP COUNTS: {vcf_dict["snp_counts"]}")
    print(f"\nINDEL COUNTS: {vcf_dict["indel_counts"]}")
    print("\n\n")
