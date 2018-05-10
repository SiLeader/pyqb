#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import log
import argparse
import signal
import sys
import pathlib
import socket
import threading
import os

import keep_alive as ka


def script_main(shell: bool, script_name: str, sock_file=None):
    path = pathlib.Path(script_name).absolute()
    sys.path.append(str(path.parent))
    script = __import__(path.stem)

    incubator = ka.Incubator(shell)
    for cl in script.commands():
        incubator.incubate(cl)
    signal_handler(incubator)
    if sock_file is not None:
        threading.Thread(target=lambda: socket_incubator(sock_file, incubator)).start()
    incubator.monitor()


def target_main(shell: bool, target_command: str, count: int, sock_file=None):
    incubator = ka.Incubator(shell)
    for i in range(count):
        incubator.incubate(target_command)
    signal_handler(incubator)
    if sock_file is not None:
        threading.Thread(target=lambda: socket_incubator(sock_file, incubator)).start()
    incubator.monitor()


def socket_incubator(sock_file: str, incubator: ka.Incubator, sock_type=socket.AF_UNIX):
    sock = socket.socket(sock_type, socket.SOCK_STREAM)
    sock.bind(sock_file)
    sock.listen()

    try:
        while True:
            conn, addr = sock.accept()
            try:
                while True:
                    data = conn.recv(1024)
                    incubator.incubate(data)
                    conn.send("OK")
            finally:
                conn.close()
    finally:
        os.remove(sock_file)


def signal_handler(incubator: ka.Incubator):
    def default_signal_handler(signal_, _):
        log.i(__name__, "Receive signal {0}".format(signal_))
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
    parser.add_argument("--socket", help="Unix domain socket path", action="store", default=None)

    args = parser.parse_args()

    if args.script is None and args.target is None:
        log.e(__name__, "--script and --target are not set.")
        exit(1)

    if args.script is not None:
        script_main(args.shell, args.script, args.socket)
    else:
        target_main(args.shell, args.target, args.count, args.socket)