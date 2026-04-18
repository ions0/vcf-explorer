"""
VCF Explorer: tests/test_vcf_io.py

testing module for vcf_explorer_io.py
"""
import pytest

from pathlib import Path

from vcf_explorer_io import load_vcf


#========================== load_vcf() tests =============================================

def test_load_vcf_filetype():

    path = Path("/home/test.vcc")

    with pytest.raises(ValueError):
        load_vcf(path)

@pytest.fixture
def test_load_vcf_fixture(tmp_path):

    with open(tmp_path / "test.vcf", "w") as f:
        f.write(
            "##\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNA12891\t"
                                                                    "NA12892\tNA12878")
        f.write(
        "\n1\t10177\trs367896724\tA\tAC\t100\tPASS\tAC=1;AF=0.167;AN=6\tGT\t0/0\t0/1\t0/0"
        )

    return tmp_path / "test.vcf"

def test_load_vcf_col_names(test_load_vcf_fixture):
    
    df = load_vcf(test_load_vcf_fixture)
    cols = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", 
                                                        "NA12891", "NA12892", "NA12878"]
    df_cols = df.columns.tolist()

    assert cols == df_cols

