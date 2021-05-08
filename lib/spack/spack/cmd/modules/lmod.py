# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools
import os

import llnl.util.filesystem
import spack.cmd.common.arguments
import spack.cmd.modules


def add_command(parser, command_dict):
    lmod_parser = parser.add_parser(
        'lmod', help='manipulate hierarchical module files'
    )
    sp = spack.cmd.modules.setup_parser(lmod_parser)

    # Set default module file for a package
    setdefault_parser = sp.add_parser(
        'setdefault', help='set the default module file for a package'
    )
    spack.cmd.common.arguments.add_common_arguments(
        setdefault_parser, ['constraint']
    )

    callbacks = dict(spack.cmd.modules.callbacks.items())
    callbacks['setdefault'] = setdefault

    command_dict['lmod'] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type='lmod', callbacks=callbacks
    )


def setdefault(module_type, specs, args):
    """Set the default module file, when multiple are present"""
    # For details on the underlying mechanism see:
    #
    # https://lmod.readthedocs.io/en/latest/060_locating.html#marking-a-version-as-default
    #
    spack.cmd.modules.one_spec_or_raise(specs)
    writer = spack.modules.module_types['lmod'](
        specs[0], args.module_set_name)

    module_folder = os.path.dirname(writer.layout.filename)
    module_basename = os.path.basename(writer.layout.filename)
    with llnl.util.filesystem.working_dir(module_folder):
        if os.path.exists('default') and os.path.islink('default'):
            os.remove('default')
        os.symlink(module_basename, 'default')
