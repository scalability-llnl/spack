# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack.repo

description = "list downloadable resources (tarballs, repos, patches, etc.)"
section = "basic"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="resource_command")

    list_parser = sp.add_parser("list", help=resource_list.__doc__)
    list_parser.add_argument(
        "--only-hashes", action="store_true", help="only print sha256 hashes of resources"
    )

    show_parser = sp.add_parser("show", help=resource_show.__doc__)
    show_parser.add_argument("hash", action="store")


def _show_patch(sha256):
    """Show a record from the patch index."""
    patches = spack.repo.PATH.patch_index.index
    data = patches.get(sha256)

    if not data:
        candidates = [k for k in patches if k.startswith(sha256)]
        if not candidates:
            tty.die("no such resource: %s" % sha256)
        elif len(candidates) > 1:
            tty.die("%s: ambiguous hash prefix. Options are:", *candidates)

        sha256 = candidates[0]
        data = patches.get(sha256)

    color.cprint("@c{%s}" % sha256)
    for package, rec in data.items():
        owner = rec["owner"]

        if "relative_path" in rec:
            pkg_dir = spack.repo.PATH.get_pkg_class(owner).package_dir
            path = os.path.join(pkg_dir, rec["relative_path"])
            print("    path:       %s" % path)
        else:
            print("    url:        %s" % rec["url"])

        print("    applies to: %s" % package)
        if owner != package:
            print("    patched by: %s" % owner)


def resource_list(args):
    """list all resources known to spack (currently just patches)"""
    patches = spack.repo.PATH.patch_index.index
    for sha256 in patches:
        if args.only_hashes:
            print(sha256)
        else:
            _show_patch(sha256)


def resource_show(args):
    """show a resource, identified by its checksum"""
    _show_patch(args.hash)


def resource(parser, args):
    action = {"list": resource_list, "show": resource_show}
    action[args.resource_command](args)
