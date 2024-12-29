# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.environment as ev
import spack.package_base
import spack.traverse
from spack.cmd.common import arguments

description = "expand downloaded archive in preparation for install"
section = "build"
level = "long"


class StageFilter:
    """
    Encapsulation of reasons to skip staging
    """

    def __init__(self, exclusions, skip_installed):
        """
        :param exclusions: A list of specs to skip if satisfied.
        :param skip_installed: A boolean indicating whether to skip already installed specs.
        """
        self.exclusions = exclusions
        self.skip_installed = skip_installed

    def __call__(self, spec):
        """filter action, true means spec should be filtered"""
        if spec.external:
            return True

        if self.skip_installed and spec.installed:
            return True

        if any(spec.satisfies(exclude) for exclude in self.exclusions):
            return True

        return False


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["no_checksum", "specs"])
    subparser.add_argument(
        "-p", "--path", dest="path", help="path to stage package, does not add to spack tree"
    )
    subparser.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="exclude packages that satisfy the specified specs",
    )
    subparser.add_argument(
        "-s", "--skip-installed", action="store_true", help="dont restage already installed specs"
    )
    arguments.add_concretizer_args(subparser)


def stage(parser, args):
    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    exclusion_specs = spack.cmd.parse_specs(args.exclude, concretize=False)
    filter = StageFilter(exclusion_specs, args.skip_installed)

    if not args.specs:
        env = ev.active_environment()
        if not env:
            tty.die("`spack stage` requires a spec or an active environment")
        return _stage_env(env, filter)

    specs = spack.cmd.parse_specs(args.specs, concretize=False)

    # We temporarily modify the working directory when setting up a stage, so we need to
    # convert this to an absolute path here in order for it to remain valid later.
    custom_path = os.path.abspath(args.path) if args.path else None

    # prevent multiple specs from extracting in the same folder
    if len(specs) > 1 and custom_path:
        tty.die("`--path` requires a single spec, but multiple were provided")

    specs = spack.cmd.matching_specs_from_env(specs)
    for spec in specs:
        spec = spack.cmd.matching_spec_from_env(spec)

        if filter(spec):
            continue

        pkg = spec.package

        if custom_path:
            pkg.path = custom_path

        _stage(pkg)


def _stage_env(env: ev.Environment, filter):
    tty.msg(f"Staging specs from environment {env.name}")
    for spec in spack.traverse.traverse_nodes(env.concrete_roots()):

        if filter(spec):
            continue

        _stage(spec.package)


def _stage(pkg: spack.package_base.PackageBase):
    # Use context manager to ensure we don't restage while an installation is in progress
    # keep = True ensures that the stage is not removed after exiting the context manager
    pkg.stage.keep = True
    with pkg.stage:
        pkg.do_stage()
    tty.msg(f"Staged {pkg.name} in {pkg.stage.path}")
