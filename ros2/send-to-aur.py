import os
import subprocess

dirs = os.listdir(".")
for dir in dirs:
	if os.path.isfile(dir):
		continue
	os.chdir(dir)
	out = subprocess.check_output(["makepkg", "--printsrcinfo"])
	with open(".SRCINFO", 'w') as f:
		f.write(out.decode('utf-8'))
	subprocess.run(["git", "init"])
	subprocess.run(["git", "remote", "add", "origin", "ssh://aur@aur.archlinux.org/{}.git".format(dir)])
	subprocess.run(["git", "fetch"])
	subprocess.run(["git", "add", "PKGBUILD", ".SRCINFO"])
	subprocess.run(["git", "commit", "-m", "Fix"])
	subprocess.run(["git", "push", "-u", "origin", "master"])
	os.chdir("..")
