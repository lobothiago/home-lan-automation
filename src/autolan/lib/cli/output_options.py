import argparse


def output_options(parser: argparse.ArgumentParser):
    """Adds standard destination output options to `parser`.

    * **`--dest_prefix`** write output to a directory/prefix.
    * **`--dest_uri`** write output to a specific file/resource.
    * **`--stdout`** write all output to stdout.

    All are mutually exclusive.

    Args:
        parser: To add options to.

    """
    outputs = parser.add_mutually_exclusive_group()
    outputs.add_argument(
        "--dest_prefix",
        type=str,
        default="local-data",
        metavar="PREFIX",
        help="output path prefix",
    )
    outputs.add_argument(
        "--dest_uri",
        type=str,
        default=None,
        metavar="URI",
        help="full output path",
    )
    outputs.add_argument("--stdout", action="store_true", help="output to 'stdout'")
