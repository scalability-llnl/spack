# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
import sys
from datetime import datetime
from glob import glob

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack
import spack.paths
import spack.platforms
import spack.spec
import spack.store
import spack.util.git
from spack.util.executable import which

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="debug_command")
    sp.add_parser("create-db-tarball", help="create a tarball of Spack's installation metadata")
    sp.add_parser("report", help="print information useful for bug reports")


def _debug_tarball_suffix():
    now = datetime.now()
    suffix = now.strftime("%Y-%m-%d-%H%M%S")

    git = spack.util.git.git()
    if not git:
        return "nobranch-nogit-%s" % suffix

    with working_dir(spack.paths.prefix):
        if not os.path.isdir(".git"):
            return "nobranch.nogit.%s" % suffix

        # Get symbolic branch name and strip any special chars (mainly '/')
        symbolic = git("rev-parse", "--abbrev-ref", "--short", "HEAD", output=str).strip()
        symbolic = re.sub(r"[^\w.-]", "-", symbolic)

        # Get the commit hash too.
        commit = git("rev-parse", "--short", "HEAD", output=str).strip()

        if symbolic == commit:
            return "nobranch.%s.%s" % (commit, suffix)
        else:
            return "%s.%s.%s" % (symbolic, commit, suffix)


def create_db_tarball(args):
    tar = which("tar")
    tarball_name = "spack-db.%s.tar.gz" % _debug_tarball_suffix()
    tarball_path = os.path.abspath(tarball_name)

    base = os.path.basename(str(spack.store.STORE.root))
    transform_args = []
    # Currently --transform and -s are not supported by Windows native tar
    if "GNU" in tar("--version", output=str):
        transform_args = ["--transform", "s/^%s/%s/" % (base, tarball_name)]
    elif sys.platform != "win32":
        transform_args = ["-s", "/^%s/%s/" % (base, tarball_name)]

    wd = os.path.dirname(str(spack.store.STORE.root))
    with working_dir(wd):
        files = [spack.store.STORE.db._index_path]
        files += glob("%s/*/*/*/.spack/spec.json" % base)
        files += glob("%s/*/*/*/.spack/spec.yaml" % base)
        files = [os.path.relpath(f) for f in files]

        args = ["-czf", tarball_path]
        args += transform_args
        args += files
        tar(*args)

    tty.msg("Created %s" % tarball_name)


def report(args):
    host_platform = spack.platforms.host()
    host_os = host_platform.operating_system("frontend")
    host_target = host_platform.target("frontend")
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))
    print("* **Spack:**", spack.get_version())
    print("* **Python:**", platform.python_version())
    print("* **Platform:**", architecture)


def debug(parser, args):
    action = {"create-db-tarball": create_db_tarball, "report": report}
    action[args.debug_command](args)
