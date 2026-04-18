# VCF Explorer

A basic tool for exploring and analysing VCF (Variant Call Format) files.
Performs statistical analysis and generates visualisations of variant data.

Built as a self-directed learning project using Claude AI prior to tertiary study.

---

## Features

- VCF file loading and validation
- Variant statistics (shape, missing values, SNP/indel counts)
- Filter type distribution analysis
- Variant density sliding window analysis
- Quality score distribution
- Basic visualisation suite
- Logging for debugging and audit trails

---

## Project Structure

```
vcf_explorer/
├── vcf_explorer.py                 # Main entry point
├── vcf_explorer_analysis.py        # Statistical analysis functions
├── vcf_explorer_cli.py             # Argument parsing and validation
├── vcf_explorer_io.py              # File Loading
├── vcf_explorer_reporter.py        # Console output formatting
├── vcf_explorer_visualiser.py      # Plot generation
├── data/
│   ├── raw/                        # Place VCF files here
│   └── processed/                  # Output files written here
├── tests/                          # Unit testing
├── conftest.py                     # pytest root marker
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.11+
- See `requirements.txt` for dependencies

---

## Installation

```bash
git clone https://github.com/ions0/vcf_explorer.git
cd vcf_explorer
pip install -r requirements.txt
```

### Options

| Flag | Description |
|------|-------------|
| `--vcf` | Path to VCF file (required) |
| `--output` | Output directory (default: `data/processed/`) |
| `--version` | Show version number |
| `--help` | Show help message |

### Example

```bash
# Basic run with auto-detected format
python vcf_explorer.py --vcf data/raw/CEU.chr22.vcf

# Specify output directory
python vcf_explorer.py --vcf data/raw/CEU.chr22.vcf --output results/
```

---

## Output

Each run creates a timestamped folder inside the output directory containing:

```
├── processed/
│   └── CEU.chr22_20260414_100647/
│       ├── visualisations/
│       │   └── *.png
│       └── logs/
│            └── vcf_explorer_20260414_100647.log
```
---

## Limitations

- Only uncompressed .vcf files are supported — .vcf.gz and .bcf are not.
- Assumes a single chromosome per file — multi-chromosome VCFs will produce misleading density plots.
- INFO and FORMAT fields are not parsed — loaded as raw strings only.
- Sample-level genotype data is not analysed.
- Window size and step size can only be changed by editing config.py directly.

---

## Version History

- **1.0.0** (19/04/2026): Initial public release

---

## Future Improvements

- [ ] **Extend argument options** — Add `--no-display` to suppress plot windows, `--window-size` and `--step-size` to override config values from the CLI
- [ ] **Config file support** — Allow analysis parameters (window size, step size, size bins) to be set via a YAML file instead of editing `config.py` directly
- [ ] **Compressed/indexed VCF support** — Add `.vcf.gz` and `.bcf` support via `pysam` or `cyvcf2`
- [ ] **INFO field parsing** — Parse structured data from the INFO column (allele frequency, depth, etc)
- [ ] **Sample-level analysis** — Use FORMAT and sample columns to calculate genotype stats like heterozygosity rates and per-sample missing data.
- [ ] **Testing coverage** — Expand unit tests with edge cases and value assertions
- [ ] **HTML report output** — Generate a self-contained HTML report bundling plots and stats table for easier sharing

---

## Author

Jared Cambridge - April 2026


