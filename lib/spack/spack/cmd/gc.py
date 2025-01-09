# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd.common.arguments
import spack.cmd.common.confirmation
import spack.cmd.uninstall
import spack.deptypes as dt
import spack.environment as ev
import spack.store

description = "remove specs that are now no longer needed"
section = "build"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "-E",
        "--except-any-environment",
        action="store_true",
        help="remove everything unless needed by an environment",
    )
    subparser.add_argument(
        "-e",
        "--except-environment",
        metavar="ENV",
        action="append",
        default=[],
        help="remove everything unless needed by specified environment\n"
        "you can list multiple environments, or specify directory\n"
        "environments by path.",
    )
    subparser.add_argument(
        "-b",
        "--keep-build-dependencies",
        action="store_true",
        help="do not remove installed build-only dependencies of roots\n"
        "(default is to keep only link & run dependencies)",
    )
    spack.cmd.common.arguments.add_common_arguments(subparser, ["yes_to_all", "constraint"])


def roots_from_environments(args, active_env):
    # if we're using -E or -e, make a list of environments whose roots we should consider.
    all_environments = []

    # -E will garbage collect anything not needed by any env, including the current one
    if args.except_any_environment:
        all_environments += list(ev.all_environments())
        if active_env:
            all_environments.append(active_env)

    # -e says "also preserve things needed by this particular env"
    for env_name_or_dir in args.except_environment:
        if ev.exists(env_name_or_dir):
            env = ev.read(env_name_or_dir)
        elif ev.is_env_dir(env_name_or_dir):
            env = ev.Environment(env_name_or_dir)
        else:
            tty.die(f"No such environment: '{env_name_or_dir}'")
        all_environments.append(env)

    # add root hashes from all considered environments to list of roots
    root_hashes = set()
    for env in all_environments:
        root_hashes |= set(env.concretized_order)

    return root_hashes


def gc(parser, args):
    deptype = dt.LINK | dt.RUN
    if args.keep_build_dependencies:
        deptype |= dt.BUILD

    active_env = ev.active_environment()

    # wrap the whole command with a read transaction to avoid multiple
    with spack.store.STORE.db.read_transaction():
        if args.except_environment or args.except_any_environment:
            # if either of these is specified, we ignore the active environment and garbage
            # collect anything NOT in specified environments.
            root_hashes = roots_from_environments(args, active_env)

        elif active_env:
            # only gc what's in current environment
            tty.msg(f"Restricting garbage collection to environment '{active_env.name}'")
            root_hashes = set(spack.store.STORE.db.all_hashes())  # keep everything
            root_hashes -= set(active_env.all_hashes())  # except this env
            root_hashes |= set(active_env.concretized_order)  # but keep its roots
        else:
            # consider all explicit specs roots (the default for db.unused_specs())
            root_hashes = None

        specs = spack.store.STORE.db.unused_specs(root_hashes=root_hashes, deptype=deptype)

        # limit search to constraint specs if provided
        if args.constraint:
            hashes = set(spec.dag_hash() for spec in args.specs())
            specs = [spec for spec in specs if spec.dag_hash() in hashes]

        if not specs:
            tty.msg("There are no unused specs. Spack's store is clean.")
            return

        if not args.yes_to_all:
            spack.cmd.common.confirmation.confirm_action(specs, "uninstalled", "uninstall")

        spack.cmd.uninstall.do_uninstall(specs, force=False)
