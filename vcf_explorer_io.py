"""
VCF Explorer: vcf_explorer_io.py

VCF input/output functions for loading and reading vcf files.
"""
import logging
from pathlib import Path

import pandas as pd

import vcf_explorer_config as config

logger = logging.getLogger(__name__)

def load_vcf(path: Path) -> pd.DataFrame:
    """
    Load a VCF file into a pandas DataFrame.

    Reads the VCF file, extracting column names from the #CHROM header line
    and skipping all other comment lines. The resulting DataFrame columns
    match the VCF header fields with the leading # stripped.

    Args:
        path (Path): Path to the VCF file to load.

    Returns:
        pd.DataFrame: DataFrame containing the variant data, with columns
            derived from the #CHROM header line (e.g. CHROM, POS, ID, REF,
            ALT, QUAL, FILTER, INFO, FORMAT, and any sample columns).

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If the file has an unsupported extension.
        OSError: If the file cannot be opened or read.
    """
    
    valid_extensions = config.VALID_EXTENSIONS

    if path.suffix.lower() not in valid_extensions:
        logger.error("Invalid file extension")
        raise ValueError(f"Invalid file extension. Expected: {valid_extensions}")

    if not path.exists():
        logger.error(f"{path} does not exist.")
        raise FileNotFoundError(f"{path} does not exist. Exiting.")
        
    try:
        with open(path) as f:
            content = f.readlines()
            for line in content:
                if line.startswith("#CHROM"):
                    columns = line
                    break
                
            columns = columns.removeprefix("#").strip().split("\t")
            csv = pd.read_csv(path, comment="#", names=columns, delimiter="\t")
    
    except OSError as e:
        logger.error(f"File: {path}, cannot be found.")
        raise

    return csv