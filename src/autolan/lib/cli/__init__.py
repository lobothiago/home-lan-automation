import os
import sys
from datetime import datetime, timezone
from typing import Optional

from autolan.lib.cli.env_default import EnvDefault
from autolan.lib.cli.log_options import log_options
from autolan.lib.cli.output_options import output_options
from autolan.lib.io import sniff_local
from autolan.lib.logging import setup_logging

__all__ = [
    "EnvDefault",
    "log_options",
    "output_options",
]


def setup_cli(opt):
    """Initialize CLI runtime including logging based on CLI options.

    Args:
        opt: Selected CLI options.

    Returns:
        Tuple of start time and start time string.

    """
    start_time = datetime.now(timezone.utc)
    start_time_str = start_time.strftime("%Y-%m-%d--%H-%M-%S")
    setup_logging(opt, start_time_str)
    return (start_time, start_time_str)


def verify_src_path(desc: str, src_path: str):
    """Determines if input/source path is valid - errors and exits if not.

    For local paths, confirms that file exists.

    Args:
        desc: Brief description of input/source.
        src_path: Path to input/source to verify.

    """
    if src_path:
        if sniff_local(src_path):
            if not os.path.exists(src_path):
                print("{desc} {src_path} does not exist.")
                sys.exit(1)


def setup_dest_path(
    opt, result_id: str, result_prefix: str = "result", result_ext: str = "json"
) -> Optional[str]:
    """Determines CLI output path based on CLI options.

    If `--dest_prefix`, output pattern is:

        {opt.dest_prefix}/{result_prefix}-{result_id}.{result_ext}

    Args:
        opt: Selected CLI options.
        result_id: If `--dest_prefix`, base name of output file.
        result_prefix: If `--dest_prefix`, prefix to output file.
        result_ext: If `--dest_prefix`, output file extension.

    Returns:
        URI to use for output or None if `--stdout`.

    """
    result_path: Optional[str] = None

    if opt.stdout:
        pass
    elif opt.dest_uri:
        result_path = opt.dest_uri
    else:
        result_path = os.path.join(
            opt.dest_prefix, f"{result_prefix}-{result_id}.{result_ext}"
        )
        # if local, create directory if it doesn't exist
        if sniff_local(opt.dest_prefix):
            if not os.path.exists(opt.dest_prefix):
                os.makedirs(opt.dest_prefix, exist_ok=True)
            elif not os.path.isdir(opt.dest_prefix):
                print("bad dest prefix - already exists, not a directory")
                sys.exit(1)

    return result_path
