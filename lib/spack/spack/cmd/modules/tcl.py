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
    tcl_parser = parser.add_parser(
        'tcl', help='manipulate non-hierarchical module files'
    )
    sp = spack.cmd.modules.setup_parser(tcl_parser)

    # Set default module file for a package
    setdefault_parser = sp.add_parser(
        'setdefault', help='set the default module file for a package'
    )
    spack.cmd.common.arguments.add_common_arguments(
        setdefault_parser, ['constraint']
    )

    callbacks = dict(spack.cmd.modules.callbacks.items())
    callbacks['setdefault'] = setdefault

    command_dict['tcl'] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type='tcl', callbacks=callbacks
    )


def setdefault(module_type, specs, args):
    """Set the default module file, when multiple are present"""
    spack.cmd.modules.one_spec_or_raise(specs)
    writer = spack.modules.module_types['tcl'](specs[0])

    module_folder = os.path.dirname(writer.layout.filename)
    module_basename = os.path.basename(writer.layout.filename)
    with llnl.util.filesystem.working_dir(module_folder):
        if os.path.exists('.version'):
            os.remove('.version')
        version_file = os.path.join(module_folder, '.version')
        with open(version_file, mode='w') as f:
            f.write('#%Module\n')
            f.write('set ModulesVersion %s\n' % module_basename)
