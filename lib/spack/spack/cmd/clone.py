# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, working_dir

import spack.paths
import spack.util.git
from spack.util.executable import ProcessError

_SPACK_UPSTREAM = "https://github.com/spack/spack"

description = "create a new installation of spack in another prefix"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-r",
        "--remote",
        action="store",
        dest="remote",
        help="name of the remote to clone from",
        default="origin",
    )
    subparser.add_argument("prefix", help="name of prefix where we should install spack")


def get_origin_info(remote):
    git_dir = os.path.join(spack.paths.prefix, ".git")
    git = spack.util.git.git(required=True)
    try:
        branch = git("symbolic-ref", "--short", "HEAD", output=str)
    except ProcessError:
        branch = "develop"
        tty.warn("No branch found; using default branch: %s" % branch)
    if remote == "origin" and branch not in ("master", "develop"):
        branch = "develop"
        tty.warn("Unknown branch found; using default branch: %s" % branch)
    try:
        origin_url = git(
            "--git-dir=%s" % git_dir, "config", "--get", "remote.%s.url" % remote, output=str
        )
    except ProcessError:
        origin_url = _SPACK_UPSTREAM
        tty.warn("No git repository found; using default upstream URL: %s" % origin_url)
    return (origin_url.strip(), branch.strip())


def clone(parser, args):
    origin_url, branch = get_origin_info(args.remote)
    prefix = args.prefix

    tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))

    if os.path.isfile(prefix):
        tty.die("There is already a file at %s" % prefix)

    mkdirp(prefix)

    if os.path.exists(os.path.join(prefix, ".git")):
        tty.die("There already seems to be a git repository in %s" % prefix)

    files_in_the_way = os.listdir(prefix)
    if files_in_the_way:
        tty.die(
            "There are already files there! Delete these files before boostrapping spack.",
            *files_in_the_way,
        )

    tty.msg("Installing:", "%s/bin/spack" % prefix, "%s/lib/spack/..." % prefix)

    with working_dir(prefix):
        git = spack.util.git.git(required=True)
        git("init", "--shared", "-q")
        git("remote", "add", "origin", origin_url)
        git("fetch", "origin", "%s:refs/remotes/origin/%s" % (branch, branch), "-n", "-q")
        git("reset", "--hard", "origin/%s" % branch, "-q")
        git("checkout", "-B", branch, "origin/%s" % branch, "-q")

        tty.msg(
            "Successfully created a new spack in %s" % prefix,
            "Run %s/bin/spack to use this installation." % prefix,
        )
