#!/usr/bin/env python3
from argparse import ArgumentParser
from os import listdir, chdir
from os.path import isdir
from re import compile as re_compile
from subprocess import check_output, run

def update(repo, version, release, commit):
    dirs = filter(isdir, listdir('.'))
    pkgbuilds = []

    for pkg in dirs:
        with open("{}/PKGBUILD".format(pkg)) as pkgbuild:
            if repo in pkgbuild.read():
                pkgbuilds.append(pkg)

    for pkgbuild in pkgbuilds:
        chdir(pkgbuild)
        run(["sed", "-i", "s/pkgver=.*/pkgver={}/g".format(version), "PKGBUILD"])
        run(["sed", "-i", "s/pkgrel=.*/pkgrel={}/g".format(release), "PKGBUILD"])
        run(["updpkgsums"])
        srcinfo = check_output(["makepkg", "--printsrcinfo"]).decode('utf-8')
        with open(".SRCINFO", 'w') as f:
            f.write(srcinfo)

        if commit:
            run(["git", "add", "PKGBUILD", ".SRCINFO"])
            run(["git", "commit", "-m", "update to {}-{}".format(version, release)])
            run(["git", "push"])

        chdir('../')


if __name__ == "__main__":
    parser = ArgumentParser(description="Update multiple repos")
    parser.add_argument("repo", help="Repository to find in PKGBUILD to update")
    parser.add_argument("pkgver", help="New version to set")
    parser.add_argument("pkgrel", help="New release to set")
    parser.add_argument("--commit", action="store_true", help="Commit to AUR")
    args = parser.parse_args()

    update(args.repo, args.pkgver, args.pkgrel, args.commit)
