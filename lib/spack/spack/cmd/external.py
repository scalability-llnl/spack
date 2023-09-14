# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import errno
import os
import sys
from typing import List, Optional

from llnl.util import tty
from llnl.util.tty import colify

import spack
import spack.cmd
import spack.cmd.common.arguments
import spack.config
import spack.detection
import spack.error
import spack.util.environment
from spack import cray_manifest

description = "manage external packages in Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="external_command")

    scopes = spack.config.scopes()

    find_parser = sp.add_parser(
        "find", help="search for external packages and add them to the local DB"
    )
    find_parser.add_argument("--exclude", action="append", help="packages to exclude from search")
    find_parser.add_argument(
        "-p",
        "--path",
        default=None,
        action="append",
        help="one or more alternative search paths for finding externals",
    )
    find_parser.add_argument(
        "--all", action="store_true", help="search for all packages that Spack knows about"
    )
    spack.cmd.common.arguments.add_common_arguments(find_parser, ["tags", "jobs"])
    find_parser.add_argument("packages", nargs=argparse.REMAINDER)
    find_parser.epilog = (
        'The search is by default on packages tagged with the "build-tools" or '
        '"core-packages" tags. Use the --all option to search for every possible '
        "package Spack knows how to find."
    )

    import_parser = sp.add_parser(
        "import", help="import external packages from user configuration to the local DB"
    )
    import_parser.add_argument(
        "--scope",
        choices=scopes,
        metavar=spack.config.SCOPES_METAVAR,
        default=spack.config.default_modify_scope("packages"),
        help="configuration scope to read from",
    )
    import_parser.add_argument(
        "--exclude", action="append", help="packages to exclude from import"
    )
    import_parser.add_argument("packages", nargs=argparse.REMAINDER)

    sp.add_parser("list", help="list detectable packages, by repository and name")

    read_cray_manifest = sp.add_parser(
        "read-cray-manifest",
        help="consume a Spack-compatible description of externally-installed packages, including "
        "dependency relationships",
    )
    read_cray_manifest.add_argument(
        "--file", default=None, help="specify a location other than the default"
    )
    read_cray_manifest.add_argument(
        "--directory", default=None, help="specify a directory storing a group of manifest files"
    )
    read_cray_manifest.add_argument(
        "--ignore-default-dir",
        action="store_true",
        default=False,
        help="ignore the default directory of manifest files",
    )
    read_cray_manifest.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="don't modify DB with files that are read",
    )
    read_cray_manifest.add_argument(
        "--fail-on-error",
        action="store_true",
        help="if a manifest file cannot be parsed, fail and report the full stack trace",
    )


def external_find(args):
    if args.all or not (args.tags or args.packages):
        # If the user calls 'spack external find' with no arguments, and
        # this system has a description of installed packages, then we should
        # consume it automatically.
        try:
            _collect_and_consume_cray_manifest_files()
        except NoManifestFileError:
            # It's fine to not find any manifest file if we are doing the
            # search implicitly (i.e. as part of 'spack external find')
            pass
        except Exception as e:
            # For most exceptions, just print a warning and continue.
            # Note that KeyboardInterrupt does not subclass Exception
            # (so CTRL-C will terminate the program as expected).
            skip_msg = "Skipping manifest and continuing with other external checks"
            if (isinstance(e, IOError) or isinstance(e, OSError)) and e.errno in [
                errno.EPERM,
                errno.EACCES,
            ]:
                # The manifest file does not have sufficient permissions enabled:
                # print a warning and keep going
                tty.warn("Unable to read manifest due to insufficient permissions.", skip_msg)
            else:
                tty.warn("Unable to read manifest, unexpected error: {0}".format(str(e)), skip_msg)

    # Outside the Cray manifest, the search is done by tag for performance reasons,
    # since tags are cached.

    # If the user specified both --all and --tag, then --all has precedence
    if args.all or args.packages:
        # Each detectable package has at least the detectable tag
        args.tags = ["detectable"]
    elif not args.tags:
        # If the user didn't specify anything, search for build tools by default
        args.tags = ["core-packages", "build-tools"]

    candidate_packages = packages_to_search_for(
        names=args.packages, tags=args.tags, exclude=args.exclude
    )
    detected_packages = spack.detection.by_path(
        candidate_packages, path_hints=args.path, max_workers=args.jobs
    )

    _, new_entries = spack.detection.update_database(detected_packages)
    if new_entries:
        tty.msg("The following specs have been detected on this system and added to the local DB")
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg("No new external packages detected")


def packages_to_search_for(
    *, names: Optional[List[str]], tags: List[str], exclude: Optional[List[str]]
):
    result = []
    for current_tag in tags:
        result.extend(spack.repo.PATH.packages_with_tags(current_tag))
    if names:
        result = [x for x in result if x in names]
    if exclude:
        result = [x for x in result if x not in exclude]
    return result


def external_import(args):
    externals = spack.detection.import_externals(scope=args.scope)
    if args.packages:
        externals = {key: value for key, value in externals.items() if key in args.packages}

    _, new_entries = spack.detection.update_database(externals)
    if new_entries:
        tty.msg(
            "The following specs have been imported from user configuration "
            "and added to the local DB"
        )
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg("No new external packages detected")


def external_read_cray_manifest(args):
    _collect_and_consume_cray_manifest_files(
        manifest_file=args.file,
        manifest_directory=args.directory,
        dry_run=args.dry_run,
        fail_on_error=args.fail_on_error,
        ignore_default_dir=args.ignore_default_dir,
    )


def _collect_and_consume_cray_manifest_files(
    manifest_file=None,
    manifest_directory=None,
    dry_run=False,
    fail_on_error=False,
    ignore_default_dir=False,
):
    manifest_files = []
    if manifest_file:
        manifest_files.append(manifest_file)

    manifest_dirs = []
    if manifest_directory:
        manifest_dirs.append(manifest_directory)

    if not ignore_default_dir and os.path.isdir(cray_manifest.default_path):
        tty.debug(
            "Cray manifest path {0} exists: collecting all files to read.".format(
                cray_manifest.default_path
            )
        )
        manifest_dirs.append(cray_manifest.default_path)
    else:
        tty.debug(
            "Default Cray manifest directory {0} does not exist.".format(
                cray_manifest.default_path
            )
        )

    for directory in manifest_dirs:
        for fname in os.listdir(directory):
            if fname.endswith(".json"):
                fpath = os.path.join(directory, fname)
                tty.debug("Adding manifest file: {0}".format(fpath))
                manifest_files.append(os.path.join(directory, fpath))

    if not manifest_files:
        raise NoManifestFileError(
            "--file/--directory not specified, and no manifest found at {0}".format(
                cray_manifest.default_path
            )
        )

    for path in manifest_files:
        tty.debug("Reading manifest file: " + path)
        try:
            cray_manifest.read(path, not dry_run)
        except spack.error.SpackError as e:
            if fail_on_error:
                raise
            else:
                tty.warn("Failure reading manifest file: {0}\n\t{1}".format(path, str(e)))


def external_list(args):
    # Trigger a read of all packages, might take a long time.
    list(spack.repo.PATH.all_package_classes())
    # Print all the detectable packages
    tty.msg("Detectable packages per repository")
    for namespace, pkgs in sorted(spack.package_base.DETECTABLE_PACKAGES.items()):
        print("Repository:", namespace)
        colify.colify(pkgs, indent=4, output=sys.stdout)


def external(parser, args):
    action = {
        "find": external_find,
        "import": external_import,
        "list": external_list,
        "read-cray-manifest": external_read_cray_manifest,
    }
    action[args.external_command](args)


class NoManifestFileError(spack.error.SpackError):
    pass
