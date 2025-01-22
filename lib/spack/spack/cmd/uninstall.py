# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from typing import Dict, List, Optional

from llnl.util import tty
from llnl.util.tty.colify import colify

import spack.cmd
import spack.cmd.common.confirmation as confirmation
import spack.environment as ev
import spack.package_base
import spack.spec
import spack.store
import spack.traverse as traverse
from spack.cmd.common import arguments

from ..enums import InstallRecordStatus

description = "remove installed packages"
section = "build"
level = "short"

error_message = """You can either:
    a) use a more specific spec, or
    b) specify the spec by its hash (e.g. `spack uninstall /hash`), or
    c) use `spack uninstall --all` to uninstall ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {"long": True, "show_flags": False, "variants": False, "indent": 4}


def setup_parser(subparser):
    epilog_msg = (
        "Specs to be uninstalled are specified using the spec syntax"
        " (`spack help --spec`) and can be identified by their "
        "hashes. To remove packages that are needed only at build "
        "time and were not explicitly installed see `spack gc -h`."
        "\n\nWhen using the --all option ALL packages matching the "
        "supplied specs will be uninstalled. For instance, "
        "`spack uninstall --all libelf` uninstalls all the versions "
        "of `libelf` currently present in Spack's store. If no spec "
        "is supplied, all installed packages will be uninstalled. "
        "If used in an environment, all packages in the environment "
        "will be uninstalled."
    )
    subparser.epilog = epilog_msg
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="remove regardless of whether other packages or environments depend on this one",
    )
    subparser.add_argument(
        "--remove",
        action="store_true",
        dest="remove",
        help="if in an environment, then the spec should also be removed from "
        "the environment description",
    )
    arguments.add_common_arguments(
        subparser, ["recurse_dependents", "yes_to_all", "installed_specs"]
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="remove ALL installed packages that match each supplied spec",
    )
    subparser.add_argument(
        "--origin", dest="origin", help="only remove DB records with the specified origin"
    )


def find_matching_specs(
    env: Optional[ev.Environment],
    specs: List[spack.spec.Spec],
    allow_multiple_matches: bool = False,
    origin=None,
) -> List[spack.spec.Spec]:
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        env: optional active environment
        specs: list of specs to be matched against installed packages
        allow_multiple_matches: if True multiple matches are admitted
        origin: origin of the spec

    Return:
        list: list of specs
    """
    # constrain uninstall resolution to current environment if one is active
    hashes = env.all_hashes() if env else None

    # List of specs that match expressions given via command line
    specs_from_cli: List[spack.spec.Spec] = []
    has_errors = False
    for spec in specs:
        matching = spack.store.STORE.db.query_local(
            spec,
            hashes=hashes,
            installed=(InstallRecordStatus.INSTALLED | InstallRecordStatus.DEPRECATED),
            origin=origin,
        )
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error("{0} matches multiple packages:".format(spec))
            sys.stderr.write("\n")
            spack.cmd.display_specs(matching, output=sys.stderr, **display_args)
            sys.stderr.write("\n")
            sys.stderr.flush()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not None:
            if env:
                pkg_type = "packages in environment '%s'" % env.name
            else:
                pkg_type = "installed packages"
            tty.die("{0} does not match any {1}.".format(spec, pkg_type))

        specs_from_cli.extend(matching)

    if has_errors:
        tty.die(error_message)

    return specs_from_cli


def installed_dependents(specs: List[spack.spec.Spec]) -> List[spack.spec.Spec]:
    # Note: the combination of arguments (in particular order=breadth
    # and root=False) ensures dependents and matching_specs are non-overlapping;
    # In the extreme case of "spack uninstall --all" we get the entire database as
    # input; in that case we return an empty list.

    def is_installed(spec):
        record = spack.store.STORE.db.query_local_by_spec_hash(spec.dag_hash())
        return record and record.installed

    all_specs = traverse.traverse_nodes(
        specs,
        root=False,
        order="breadth",
        cover="nodes",
        deptype=("link", "run"),
        direction="parents",
        key=lambda s: s.dag_hash(),
    )

    with spack.store.STORE.db.read_transaction():
        return [spec for spec in all_specs if is_installed(spec)]


def dependent_environments(
    specs: List[spack.spec.Spec], current_env: Optional[ev.Environment] = None
) -> Dict[ev.Environment, List[spack.spec.Spec]]:
    # For each tracked environment, get the specs we would uninstall from it.
    # Don't instantiate current environment twice.
    env_names = ev.all_environment_names()
    if current_env:
        env_names = (name for name in env_names if name != current_env.name)

    # Mapping from Environment -> non-zero list of specs contained in it.
    other_envs_to_specs: Dict[ev.Environment, List[spack.spec.Spec]] = {}
    for other_env in (ev.Environment(ev.root(name)) for name in env_names):
        specs_in_other_env = all_specs_in_env(other_env, specs)
        if specs_in_other_env:
            other_envs_to_specs[other_env] = specs_in_other_env

    return other_envs_to_specs


def all_specs_in_env(env: ev.Environment, specs: List[spack.spec.Spec]) -> List[spack.spec.Spec]:
    """Given a list of specs, return those that are in the env"""
    hashes = set(env.all_hashes())
    return [s for s in specs if s.dag_hash() in hashes]


def _remove_from_env(spec, env):
    """Remove a spec from an environment if it is a root."""
    try:
        # try removing the spec from the current active
        # environment. this will fail if the spec is not a root
        env.remove(spec, force=True)
    except ev.SpackEnvironmentError:
        pass  # ignore non-root specs


def do_uninstall(specs: List[spack.spec.Spec], force: bool = False):
    # TODO: get rid of the call-sites that use this function,
    # so that we don't have to do a dance of list -> set -> list -> set
    hashes_to_remove = set(s.dag_hash() for s in specs)

    for s in traverse.traverse_nodes(
        specs, order="topo", direction="children", root=True, cover="nodes", deptype="all"
    ):
        if s.dag_hash() in hashes_to_remove:
            spack.package_base.PackageBase.uninstall_by_spec(s, force=force)


def get_uninstall_list(args, specs: List[spack.spec.Spec], env: Optional[ev.Environment]):
    """Returns unordered uninstall_list and remove_list: these may overlap (some things
    may be both uninstalled and removed from the current environment).

    It is assumed we are in an environment if --remove is specified (this
    method raises an exception otherwise)."""
    if args.remove and not env:
        raise ValueError("Can only use --remove when in an environment")

    # Gets the list of installed specs that match the ones given via cli
    # args.all takes care of the case where '-a' is given in the cli
    matching_specs = find_matching_specs(env, specs, args.all, origin=args.origin)
    dependent_specs = installed_dependents(matching_specs)
    all_uninstall_specs = matching_specs + dependent_specs if args.dependents else matching_specs
    other_dependent_envs = dependent_environments(all_uninstall_specs, current_env=env)

    # There are dependents and we didn't ask to remove dependents
    dangling_dependents = dependent_specs and not args.dependents

    # An environment different than the current env depends on
    # one or more of the list of all specs to be uninstalled.
    dangling_environments = not args.remove and other_dependent_envs

    has_error = not args.force and (dangling_dependents or dangling_environments)

    if has_error:
        msgs = []
        tty.info("Refusing to uninstall the following specs")
        spack.cmd.display_specs(matching_specs, **display_args)
        if dangling_dependents:
            print()
            tty.info("The following dependents are still installed:")
            spack.cmd.display_specs(dependent_specs, **display_args)
            msgs.append("use `spack uninstall --dependents` to remove dependents too")
        if dangling_environments:
            print()
            tty.info("The following environments still reference these specs:")
            colify([e.name for e in other_dependent_envs.keys()], indent=4)
            if env:
                msgs.append("use `spack remove` to remove the spec from the current environment")
            msgs.append("use `spack env remove` to remove environments")
        msgs.append("use `spack uninstall --force` to override")
        print()
        tty.die("There are still dependents.", *msgs)

    # If we are in an environment, this will track specs in this environment
    # which should only be removed from the environment rather than uninstalled
    remove_only = []
    if args.remove and not args.force:
        for specs_in_other_env in other_dependent_envs.values():
            remove_only.extend(specs_in_other_env)

    if remove_only:
        tty.info(
            "The following specs will be removed but not uninstalled because"
            " they are also used by another environment: {speclist}".format(
                speclist=", ".join(x.name for x in remove_only)
            )
        )

    # Compute the set of specs that should be removed from the current env.
    # This may overlap (some specs may be uninstalled and also removed from
    # the current environment).
    remove_specs = all_specs_in_env(env, all_uninstall_specs) if env and args.remove else []

    return list(set(all_uninstall_specs) - set(remove_only)), remove_specs


def uninstall_specs(args, specs):
    env = ev.active_environment()

    uninstall_list, remove_list = get_uninstall_list(args, specs, env)

    if not uninstall_list:
        tty.warn("There are no package to uninstall.")
        return

    if not args.yes_to_all:
        confirmation.confirm_action(uninstall_list, "uninstalled", "uninstall")

    # Uninstall everything on the list
    do_uninstall(uninstall_list, args.force)

    if env:
        with env.write_transaction():
            for spec in remove_list:
                _remove_from_env(spec, env)
            env.write()

        env.regenerate_views()


def uninstall(parser, args):
    if not args.specs and not args.all:
        tty.die(
            "uninstall requires at least one package argument.",
            "  Use `spack uninstall --all` to uninstall ALL packages.",
        )

    # [None] here handles the --all case by forcing all specs to be returned
    specs = spack.cmd.parse_specs(args.specs) if args.specs else [None]
    uninstall_specs(args, specs)
