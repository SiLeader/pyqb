#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, List
import time
import subprocess
import log


class Incubator:
    def __init__(self, shell: bool):
        self.__shell = shell
        self.__processes = []
        self.__processes_appended = []
        self.__running = True

    def monitor(self):
        while self.__running:
            args = None
            for process in self.__processes:
                code = process.poll()
                if code is not None and code != 0:
                    log.w(__name__, "Process is dead. PID={0} code={1}".format(process.pid, process.returncode))
                    args = process.args
                    self.__processes.remove(process)
                    break
                time.sleep(1)
            if args is not None:
                self.incubate(args)

            self.__processes.extend(self.__processes_appended)
            self.__processes_appended.clear()

    def incubate(self, cmdline: Union[List[str], str]):
        if isinstance(cmdline, str):
            cmdline = cmdline.split(" ")
        process = subprocess.Popen(
            cmdline,
            shell=self.__shell,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        log.i(__name__, "Incubated process. PID={}".format(process.pid))
        self.__processes_appended.append(process)

    def stop(self):
        self.__running = False
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(5)
            except subprocess.TimeoutExpired:
                log.w(__name__, "Terminate process PID={} is failed (5 seconds waited). kill this process.".format(
                    process.pid))
                process.kill()
                process.wait()

    @property
    def processes(self):
        return self.__processes
