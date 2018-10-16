#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Copyright 2018 SiLeader and Cerussite.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


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

    while True:
        user = input("User (Required) >>> ")
        if len(user) > 0:
            break

    while True:
        group = input("Group (Required) >>> ")
        if len(group) > 0:
            break

    while True:
        log_path = input("Log file path (Required) >>> ")
        if len(log_path) > 0:
            break

    file_dir = str(pathlib.Path(__file__).absolute().parent)
    with open("{}/pyqb.service.skeleton".format(file_dir)) as pss_fp:
        service = pss_fp.read()
        service = service.replace("${TARGET}", target).replace("${PYQB_LOCATION}", pyqb_location)
        service = service.replace("${COMMAND_SCRIPT_LOCATION}", command_script)
        service = service.replace("${SOCKET_NAME}", socket_name)
        service = service.replace("${USER}", user)
        service = service.replace("${GROUP}", group)

        with open("{}/{}-pyqb.service".format(file_dir, target), "w") as pfp:
            pfp.write(service)

    with open("{}/rsyslog.conf.skeleton".format(file_dir)) as rcs_fp:
        conf = rcs_fp.read()
        conf = conf.replace("${NAME}", target)
        conf = conf.replace("${LOG_PATH}", log_path)

        with open("{}/{}-pyqb.conf".replace(file_dir, target), "w") as pfp:
            pfp.write(conf)


if __name__ == '__main__':
    main()
