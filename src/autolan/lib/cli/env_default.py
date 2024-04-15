import argparse
import os


class EnvDefault(argparse.Action):
    """Environment variable setter action.

    Sets an `argparse` option value to the value of an environment variable if
    that option does not otherwise already have a value.

    """

    def __init__(self, envvar: str, required=True, default=None, **kwargs):
        """Constructor.

        Args:
            envvar: Environment variable name.

        """
        if envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
                if default and isinstance(default, str):
                    default = default.strip()
            if required and default is not None:
                required = False
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
