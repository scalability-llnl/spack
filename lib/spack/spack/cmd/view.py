# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Produce a "view" of a Spack DAG.

A "view" is file hierarchy representing the union of a number of
Spack-installed package file hierarchies.  The union is formed from:

- specs resolved from the package names given by the user (the seeds)

- all dependencies of the seeds unless user specifies `--no-dependencies`

- less any specs with names matching the regular expressions given by
  `--exclude`

The `view` can be built and tore down via a number of methods (the "actions"):

- symlink :: a file system view which is a directory hierarchy that is
  the union of the hierarchies of the installed packages in the DAG
  where installed files are referenced via symlinks.

- hardlink :: like the symlink view but hardlinks are used.

- statlink :: a view producing a status report of a symlink or
  hardlink view.

The file system view concept is imspired by Nix, implemented by
brett.viren@gmail.com ca 2016.

All operations on views are performed via proxy objects such as
YamlFilesystemView.

"""
import sys

import llnl.util.tty as tty
from llnl.util.link_tree import MergeConflictError

import spack.cmd
import spack.environment as ev
import spack.filesystem_view as fsv
import spack.schema.projections
import spack.store
from spack.config import validate
from spack.util import spack_yaml as s_yaml

description = "project packages to a compact naming scheme on the filesystem"
section = "environments"
level = "short"

actions_link = ["symlink", "add", "soft", "hardlink", "hard", "copy", "relocate"]
actions_remove = ["remove", "rm"]
actions_status = ["statlink", "status", "check"]


def disambiguate_in_view(specs, view):
    """
    When dealing with querying actions (remove/status) we only need to
    disambiguate among specs in the view
    """
    view_specs = set(view.get_all_specs())

    def squash(matching_specs):
        if not matching_specs:
            tty.die("Spec matches no installed packages.")

        matching_in_view = [ms for ms in matching_specs if ms in view_specs]
        spack.cmd.ensure_single_spec_or_die("Spec", matching_in_view)

        return matching_in_view[0] if matching_in_view else matching_specs[0]

    # make function always return a list to keep consistency between py2/3
    return list(map(squash, map(spack.store.STORE.db.query, specs)))


def setup_parser(sp):
    setup_parser.parser = sp

    sp.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="if not verbose only warnings/errors will be printed",
    )
    sp.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="exclude packages with names matching the given regex pattern",
    )
    sp.add_argument(
        "-d",
        "--dependencies",
        choices=["true", "false", "yes", "no"],
        default="true",
        help="link/remove/list dependencies",
    )

    ssp = sp.add_subparsers(metavar="ACTION", dest="action")

    specs_opts = dict(metavar="spec", action="store", help="seed specs of the packages to view")

    # The action parameterizes the command but in keeping with Spack
    # patterns we make it a subcommand.
    file_system_view_actions = {
        "symlink": ssp.add_parser(
            "symlink",
            aliases=["add", "soft"],
            help="add package files to a filesystem view via symbolic links",
        ),
        "hardlink": ssp.add_parser(
            "hardlink",
            aliases=["hard"],
            help="add packages files to a filesystem view via hard links",
        ),
        "copy": ssp.add_parser(
            "copy",
            aliases=["relocate"],
            help="add package files to a filesystem view via copy/relocate",
        ),
        "remove": ssp.add_parser(
            "remove", aliases=["rm"], help="remove packages from a filesystem view"
        ),
        "statlink": ssp.add_parser(
            "statlink",
            aliases=["status", "check"],
            help="check status of packages in a filesystem view",
        ),
    }

    # All these options and arguments are common to every action.
    for cmd, act in file_system_view_actions.items():
        act.add_argument("path", nargs=1, help="path to file system view directory")

        if cmd in ("symlink", "hardlink", "copy"):
            # invalid for remove/statlink, for those commands the view needs to
            # already know its own projections.
            act.add_argument(
                "--projection-file",
                dest="projection_file",
                type=spack.cmd.extant_file,
                help="initialize view using projections from file",
            )

        if cmd == "remove":
            grp = act.add_mutually_exclusive_group(required=True)
            act.add_argument(
                "--no-remove-dependents",
                action="store_true",
                help="do not remove dependents of specified specs",
            )

            # with all option, spec is an optional argument
            so = specs_opts.copy()
            so["nargs"] = "*"
            so["default"] = []
            grp.add_argument("specs", **so)
            grp.add_argument("-a", "--all", action="store_true", help="act on all specs in view")

        elif cmd == "statlink":
            so = specs_opts.copy()
            so["nargs"] = "*"
            act.add_argument("specs", **so)

        else:
            # without all option, spec is required
            so = specs_opts.copy()
            so["nargs"] = "+"
            act.add_argument("specs", **so)

    for cmd in ["symlink", "hardlink", "copy"]:
        act = file_system_view_actions[cmd]
        act.add_argument("-i", "--ignore-conflicts", action="store_true")

    return


def view(parser, args):
    """Produce a view of a set of packages."""

    if sys.platform == "win32" and args.action in ("hardlink", "hard"):
        # Hard-linked views are not yet allowed on Windows.
        # See https://github.com/spack/spack/pull/46335#discussion_r1757411915
        tty.die("Hard linking is not supported on Windows. Please use symlinks or copy methods.")

    specs = spack.cmd.parse_specs(args.specs)
    path = args.path[0]

    if args.action in actions_link and args.projection_file:
        # argparse confirms file exists
        with open(args.projection_file, "r") as f:
            projections_data = s_yaml.load(f)
            validate(projections_data, spack.schema.projections.schema)
            ordered_projections = projections_data["projections"]
    else:
        ordered_projections = {}

    # What method are we using for this view
    link_type = args.action if args.action in actions_link else "symlink"
    view = fsv.YamlFilesystemView(
        path,
        spack.store.STORE.layout,
        projections=ordered_projections,
        ignore_conflicts=getattr(args, "ignore_conflicts", False),
        link_type=link_type,
        verbose=args.verbose,
    )

    # Process common args and specs
    if getattr(args, "all", False):
        specs = view.get_all_specs()
        if len(specs) == 0:
            tty.warn("Found no specs in %s" % path)

    elif args.action in actions_link:
        # only link commands need to disambiguate specs
        env = ev.active_environment()
        specs = [spack.cmd.disambiguate_spec(s, env) for s in specs]

    elif args.action in actions_status:
        # no specs implies all
        if len(specs) == 0:
            specs = view.get_all_specs()
        else:
            specs = disambiguate_in_view(specs, view)

    else:
        # status and remove can map a partial spec to packages in view
        specs = disambiguate_in_view(specs, view)

    with_dependencies = args.dependencies.lower() in ["true", "yes"]

    # Map action to corresponding functionality
    if args.action in actions_link:
        try:
            view.add_specs(*specs, with_dependencies=with_dependencies, exclude=args.exclude)
        except MergeConflictError:
            tty.info(
                "Some file blocked the merge, adding the '-i' flag will "
                "ignore this conflict. For more information see e.g. "
                "https://github.com/spack/spack/issues/9029"
            )
            raise

    elif args.action in actions_remove:
        view.remove_specs(
            *specs,
            with_dependencies=with_dependencies,
            exclude=args.exclude,
            with_dependents=not args.no_remove_dependents,
        )

    elif args.action in actions_status:
        view.print_status(*specs, with_dependencies=with_dependencies)

    else:
        tty.error('Unknown action: "%s"' % args.action)
