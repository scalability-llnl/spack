# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import functools

import spack.cmd.common.arguments
import spack.cmd.modules
import spack.config
import spack.modules
import spack.modules.tcl


def add_command(parser, command_dict):
    tcl_parser = parser.add_parser("tcl", help="manipulate non-hierarchical module files")
    sp = spack.cmd.modules.setup_parser(tcl_parser)

    # Set default module file for a package
    setdefault_parser = sp.add_parser(
        "setdefault", help="set the default module file for a package"
    )
    spack.cmd.common.arguments.add_common_arguments(setdefault_parser, ["constraint"])

    callbacks = dict(spack.cmd.modules.callbacks.items())
    callbacks["setdefault"] = setdefault

    command_dict["tcl"] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type="tcl", callbacks=callbacks
    )


def setdefault(module_type, specs, args):
    """set the default module file, when multiple are present"""
    # Currently, accepts only a single matching spec
    spack.cmd.modules.one_spec_or_raise(specs)
    spec = specs[0]
    data = {"modules": {args.module_set_name: {"tcl": {"defaults": [str(spec)]}}}}
    spack.modules.tcl.configuration_registry = {}
    scope = spack.config.InternalConfigScope("tcl-setdefault", data)
    with spack.config.override(scope):
        writer = spack.modules.module_types["tcl"](spec, args.module_set_name)
        writer.update_module_defaults()
