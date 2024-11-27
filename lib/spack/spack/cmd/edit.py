# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import glob
import os

import llnl.util.tty as tty

import spack.cmd
import spack.paths
import spack.repo
import spack.util.editor

description = "open package files in $EDITOR"
section = "packaging"
level = "short"


def setup_parser(subparser):
    excl_args = subparser.add_mutually_exclusive_group()

    # Various types of Spack files that can be edited
    # Edits package files by default
    excl_args.add_argument(
        "-b",
        "--build-system",
        dest="path",
        action="store_const",
        const=spack.paths.build_systems_path,
        help="edit the build system with the supplied name",
    )
    excl_args.add_argument(
        "-c",
        "--command",
        dest="path",
        action="store_const",
        const=spack.paths.command_path,
        help="edit the command with the supplied name",
    )
    excl_args.add_argument(
        "-d",
        "--docs",
        dest="path",
        action="store_const",
        const=os.path.join(spack.paths.lib_path, "docs"),
        help="edit the docs with the supplied name",
    )
    excl_args.add_argument(
        "-t",
        "--test",
        dest="path",
        action="store_const",
        const=spack.paths.test_path,
        help="edit the test with the supplied name",
    )
    excl_args.add_argument(
        "-m",
        "--module",
        dest="path",
        action="store_const",
        const=spack.paths.module_path,
        help="edit the main spack module with the supplied name",
    )

    # Options for editing packages
    excl_args.add_argument("-r", "--repo", default=None, help="path to repo to edit package in")
    excl_args.add_argument("-N", "--namespace", default=None, help="namespace of package to edit")

    subparser.add_argument("package", nargs="*", default=None, help="package name")


def locate_package(name: str, repo: spack.repo.Repo) -> str:
    path = repo.filename_for_package_name(name)

    try:
        with open(path, "r"):
            return path
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise spack.repo.UnknownPackageError(name) from e
        tty.die(f"Cannot edit package: {e}")


def locate_file(name: str, path: str) -> str:
    # convert command names to python module name
    if path == spack.paths.command_path:
        name = spack.cmd.python_name(name)

    file_path = os.path.join(path, name)

    # Try to open direct match.
    try:
        with open(file_path, "r"):
            return file_path
    except OSError as e:
        if e.errno != errno.ENOENT:
            tty.die(f"Cannot edit file: {e}")
        pass

    # Otherwise try to find a file that starts with the name
    candidates = glob.glob(file_path + "*")
    exclude_list = [".pyc", "~"]  # exclude binaries and backups
    files = [f for f in candidates if not any(f.endswith(ext) for ext in exclude_list)]
    if len(files) > 1:
        tty.die(
            f"Multiple files start with `{name}`:\n"
            + "\n".join(f"        {os.path.basename(f)}" for f in files)
        )
    elif not files:
        tty.die(f"No file for '{name}' was found in {path}")
    return files[0]


def edit(parser, args):
    names = args.package

    # If `--command`, `--test`, or `--module` is chosen, edit those instead
    if args.path:
        paths = [locate_file(name, args.path) for name in names] if names else [args.path]
        spack.util.editor.editor(*paths)
    elif names:
        if args.repo:
            repo = spack.repo.from_path(args.repo)
        elif args.namespace:
            repo = spack.repo.PATH.get_repo(args.namespace)
        else:
            repo = spack.repo.PATH
        paths = [locate_package(name, repo) for name in names]
        spack.util.editor.editor(*paths)
    else:
        # By default open the directory where packages live
        spack.util.editor.editor(spack.paths.packages_path)
