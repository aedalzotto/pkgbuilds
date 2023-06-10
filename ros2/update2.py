#!/usr/bin/env python3
from argparse import ArgumentParser
from os import listdir, chdir
from os.path import isdir
from re import compile as re_compile
from subprocess import check_output, run

def update():
    dirs = filter(isdir, listdir('.'))
    pkgbuilds = list(dirs)

    for pkgbuild in pkgbuilds:
        chdir(pkgbuild)
        print(pkgbuild)
        srcinfo = check_output(["makepkg", "--printsrcinfo"]).decode('utf-8')
        with open(".SRCINFO", 'w') as f:
            f.write(srcinfo)

        run(["git", "add", "PKGBUILD", ".SRCINFO"])
        run(["git", "commit", "-m", "update build"])
        run(["git", "push"])

        chdir('../')


if __name__ == "__main__":
    update()
