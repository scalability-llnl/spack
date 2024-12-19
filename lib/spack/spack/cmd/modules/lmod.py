# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools

import spack.cmd.common.arguments
import spack.cmd.modules
import spack.config
import spack.modules
import spack.modules.lmod


def add_command(parser, command_dict):
    lmod_parser = parser.add_parser("lmod", help="manipulate hierarchical module files")
    sp = spack.cmd.modules.setup_parser(lmod_parser)

    # Set default module file for a package
    setdefault_parser = sp.add_parser(
        "setdefault", help="set the default module file for a package"
    )
    spack.cmd.common.arguments.add_common_arguments(setdefault_parser, ["constraint"])

    callbacks = dict(spack.cmd.modules.callbacks.items())
    callbacks["setdefault"] = setdefault

    command_dict["lmod"] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type="lmod", callbacks=callbacks
    )


def setdefault(module_type, specs, args):
    """set the default module file, when multiple are present"""
    # For details on the underlying mechanism see:
    #
    # https://lmod.readthedocs.io/en/latest/060_locating.html#marking-a-version-as-default
    #
    spack.cmd.modules.one_spec_or_raise(specs)
    spec = specs[0]
    data = {"modules": {args.module_set_name: {"lmod": {"defaults": [str(spec)]}}}}
    # Need to clear the cache if a SpackCommand is called during scripting
    spack.modules.lmod.configuration_registry = {}
    scope = spack.config.InternalConfigScope("lmod-setdefault", data)
    with spack.config.override(scope):
        writer = spack.modules.module_types["lmod"](spec, args.module_set_name)
        writer.update_module_defaults()
