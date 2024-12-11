# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import spack.cmd
import spack.cmd.common
import spack.environment as ev
import spack.store
import spack.user_environment as uenv
from spack.cmd.common import arguments

description = "add package to the user environment"
section = "user environment"
level = "short"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
    message with -h."""
    arguments.add_common_arguments(subparser, ["constraint"])

    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        "--sh",
        action="store_const",
        dest="shell",
        const="sh",
        help="print sh commands to load the package",
    )
    shells.add_argument(
        "--csh",
        action="store_const",
        dest="shell",
        const="csh",
        help="print csh commands to load the package",
    )
    shells.add_argument(
        "--fish",
        action="store_const",
        dest="shell",
        const="fish",
        help="print fish commands to load the package",
    )
    shells.add_argument(
        "--bat",
        action="store_const",
        dest="shell",
        const="bat",
        help="print bat commands to load the package",
    )
    shells.add_argument(
        "--pwsh",
        action="store_const",
        dest="shell",
        const="pwsh",
        help="print pwsh commands to load the package",
    )

    subparser.add_argument(
        "--first",
        action="store_true",
        default=False,
        dest="load_first",
        help="load the first match if multiple packages match the spec",
    )

    subparser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="show loaded packages: same as `spack find --loaded`",
    )


# Use this later for executing the cached shell script
def read_script_and_execute(env_mod, variable, *paths):
    for path in paths:
        env_mod.prepend_path(variable, path)


def cache_shell_script(specs, shell = None):
    spack_shell = shell if shell else os.environ.get("SPACK_SHELL")
    for spec in specs:
       # spec is a str
       shell_script_path = os.path.join(spec.prefix, ".spack", f"{spec.name}_shell.{spack_shell}")

       spec_mod = uenv.environment_modifications_for_specs(*[spec])
       spec_mod.prepend_path(uenv.spack_loaded_hashes_var, spec.dag_hash())
       spec_cmds = spec_mod.shell_modifications(shell)

       with open(shell_script_path, "w") as f:
           f.write(spec_cmds)


def load(parser, args):
    env = ev.active_environment()

    if args.list:
        results = spack.cmd.filter_loaded_specs(args.specs())
        if sys.stdout.isatty():
            spack.cmd.print_how_many_pkgs(results, "loaded")
        spack.cmd.display_specs(results)
        return

    constraint_specs = spack.cmd.parse_specs(args.constraint)
    specs = [
        spack.cmd.disambiguate_spec(spec, env, first=args.load_first) for spec in constraint_specs
    ]

    if not args.shell:
        specs_str = " ".join(str(s) for s in constraint_specs) or "SPECS"
        spack.cmd.common.shell_init_instructions(
            "spack load", f"    eval `spack load {{sh_arg}} {specs_str}`"
        )
        return 1

    # Check if spec's pkg.py file was changed
    # (modification date - os.path.get_end_time?)
    # var/spack/envirnonments/env-name/.spack-env

    with spack.store.STORE.db.read_transaction():
        shell = args.shell if args.shell else os.environ.get("SPACK_SHELL")
        env_mod = uenv.environment_modifications_for_specs(*specs)
        for spec in specs:
            shell_script_path = os.path.join(spec.prefix, ".spack", f"{spec.name}_shell.{shell}")

            # Cache each individual spec's commands
            cache_shell_script([spec], shell)

            env_mod.prepend_path(uenv.spack_loaded_hashes_var, spec.dag_hash())
            cmds = env_mod.shell_modifications(shell)

        sys.stdout.write(cmds)
