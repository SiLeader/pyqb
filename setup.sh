#!/bin/sh

set -e

/usr/bin/env python3 systemd/systemd_setup.py

cd systemd

for file in `ls | grep *-pyqb.service`;do
    echo "Link $file created."
    sudo ln -s `pwd`/$file /etc/systemd/system/$file
done
