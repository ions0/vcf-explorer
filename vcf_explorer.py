"""
VCF Explorer: vcf_explorer.py

A basic tool for exploring and analysing VCF (Variant Call Format) files.
Performs statistical analysis and generates visualisations of variant data.

Features:
    - VCF file loading and validation
    - Variant statistics (shape, missing values, SNP/indel counts)
    - Filter type distribution analysis
    - Variant density sliding window analysis
    - Quality score distribution
    - Basic visualisation suite
    - Logging for debugging and audit trails

Usage:
    python vcf_explorer.py --vcf path/to/variants.vcf [options]

    Options:
        --vcf PATH          Path to VCF file (.vcf)
        --output DIR        Custom output directory (default: auto-generated)
        --help              Show help message
        --version           Show version information

Output Structure:
    processed/[vcf_name]_[timestamp]/
        ├── logs/
        │   └── vcf_explorer_[timestamp].log
        └── visualisations/
            ├── filter_types.png
            ├── variant_density.png
            └── quality_scores.png

Author: Jared Cambridge
Date: April 01, 2026
Updated: April 13, 2026
Version: 1.0.0
"""

import logging
from datetime import datetime
from pathlib import Path

import vcf_explorer_cli
import vcf_explorer_config as config
from vcf_explorer_io import load_vcf
from vcf_explorer_analysis import (
    calculate_stats, 
    calculate_variant_density, 
    extract_qual
)
from vcf_explorer_config import setup_logging, setup_output_directories
from vcf_explorer_reporter import print_stats
from vcf_explorer_visualiser import (
    plot_filter_types, 
    plot_variant_density, 
    plot_qual_score
)

logger = logging.getLogger(__name__)

def main(vcf_path=None, output_dir=None):
    """
    Run the VCF Explorer analysis pipeline.

    Orchestrates the full analysis pipeline: sets up output directories,
    loads the VCF file, calculates summary statistics, prints them to stdout,
    and generates and saves all visualisations.

    Args:
        vcf_path (Path | None): Path to the VCF file to analyse. Defaults to
            config.DEFAULT_VCF_FILE if None.
        output_dir (Path | None): Root output directory for the current run.
            A timestamped directory is constructed from the VCF filename if
            None.
    """
    
    logger.info("Output directories created")

    vcf = load_vcf(vcf_path)
    vcf_name = vcf_path.stem
    logger.info(f"Successfully loaded: {len(vcf)} variants from path: {vcf_path}")

    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = config.SCRIPT_PATH / f"{vcf_name}_{timestamp}"

    setup_output_directories(output_dir)
    stats_dict = calculate_stats(vcf)
    print_stats(stats_dict)   

    plot_filter_types(
        stats_dict["filter_counts"], config.FIGSIZE, 
                                            output_dir / "visualisations", vcf_name)
    positions, counts = calculate_variant_density(
        vcf, vcf["POS"].max(), config.WINDOW_SIZE, config.STEP_SIZE)
    plot_variant_density(positions, counts, config.FIGSIZE, 
                                            output_dir / "visualisations", vcf_name)
    q_scores = extract_qual(vcf)
    plot_qual_score(q_scores, config.FIGSIZE, output_dir / "visualisations", vcf_name)

if __name__ == "__main__":

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args = vcf_explorer_cli.parse_arguments()
        config_dict = vcf_explorer_cli.validate_arguments(args)

        if args.vcf is None:
            vcf_name = config.DEFAULT_VCF_FILE.stem
        else:
            vcf_name = Path(args.vcf).stem.replace(" ", "_").replace(".", "_")

        if config_dict["output_dir"] is None:
            output_dir = config.DATA_PATH / "processed" / f"{vcf_name}_{timestamp}"
        else:
            output_dir = config_dict["output_dir"]

        setup_logging(output_dir / "logs")
        config.validate_config()

        logger.info(f"VCF Explorer {config.VERSION} started")

        main(
            vcf_path=config_dict["vcf_path"],
            output_dir=output_dir
        )

    except ValueError as e:
        print(e)

    except FileNotFoundError as e:
        print(e)