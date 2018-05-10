#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib


def main():
    while True:
        target = input("PyQB Target name (Required) >>> ")
        if len(target) > 0:
            break

    pyqb_location = input("PyQB Location [{}] >>> ".format(pathlib.Path.cwd()))
    if len(pyqb_location) <= 0:
        pyqb_location = str(pathlib.Path.cwd())

    while True:
        command_script = input("Command script location (Required) >>> ")
        if len(command_script) > 0:
            break

    socket_name = input("Socket name [pyqb] >>> ")
    if len(socket_name) <= 0:
        socket_name = "pyqb"

    file_dir = str(pathlib.Path(__file__).absolute().parent)
    with open("{}/pyqb.service.skeleton".format(file_dir)) as pss_fp:
        service = pss_fp.read()
        service = service.replace("${TARGET}", target).replace("${PYQB_LOCATION}", pyqb_location)
        service = service.replace("${COMMAND_SCRIPT_LOCATION}", command_script).replace("${SOCKET_NAME}", socket_name)

        with open("{}/{}-pyqb.service".format(file_dir, target), "w") as pfp:
            pfp.write(service)


if __name__ == '__main__':
    main()
