# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
from collections import defaultdict

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.repo

description = "get information about package maintainers"
section = "developer"
level = "long"


def setup_parser(subparser):
    maintained_group = subparser.add_mutually_exclusive_group()
    maintained_group.add_argument(
        "--maintained",
        action="store_true",
        default=False,
        help="show names of maintained packages",
    )

    maintained_group.add_argument(
        "--unmaintained",
        action="store_true",
        default=False,
        help="show names of unmaintained packages",
    )

    subparser.add_argument(
        "-a", "--all", action="store_true", default=False, help="show maintainers for all packages"
    )

    subparser.add_argument(
        "--by-user",
        action="store_true",
        default=False,
        help="show packages for users instead of users for packages",
    )

    # options for commands that take package arguments
    subparser.add_argument(
        "package_or_user",
        nargs=argparse.REMAINDER,
        help="names of packages or users to get info for",
    )


def packages_to_maintainers(package_names=None):
    if not package_names:
        package_names = spack.repo.PATH.all_package_names()

    pkg_to_users = defaultdict(lambda: set())
    for name in package_names:
        cls = spack.repo.PATH.get_pkg_class(name)
        for user in cls.maintainers:
            pkg_to_users[name].add(user)

    return pkg_to_users


def maintainers_to_packages(users=None):
    user_to_pkgs = defaultdict(lambda: [])
    for name in spack.repo.PATH.all_package_names():
        cls = spack.repo.PATH.get_pkg_class(name)
        for user in cls.maintainers:
            lower_users = [u.lower() for u in users]
            if not users or user.lower() in lower_users:
                user_to_pkgs[user].append(cls.name)

    return user_to_pkgs


def maintained_packages():
    maintained = []
    unmaintained = []
    for name in spack.repo.PATH.all_package_names():
        cls = spack.repo.PATH.get_pkg_class(name)
        if cls.maintainers:
            maintained.append(name)
        else:
            unmaintained.append(name)

    return maintained, unmaintained


def union_values(dictionary):
    """Given a dictionary with values that are Collections, return their union.

    Arguments:
        dictionary (dict): dictionary whose values are all collections.

    Return:
        (set): the union of all collections in the dictionary's values.
    """
    sets = [set(p) for p in dictionary.values()]
    return sorted(set.union(*sets)) if sets else set()


def maintainers(parser, args):
    if args.maintained or args.unmaintained:
        maintained, unmaintained = maintained_packages()
        pkgs = maintained if args.maintained else unmaintained
        colify(pkgs)
        return 0 if pkgs else 1

    if args.all:
        if args.by_user:
            maintainers = maintainers_to_packages(args.package_or_user)
            for user, packages in sorted(maintainers.items()):
                color.cprint("@c{%s}: %s" % (user, ", ".join(sorted(packages))))
            return 0 if maintainers else 1

        else:
            packages = packages_to_maintainers(args.package_or_user)
            for pkg, maintainers in sorted(packages.items()):
                color.cprint("@c{%s}: %s" % (pkg, ", ".join(sorted(maintainers))))
            return 0 if packages else 1

    if args.by_user:
        if not args.package_or_user:
            tty.die("spack maintainers --by-user requires a user or --all")

        packages = union_values(maintainers_to_packages(args.package_or_user))
        colify(packages)
        return 0 if packages else 1

    else:
        if not args.package_or_user:
            tty.die("spack maintainers requires a package or --all")

        users = union_values(packages_to_maintainers(args.package_or_user))
        colify(users)
        return 0 if users else 1
