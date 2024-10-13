# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.environment as ev
import spack.package_base
import spack.traverse
from spack.cmd.common import arguments

description = "patch expanded archive sources in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["no_checksum", "specs"])
    arguments.add_concretizer_args(subparser)


def patch(parser, args):
    if not args.specs:
        env = ev.active_environment()
        if not env:
            tty.die("`spack patch` requires a spec or an active environment")
        return _patch_env(env)

    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    specs = spack.cmd.parse_specs(args.specs, concretize=False)
    for spec in specs:
        _patch(spack.cmd.matching_spec_from_env(spec).package)


def _patch_env(env: ev.Environment):
    tty.msg(f"Patching specs from environment {env.name}")
    for spec in spack.traverse.traverse_nodes(env.concrete_roots()):
        _patch(spec.package)


def _patch(pkg: spack.package_base.PackageBase):
    pkg.stage.keep = True
    with pkg.stage:
        pkg.do_patch()
    tty.msg(f"Patched {pkg.name} in {pkg.stage.path}")
