#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import log
import argparse
import signal
import sys
import pathlib

import keep_alive as ka


def script_main(shell: bool, script_name: str):
    path = pathlib.Path(script_name).absolute()
    sys.path.append(str(path.parent))
    script = __import__(path.stem)

    incubator = ka.Incubator(shell)
    for cl in script.commands():
        incubator.incubate(cl)
    signal_handler(incubator)
    incubator.monitor()


def target_main(shell: bool, target_command: str, count: int):
    incubator = ka.Incubator(shell)
    for i in range(count):
        incubator.incubate(target_command)
    signal_handler(incubator)
    incubator.monitor()


def signal_handler(incubator: ka.Incubator):
    def default_signal_handler(signal_, _):
        log.i(__name__, "Sent signal {0}".format(signal_))
        incubator.stop()
    signal.signal(signal.SIGINT, default_signal_handler)


if __name__ == '__main__':
    log.i(__name__, "Start QB Incubator")

    parser = argparse.ArgumentParser(
        prog="QB Process incubator",
        description="Incubate and manage processes.\nYou must set --script or --target",
        usage="SCRIPT [OPTIONS]...",
        add_help=True
    )

    parser.add_argument("-s", "--script", help="Incubate script", action="store", default=None)
    parser.add_argument("-t", "--target", help="Target script name", action="store", default=None)
    parser.add_argument("-c", "--target-count", help="Target instance count", action="store", type=int, default=1)
    parser.add_argument("--shell", help="Run command as shell mode", action="store_true", default=False)

    args = parser.parse_args()

    if args.script is None and args.target is None:
        log.e(__name__, "--script and --target are not set.")
        exit(1)

    if args.script is not None:
        script_main(args.shell, args.script)
    else:
        target_main(args.shell, args.target, args.count)
