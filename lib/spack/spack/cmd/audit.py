# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import warnings

import llnl.util.tty as tty
import llnl.util.tty.colify
import llnl.util.tty.color as cl

import spack.audit
import spack.repo

description = "audit configuration files, packages, etc."
section = "system"
level = "short"


def setup_parser(subparser):
    # Top level flags, valid for every audit class
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="subcommand")

    # Audit configuration files
    sp.add_parser("configs", help="audit configuration files")

    # Audit package recipes
    external_parser = sp.add_parser("externals", help="check external detection in packages")
    external_parser.add_argument(
        "--list",
        action="store_true",
        dest="list_externals",
        help="if passed, list which packages have detection tests",
    )

    # Https and other linting
    https_parser = sp.add_parser("packages-https", help="check https in packages")
    https_parser.add_argument(
        "--all", action="store_true", default=False, dest="check_all", help="audit all packages"
    )

    # Audit package recipes
    pkg_parser = sp.add_parser("packages", help="audit package recipes")

    for group in [pkg_parser, https_parser, external_parser]:
        group.add_argument(
            "name",
            metavar="PKG",
            nargs="*",
            help="package to be analyzed (if none all packages will be processed)",
        )

    # List all checks
    sp.add_parser("list", help="list available checks and exits")


def configs(parser, args):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        reports = spack.audit.run_group(args.subcommand)
        _process_reports(reports)


def packages(parser, args):
    pkgs = args.name or spack.repo.PATH.all_package_names()
    reports = spack.audit.run_group(args.subcommand, pkgs=pkgs)
    _process_reports(reports)


def packages_https(parser, args):
    # Since packages takes a long time, --all is required without name
    if not args.check_all and not args.name:
        tty.die("Please specify one or more packages to audit, or --all.")

    pkgs = args.name or spack.repo.PATH.all_package_names()
    reports = spack.audit.run_group(args.subcommand, pkgs=pkgs)
    _process_reports(reports)


def externals(parser, args):
    if args.list_externals:
        msg = "@*{The following packages have detection tests:}"
        tty.msg(cl.colorize(msg))
        llnl.util.tty.colify.colify(spack.audit.packages_with_detection_tests(), indent=2)
        return

    pkgs = args.name or spack.repo.PATH.all_package_names()
    reports = spack.audit.run_group(args.subcommand, pkgs=pkgs, debug_log=tty.debug)
    _process_reports(reports)


def list(parser, args):
    for subcommand, check_tags in spack.audit.GROUPS.items():
        print(cl.colorize("@*b{" + subcommand + "}:"))
        for tag in check_tags:
            audit_obj = spack.audit.CALLBACKS[tag]
            print("  " + audit_obj.description)
            if args.verbose:
                for idx, fn in enumerate(audit_obj.callbacks):
                    print("    {0}. ".format(idx + 1) + fn.__doc__)
                print()
        print()


def audit(parser, args):
    subcommands = {
        "configs": configs,
        "externals": externals,
        "packages": packages,
        "packages-https": packages_https,
        "list": list,
    }
    subcommands[args.subcommand](parser, args)


def _process_reports(reports):
    for check, errors in reports:
        if errors:
            status = f"{len(errors)} issue{'' if len(errors) == 1 else 's'} found"
            print(cl.colorize(f"{check}: @*r{{{status}}}"))
            numdigits = len(str(len(errors)))
            for idx, error in enumerate(errors):
                print(f"{idx + 1:>{numdigits}}. {error}")
            raise SystemExit(1)
        else:
            print(cl.colorize(f"{check}: @*g{{passed}}"))
