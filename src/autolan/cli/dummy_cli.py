"""Sub-command: `split`"""

import logging

from autolan.lib.cli import output_options, setup_cli


def command(opt):
    """Sub-command."""
    log = logging.getLogger(__name__)

    start_time, start_time_str = setup_cli(opt)

    log.info(f"Hello CLI! {opt.somevar}")


def options(subparsers):
    """Sub-command options."""
    parser_desc = "Dummy CLI tool."

    parser = subparsers.add_parser(
        "dummy-cli",
        help=parser_desc,
        description=parser_desc,
    )
    parser.set_defaults(func=command)

    # parser.add_argument(
    #     "test",
    #     type=str,
    #     metavar="PATH",
    #     help="input to path of pdf",
    # )

    parser.add_argument(
        "--somevar",
        required=False,
        type=int,
        help="some var",
        default=None,
    )

    output_options(parser)
