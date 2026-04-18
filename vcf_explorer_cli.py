"""
VCF Explorer: vcf_explorer_cli.py

Command-line interface module for argument parsing and validation.
"""
import logging
import argparse
import sys
from datetime import datetime
from pathlib import Path

import vcf_explorer_config as config

logger = logging.getLogger(__name__)

def parse_arguments() -> None:
    """
    Parse and validate command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments containing:
            - genome: Path to genome file
            - vcf: Path to vcf file
            - output: Output directory path
            - version: show version number
    """

    parser = argparse.ArgumentParser(
        description=
            "VCF Explorer: explore and analyse VCF files. Generates summary "
            "statistics and visualisations of variant data including filter "
            "type distributions, variant density, and quality scores.",
        epilog=
            "Example usage:\n"
            "  python vcf_explorer.py --vcf path/to/variants.vcf\n"
            "  python vcf_explorer.py --vcf path/to/variants.vcf --output path/to/output\n\n"
            "If no arguments are provided, the default VCF file will be used and "
            "output will be saved to the processed/ directory.",
            formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "--vcf",
        type=str,
        default=None,
        help="Path to the VCF file to analyse (.vcf). "
            "Defaults to data/raw/CEU.chr22.vcf if not provided."
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to the output directory. A timestamped subdirectory will be "
         "created automatically under processed/. "
         "Defaults to the script directory if not provided."
    )

    parser.add_argument(
        "--version",
        action="version",
        version="VCF Explorer v1.0.1"
    )

    return parser.parse_args()

def validate_arguments(args: argparse.Namespace) -> dict[str, any]:
    """
    Validate parsed command-line arguments and resolve file paths.

    Validates that the VCF file exists and has a supported extension. If an
    output directory is provided, constructs a timestamped subdirectory path
    under processed/.

    Args:
        args (argparse.Namespace): Parsed arguments from parse_arguments(), containing:
            - vcf (str | None): Path to the VCF file, or None to use the default.
            - output (str | None): Path to the output directory, or None to use the default.

    Returns:
        dict: A dictionary containing:
            - vcf_path (Path): Resolved path to the VCF file.
            - output_dir (Path | None): Resolved timestamped output path, or None
              if no output directory was provided.

    Raises:
        ValueError: If the VCF file does not exist or has an unsupported extension.
    """
    
    if args.vcf is None:
        logger.info(f"Using default VCF: {config.DEFAULT_VCF_FILE}")
        vcf_path = config.DEFAULT_VCF_FILE
    else:
        vcf_path = Path(args.vcf)

    if not vcf_path.exists():
        raise ValueError(f"VCF file not found: {vcf_path}")

    valid_extensions = config.VALID_EXTENSIONS

    if vcf_path.suffix.lower() not in valid_extensions:
        raise ValueError(f"Invalid file extension. Expected: {valid_extensions}")

    if args.output is None:
        output_dir = None
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vcf_name = vcf_path.stem

        base_output = Path(args.output)
        output_dir = base_output / "processed" / f"{vcf_name}_{timestamp}"

    return {
        "vcf_path": vcf_path,
        "output_dir": output_dir
    }
    