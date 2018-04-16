#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep


if __name__ == '__main__':  # .format(sys.argv[0])
    with open("/Users/sileader/PycharmProjects/Qb/test/files/12.txt", "w") as fp:
        num = 0
        while True:
            fp.write("{} ".format(num))
            num += 1
            if num > 10:
                num = 0
                fp.write("\n")
            sleep(2)
