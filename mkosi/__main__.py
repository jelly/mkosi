# SPDX-License-Identifier: LGPL-2.1+
# PYTHON_ARGCOMPLETE_OK

import contextlib
import os
import subprocess
import sys
from collections.abc import Iterator

from mkosi import load_args, run_verb
from mkosi.config import MkosiConfigParser
from mkosi.log import ARG_DEBUG, MkosiPrinter, die
from mkosi.run import excepthook


@contextlib.contextmanager
def propagate_failed_return() -> Iterator[None]:
    try:
        yield
    except SystemExit as e:
        if ARG_DEBUG:
            raise e

        sys.exit(e.code)
    except KeyboardInterrupt as e:
        if ARG_DEBUG:
            raise e

        MkosiPrinter.error("Interrupted")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        if ARG_DEBUG:
            raise e

        # We always log when subprocess.CalledProcessError is raised, so we don't log again here.
        sys.exit(e.returncode)
    except Exception as e:
        if ARG_DEBUG:
            raise e

        MkosiPrinter.error(f"Error: {str(e)}, rerun mkosi with --debug run to get more information")
        sys.exit(1)


@propagate_failed_return()
def main() -> None:
    args = MkosiConfigParser().parse()

    if args.directory:
        if args.directory.is_dir():
            os.chdir(args.directory)
        else:
            die(f"Error: {args.directory} is not a directory!")

    run_verb(load_args(args))


if __name__ == "__main__":
    sys.excepthook = excepthook
    main()
