"""
VCF Explorer: vcf_explorer_config.py

Configuration file for VCF Explorer
Contains paths and analysis parameters
"""
import logging
from pathlib import Path
from datetime import datetime

SCRIPT_PATH = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_PATH / "data"
DEFAULT_VCF_FILE = DATA_PATH / "raw" / "CEU.chr22.vcf"
FIGSIZE = (14, 10) 
VALID_EXTENSIONS = {".vcf"}
VERSION = "1.0.0"

WINDOW_SIZE = 5000
STEP_SIZE = 1000

def setup_output_directories(output_dir: Path) -> None:
    """
    Create the required output subdirectories for a run.

    Creates visualisations/ and logs/ subdirectories under the given output
    directory. Directories are created recursively and will not raise an error
    if they already exist.

    Args:
        output_dir (Path): Root output directory for the current run.

    Raises:
        RuntimeError: If any directory cannot be created due to an OS error.
    """

    directories = [
        output_dir / "visualisations",
        output_dir / "logs"
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create directory: {directory}") from e
    
    print("Output directories initialised")

def validate_config() -> None:
    """
    Validate analysis configuration parameters.

    Raises:
        ValueError: If WINDOW_SIZE or STEP_SIZE are non-positive, or if
            STEP_SIZE exceeds WINDOW_SIZE.
    """
    if WINDOW_SIZE <= 0 or STEP_SIZE <= 0:
        raise ValueError("WINDOW_SIZE and STEP_SIZE must be positive integers.")
    if STEP_SIZE > WINDOW_SIZE:
        raise ValueError("STEP_SIZE should not exceed WINDOW_SIZE.")

def setup_logging(log_dir: Path) -> None:
    """
    Configure file and console logging for a run.

    Creates a timestamped log file in the given directory and attaches both a
    file handler (DEBUG and above) and a console handler (INFO and above) to
    the root logger. Noisy third-party loggers (e.g. matplotlib) are silenced
    to WARNING level.

    Args:
        log_dir (Path): Directory where the log file will be written. Created
            if it does not already exist.
    """
    
    log_dir.mkdir(parents=True, exist_ok=True)    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"vcf_explorer_{timestamp}.log"

    LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(message)s]"
    formatter = logging.Formatter(LOG_FORMAT)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Silence noisy third-party libraries
    logging.getLogger('matplotlib').setLevel(logging.WARNING)