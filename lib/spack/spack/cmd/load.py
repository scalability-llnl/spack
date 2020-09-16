# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment
import spack.user_environment as uenv
import spack.store

description = "add package to the user environment"
section = "user environment"
level = "short"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
       message with -h. """
    arguments.add_common_arguments(
        subparser, ['recurse_dependencies', 'installed_specs'])

    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to load the package")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to load the package")
    shells.add_argument(
        '--fish', action='store_const', dest='shell', const='fish',
        help="print fish commands to load the package")

    subparser.add_argument(
        '--first',
        action='store_true',
        default=False,
        dest='load_first',
        help="load the first match if multiple packages match the spec"
    )

    subparser.add_argument(
        '--only',
        default='package,dependencies',
        dest='things_to_load',
        choices=['package', 'dependencies'],
        help="""select whether to load the package and its dependencies
the default is to load the package and all dependencies
alternatively one can decide to load only the package or only
the dependencies"""
    )


def load(parser, args):
    env = ev.get_env(args, 'load')
    specs = [spack.cmd.disambiguate_spec(spec, env, first=args.load_first,
                                         compatible=True,
                                         preferred=True)
             for spec in spack.cmd.parse_specs(args.specs)]

    if not args.shell:
        specs_string = ' '.join(args.specs)
        msg = [
            "This command works best with Spack's shell support",
            ""
        ] + spack.cmd.common.shell_init_instructions + [
            'Or, if you want to use `spack load` without initializing',
            'shell support, you can run one of these:',
            '',
            '    eval `spack load --sh %s`   # for bash/sh' % specs_string,
            '    eval `spack load --csh %s`  # for csh/tcsh' % specs_string,
        ]
        tty.msg(*msg)
        return 1

    with spack.store.db.read_transaction():
        if 'dependencies' in args.things_to_load:
            include_roots = 'package' in args.things_to_load
            specs = [dep for spec in specs
                     for dep in
                     spec.traverse(root=include_roots, order='post')]

        env_mod = spack.util.environment.EnvironmentModifications()
        for spec in specs:
            env_mod.extend(uenv.environment_modifications_for_spec(spec))
            env_mod.prepend_path(uenv.spack_loaded_hashes_var, spec.dag_hash())
        cmds = env_mod.shell_modifications(args.shell)

        sys.stdout.write(cmds)
