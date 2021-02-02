# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import glob

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.deployment as deployment
import spack.paths
import spack.repo
from spack.spec import Spec
from spack.util.editor import editor

description = "open package files in $EDITOR"
section = "packaging"
level = "short"


def edit_package(name, repo_path, namespace):
    """Opens the requested package file in your favorite $EDITOR.

    Args:
        name (str): The name of the package
        repo_path (str): The path to the repository containing this package
        namespace (str): A valid namespace registered with Spack
    """
    # Find the location of the package
    if repo_path:
        repo = spack.repo.Repo(repo_path)
    elif namespace:
        repo = spack.repo.path.get_repo(namespace)
    else:
        repo = spack.repo.path
    path = repo.filename_for_package_name(name)

    spec = Spec(name)
    if os.path.exists(path):
        if not os.path.isfile(path):
            tty.die("Something is wrong. '{0}' is not a file!".format(path))
        if not os.access(path, os.R_OK):
            tty.die("Insufficient permissions on '%s'!" % path)
    else:
        tty.die("No package for '{0}' was found.".format(spec.name),
                "  Use `spack create` to create a new package")

    editor(path)


def setup_parser(subparser):
    excl_args = subparser.add_mutually_exclusive_group()

    # Various types of Spack files that can be edited
    # Edits package files by default
    excl_args.add_argument(
        '-b', '--build-system', dest='path', action='store_const',
        const=spack.paths.build_systems_path,
        help="Edit the build system with the supplied name.")
    excl_args.add_argument(
        '-c', '--command', dest='path', action='store_const',
        const=spack.paths.command_path,
        help="edit the command with the supplied name")
    excl_args.add_argument(
        '-d', '--docs', dest='path', action='store_const',
        const=os.path.join(spack.paths.lib_path, 'docs'),
        help="edit the docs with the supplied name")
    excl_args.add_argument(
        '-t', '--test', dest='path', action='store_const',
        const=spack.paths.test_path,
        help="edit the test with the supplied name")
    excl_args.add_argument(
        '-m', '--module', dest='path', action='store_const',
        const=spack.paths.module_path,
        help="edit the main spack module with the supplied name")

    # Options for editing packages
    excl_args.add_argument(
        '-r', '--repo', default=None,
        help="path to repo to edit package in")
    excl_args.add_argument(
        '-N', '--namespace', default=None,
        help="namespace of package to edit")

    subparser.add_argument(
        'package', nargs='?', default=None, help="package name")


def edit(parser, args):
    deployment.die_if_deployment('edit')

    name = args.package

    # By default, edit package files
    path = spack.paths.packages_path

    # If `--command`, `--test`, or `--module` is chosen, edit those instead
    if args.path:
        path = args.path
        if name:
            # convert command names to python module name
            if path == spack.paths.command_path:
                name = spack.cmd.python_name(name)

            path = os.path.join(path, name)
            if not os.path.exists(path):
                files = glob.glob(path + '*')
                blacklist = ['.pyc', '~']  # blacklist binaries and backups
                files = list(filter(
                    lambda x: all(s not in x for s in blacklist), files))
                if len(files) > 1:
                    m = 'Multiple files exist with the name {0}.'.format(name)
                    m += ' Please specify a suffix. Files are:\n\n'
                    for f in files:
                        m += '        ' + os.path.basename(f) + '\n'
                    tty.die(m)
                if not files:
                    tty.die("No file for '{0}' was found in {1}".format(name,
                                                                        path))
                path = files[0]  # already confirmed only one entry in files

        editor(path)
    elif name:
        edit_package(name, args.repo, args.namespace)
    else:
        # By default open the directory where packages live
        editor(path)
