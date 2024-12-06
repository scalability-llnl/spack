# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.config
from spack.cmd.common import arguments

description = "remove specs from an environment"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "-a", "--all", action="store_true", help="remove all specs from (clear) the environment"
    )

    arguments.add_common_arguments(subparser, ["specs"])


def _update_config(specs_to_remove, remove_all=False):
    def change_fn(dev_config):
        modified = False
        for spec in specs_to_remove:
            if spec.name in dev_config:
                tty.msg("Undevelop: removing {0}".format(spec.name))
                del dev_config[spec.name]
                modified = True
        if remove_all and dev_config:
            dev_config.clear()
            modified = True
        return modified

    spack.config.update_all("develop", change_fn)


def undevelop(parser, args):
    remove_specs = None
    remove_all = False
    if args.all:
        remove_all = True
    else:
        remove_specs = spack.cmd.parse_specs(args.specs)

    # TODO: when https://github.com/spack/spack/pull/35307 is merged,
    # an active env is not required if a scope is specified
    env = spack.cmd.require_active_env(cmd_name="undevelop")
    with env.write_transaction():
        _update_config(remove_specs, remove_all)

    updated_all_dev_specs = set(spack.config.get("develop"))
    remove_spec_names = set(x.name for x in remove_specs)

    if remove_all:
        not_fully_removed = updated_all_dev_specs
    else:
        not_fully_removed = updated_all_dev_specs & remove_spec_names

    if not_fully_removed:
        tty.msg(
            "The following specs could not be removed as develop specs"
            " - see `spack config blame develop` to locate files requiring"
            f" manual edits: {', '.join(not_fully_removed)}"
        )
