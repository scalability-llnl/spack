# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys
from argparse import ArgumentParser, Namespace
from typing import Dict, List

from llnl.util import tty
from llnl.util.filesystem import working_dir
from llnl.util.tty.colify import colify

import spack.cmd
import spack.util.git
from spack.cmd import spack_is_git_repo

description = "update the spack repository to the latest commit"
section = "system"
level = "short"


def setup_parser(subparser: ArgumentParser) -> None:
    subparser.add_argument("-b", "--branch", help="name of the branch to upate the repository to")


def update(parser: ArgumentParser, args: Namespace) -> None:
    # make sure that spack is a git repository
    if not spack_is_git_repo():
        tty.die("This spack is not a git clone. Can't use 'spack update'")

    git = spack.util.git.git()
    if git is None:
        tty.die("Couldn't find a usable git executable in PATH. Unable to update.")

    # execute git within the spack repository
    with working_dir(spack.paths.prefix):
        checked_out_ref = git("symbolic-ref", "-q", "HEAD", output=str)
        current_branch = checked_out_ref.replace("refs/heads/", "", 1)

        # provide a warning if the user did not specify a branch
        # and spack's repository is not tracking upstream develop
        if args.branch is None:
            upstream_branch = None

            refs = git("for-each-ref", "--format=%(refname)", "refs/heads/", output=str)
            for ref in refs.split():
                branch = ref.replace("refs/heads/", "", 1)
                branch_remote_ref = git("config", f"branch.{branch}.merge", output=str)

                if branch_remote_ref.strip().endswith("develop"):
                    remote = git("config", f"branch.{branch}.remote", output=str).strip()
                    remote_url = git("config", f"remote.{remote}.url", output=str).strip()

                    if re.match(r"spack\/spack(\.git)?$", remote_url):
                        upstream_branch = branch
                        break

            if upstream_branch is not None and current_branch != upstream_branch:
                tty.warn("Spack is not tracking upstream develop.")
                tty.warn("Packages may be out of date. To switch to develop run,")
                print()
                print(f"    spack update -b {upstream_branch}")
                print()

        elif args.branch != current_branch:
            git("checkout", args.branch)

        # record commit hash before pull
        old_head = git("rev-parse", "HEAD", output=str).strip()

        # perform a git pull to update the repository
        git("pull", "--rebase", "-n")

        # record commit hash after pull
        new_head = git("rev-parse", "HEAD", output=str).strip()

        # check to see if the repository updated
        if old_head != new_head:
            changed_files = git(
                "diff-tree", "-r", "--name-status", f"{old_head}..{new_head}", output=str
            )
            changed_packages: Dict[str, List] = {"Added": [], "Updated": [], "Deleted": []}

            for file in changed_files.split("\n"):
                if file.endswith("package.py"):
                    result = re.search("var/spack/repos/builtin/packages/(.*)/package.py", file)
                    if result is None:
                        continue
                    pkg = result.group(1)
                    if file[0] == "A":
                        changed_packages["Added"].append(pkg)
                    elif file[0] == "M":
                        changed_packages["Updated"].append(pkg)
                    elif file[0] == "D":
                        changed_packages["Deleted"].append(pkg)

            for action, pkgs in changed_packages.items():
                if len(pkgs) > 0:
                    tty.msg(f"{action} %d packages" % len(pkgs))
                    colify(pkgs, output=sys.stdout)
