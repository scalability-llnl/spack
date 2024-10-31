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


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["no_checksum", "specs"])
    subparser.add_argument(
        "-p", "--path", dest="path", help="path to stage package, does not add to spack tree"
    )
    arguments.add_concretizer_args(subparser)


def stage(parser, args):
    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    if not args.specs:
        env = ev.active_environment()
        if not env:
            tty.die("`spack stage` requires a spec or an active environment")
        return _stage_env(env)

    specs = spack.cmd.parse_specs(args.specs, concretize=False)

    # We temporarily modify the working directory when setting up a stage, so we need to
    # convert this to an absolute path here in order for it to remain valid later.
    custom_path = os.path.abspath(args.path) if args.path else None

    # prevent multiple specs from extracting in the same folder
    if len(specs) > 1 and custom_path:
        tty.die("`--path` requires a single spec, but multiple were provided")

    for spec in specs:
        spec = spack.cmd.matching_spec_from_env(spec)
        pkg = spec.package

        if custom_path:
            pkg.path = custom_path

        _stage(pkg)


def _stage_env(env: ev.Environment):
    tty.msg(f"Staging specs from environment {env.name}")
    for spec in spack.traverse.traverse_nodes(env.concrete_roots()):
        _stage(spec.package)


def _stage(pkg: spack.package_base.PackageBase):
    # Use context manager to ensure we don't restage while an installation is in progress
    # keep = True ensures that the stage is not removed after exiting the context manager
    pkg.stage.keep = True
    with pkg.stage:
        pkg.do_stage()
    tty.msg(f"Staged {pkg.name} in {pkg.stage.path}")
