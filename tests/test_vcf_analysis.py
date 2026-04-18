"""
VCF Explorer: tests/test_vcf_analysis.py

testing module for vcf_explorer_analysis.py
"""
import pytest
from pathlib import Path

import pandas as pd

from vcf_explorer_analysis import calculate_variant_density, calculate_stats

#========================== calculate_variant_density() tests ============================

def test_calc_density():

    test_data = [
        {"POS": 10},
        {"POS": 20},
        {"POS": 30},
        {"POS": 40}
    ]

    test_df = pd.DataFrame(test_data)
    pos, den = calculate_variant_density(test_df, 40, 20, 20)
    
    assert pos == [10, 30]
    assert den == [1, 2]


def test_calc_density_empty_df():

    test_df = pd.DataFrame({"POS": []})

    with pytest.raises(ValueError):
        pos, den = calculate_variant_density(test_df, 100, 20, 20)
        
def test_calc_density_window_larger():

    test_data = [
        {"POS": 10},
        {"POS": 20},
        {"POS": 30},
        {"POS": 40}
    ]

    test_df = pd.DataFrame(test_data)

    with pytest.raises(ValueError):
        pos, den = calculate_variant_density(test_df, test_df["POS"].max(), 50, 20)

def test_calc_density_nonnumeric_pos():

    test_data = [
        {"POS": 10},
        {"POS": 20},
        {"POS": 30},
        {"POS": "x"}
    ]

    test_df = pd.DataFrame(test_data)

    with pytest.raises(TypeError):
        pos, den = calculate_variant_density(test_df, test_df["POS"].max(), 20, 20)

#========================== calculate_stats() tests ======================================

def test_calc_stats():

    test_data = {
        "FILTER": [".", "mapQ=0", "."],
        "REF": ["a", "t", "c"],
        "ALT": ["t", "g", "a"]
    }

    test_df = pd.DataFrame(test_data)
    test_dict = calculate_stats(test_df)

    keys = ["shape", "missing", "desc", "filter_counts", "snp_counts", "indel_counts"]

    assert keys == list(test_dict.keys())

def test_calc_stats_values():

    test_data = {
        "FILTER": [".", "mapQ=0", ".", None],
        "REF": ["a", "t", "c", "g"],
        "ALT": ["t", "g", "a", "c"],
    }

    test_df = pd.DataFrame(test_data)
    test_dict = calculate_stats(test_df)

    assert len(test_dict["filter_counts"]) == 2
    assert test_dict["snp_counts"] == 4
    assert test_dict["shape"] == (4, 3)
    assert test_dict["missing"]["FILTER"] == 1
    assert test_dict["desc"].shape[0] == 4
