# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys
from typing import Dict, Optional

import llnl.string
import llnl.util.lang
from llnl.util import tty

import spack.cmd
import spack.repo
import spack.spec
import spack.stage
import spack.util.web as web_util
from spack.cmd.common import arguments
from spack.package_base import (
    ManualDownloadRequiredError,
    PackageBase,
    deprecated_version,
    preferred_version,
)
from spack.util.editor import editor
from spack.util.format import get_version_lines
from spack.version import StandardVersion, Version

description = "checksum available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "--keep-stage",
        action="store_true",
        default=False,
        help="don't clean up staging area when command completes",
    )
    subparser.add_argument(
        "--batch",
        "-b",
        action="store_true",
        default=False,
        help="don't ask which versions to checksum",
    )
    subparser.add_argument(
        "--latest",
        "-l",
        action="store_true",
        default=False,
        help="checksum the latest available version",
    )
    subparser.add_argument(
        "--preferred",
        "-p",
        action="store_true",
        default=False,
        help="checksum the known Spack preferred version",
    )
    modes_parser = subparser.add_mutually_exclusive_group()
    modes_parser.add_argument(
        "--add-to-package",
        "-a",
        action="store_true",
        default=False,
        help="add new versions to package",
    )
    modes_parser.add_argument(
        "--verify", action="store_true", default=False, help="verify known package checksums"
    )
    subparser.add_argument("package", help="name or spec (e.g. `cmake` or `cmake@3.18`)")
    subparser.add_argument(
        "versions",
        nargs="*",
        help="checksum these specific versions (if omitted, Spack searches for remote versions)",
    )
    arguments.add_common_arguments(subparser, ["jobs"])
    subparser.epilog = (
        "examples:\n"
        "  `spack checksum zlib@1.2` autodetects versions 1.2.0 to 1.2.13 from the remote\n"
        "  `spack checksum zlib 1.2.13` checksums exact version 1.2.13 directly without search\n"
    )


def checksum(parser, args):
    spec = spack.spec.Spec(args.package)

    # Get the package we're going to generate checksums for
    pkg: PackageBase = spack.repo.PATH.get_pkg_class(spec.name)(spec)

    # Skip manually downloaded packages
    if pkg.manual_download:
        raise ManualDownloadRequiredError(pkg.download_instr)

    versions = [StandardVersion.from_string(v) for v in args.versions]

    # Define placeholder for remote versions. This'll help reduce redundant work if we need to
    # check for the existence of remote versions more than once.
    remote_versions: Optional[Dict[StandardVersion, str]] = None

    # Add latest version if requested
    if args.latest:
        remote_versions = pkg.fetch_remote_versions(concurrency=args.jobs)
        if len(remote_versions) > 0:
            versions.append(max(remote_versions.keys()))

    # Add preferred version if requested (todo: exclude git versions)
    if args.preferred:
        versions.append(preferred_version(pkg))

    # Store a dict of the form version -> URL
    url_dict: Dict[StandardVersion, str] = {}

    for version in versions:
        if deprecated_version(pkg, version):
            tty.warn(f"Version {version} is deprecated")

        url = pkg.find_valid_url_for_version(version)
        if url is not None:
            url_dict[version] = url
            continue
        # If we get here, it's because no valid url was provided by the package. Do expensive
        # fallback to try to recover
        if remote_versions is None:
            remote_versions = pkg.fetch_remote_versions(concurrency=args.jobs)
        if version in remote_versions:
            url_dict[version] = remote_versions[version]

    if len(versions) <= 0:
        if remote_versions is None:
            remote_versions = pkg.fetch_remote_versions(concurrency=args.jobs)
        url_dict = remote_versions

    # A spidered URL can differ from the package.py *computed* URL, pointing to different tarballs.
    # For example, GitHub release pages sometimes have multiple tarballs with different shasum:
    # - releases/download/1.0/<pkg>-1.0.tar.gz (uploaded tarball)
    # - archive/refs/tags/1.0.tar.gz           (generated tarball)
    # We wanna ensure that `spack checksum` and `spack install` ultimately use the same URL, so
    # here we check whether the crawled and computed URLs disagree, and if so, prioritize the
    # former if that URL exists (just sending a HEAD request that is).
    url_changed_for_version = set()
    for version, url in url_dict.items():
        possible_urls = pkg.all_urls_for_version(version)
        if url not in possible_urls:
            for possible_url in possible_urls:
                if web_util.url_exists(possible_url):
                    url_dict[version] = possible_url
                    break
            else:
                url_changed_for_version.add(version)

    if not url_dict:
        tty.die(f"Could not find any remote versions for {pkg.name}")
    elif len(url_dict) > 1 and not args.batch and sys.stdin.isatty():
        filtered_url_dict = spack.stage.interactive_version_filter(
            url_dict,
            pkg.versions,
            url_changes=url_changed_for_version,
            initial_verion_filter=spec.versions,
        )
        if not filtered_url_dict:
            exit(0)
        url_dict = filtered_url_dict
    else:
        tty.info(f"Found {llnl.string.plural(len(url_dict), 'version')} of {pkg.name}")

    version_hashes = spack.stage.get_checksums_for_versions(
        url_dict, pkg.name, keep_stage=args.keep_stage, fetch_options=pkg.fetch_options
    )

    if args.verify:
        print_checksum_status(pkg, version_hashes)
        sys.exit(0)

    # convert dict into package.py version statements
    version_lines = get_version_lines(version_hashes, url_dict)
    print()
    print(version_lines)
    print()

    if args.add_to_package:
        add_versions_to_package(pkg, version_lines, args.batch)


def print_checksum_status(pkg: PackageBase, version_hashes: dict):
    """
    Verify checksums present in version_hashes against those present
    in the package's instructions.

    Args:
        pkg (spack.package_base.PackageBase): A package class for a given package in Spack.
        version_hashes (dict): A dictionary of the form: version -> checksum.

    """
    results = []
    num_verified = 0
    failed = False

    max_len = max(len(str(v)) for v in version_hashes)
    num_total = len(version_hashes)

    for version, sha in version_hashes.items():
        if version not in pkg.versions:
            msg = "No previous checksum"
            status = "-"

        elif sha == pkg.versions[version]["sha256"]:
            msg = "Correct"
            status = "="
            num_verified += 1

        else:
            msg = sha
            status = "x"
            failed = True

        results.append("{0:{1}}  {2} {3}".format(str(version), max_len, f"[{status}]", msg))

    # Display table of checksum results.
    tty.msg(f"Verified {num_verified} of {num_total}", "", *llnl.util.lang.elide_list(results), "")

    # Terminate at the end of function to prevent additional output.
    if failed:
        print()
        tty.die("Invalid checksums found.")


def add_versions_to_package(pkg: PackageBase, version_lines: str, is_batch: bool):
    """
    Add checksumed versions to a package's instructions and open a user's
    editor so they may double check the work of the function.

    Args:
        pkg (spack.package_base.PackageBase): A package class for a given package in Spack.
        version_lines (str): A string of rendered version lines.

    """
    # Get filename and path for package
    filename = spack.repo.PATH.filename_for_package_name(pkg.name)
    num_versions_added = 0

    version_statement_re = re.compile(r"([\t ]+version\([^\)]*\))")
    version_re = re.compile(r'[\t ]+version\(\s*"([^"]+)"[^\)]*\)')

    # Split rendered version lines into tuple of (version, version_line)
    # We reverse sort here to make sure the versions match the version_lines
    new_versions = []
    for ver_line in version_lines.split("\n"):
        match = version_re.match(ver_line)
        if match:
            new_versions.append((Version(match.group(1)), ver_line))

    with open(filename, "r+") as f:
        contents = f.read()
        split_contents = version_statement_re.split(contents)

        for i, subsection in enumerate(split_contents):
            # If there are no more versions to add we should exit
            if len(new_versions) <= 0:
                break

            # Check if the section contains a version
            contents_version = version_re.match(subsection)
            if contents_version is not None:
                parsed_version = Version(contents_version.group(1))

                if parsed_version < new_versions[0][0]:
                    split_contents[i:i] = [new_versions.pop(0)[1], " # FIXME", "\n"]
                    num_versions_added += 1

                elif parsed_version == new_versions[0][0]:
                    new_versions.pop(0)

        # Seek back to the start of the file so we can rewrite the file contents.
        f.seek(0)
        f.writelines("".join(split_contents))

        tty.msg(f"Added {num_versions_added} new versions to {pkg.name}")
        tty.msg(f"Open {filename} to review the additions.")

    if sys.stdout.isatty() and not is_batch:
        editor(filename)
