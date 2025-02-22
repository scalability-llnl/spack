# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty
from llnl.util.link_tree import MergeConflictError

import spack.cmd
import spack.environment as ev
import spack.schema.projections
import spack.store
from spack import traverse
from spack.config import validate
from spack.filesystem_view import YamlFilesystemView
from spack.util import spack_yaml as s_yaml

description = "Create a view based on all specs in an environment"
section = "environments"
level = "short"


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
        "--projection-file",
        dest="projection_file",
        type=spack.cmd.extant_file,
        help="initialize view using projections from file",
    )
    sp.add_argument("-i", "--ignore-conflicts", action="store_true")

    sp.add_argument("path", nargs=1, help="path to file system view directory")


def _specs_for_view(env):
    deptype = ("link", "run")

    concrete_roots = env.concrete_roots()

    specs = traverse.traverse_nodes(
        concrete_roots, order="topo", deptype=deptype, key=traverse.by_dag_hash
    )

    selected = list()
    for x in specs:
        if not x.installed:
            continue
        if hasattr(x.package, "tags") and "runtime" in x.package.tags:
            continue
        selected.append(x)

    return selected


def env_view(parser, args):
    path = args.path[0]

    if args.projection_file:
        with open(args.projection_file, "r") as f:
            projections_data = s_yaml.load(f)
            validate(projections_data, spack.schema.projections.schema)
            ordered_projections = projections_data["projections"]
    else:
        ordered_projections = {}

    view = YamlFilesystemView(
        path,
        spack.store.STORE.layout,
        projections=ordered_projections,
        ignore_conflicts=getattr(args, "ignore_conflicts", False),
        link_type="symlink",
        verbose=args.verbose,
    )

    env = ev.active_environment()
    if not env:
        tty.die("View creation requires specs unless you are in an environment")
    specs = _specs_for_view(env)

    try:
        view.add_specs(*specs, with_dependencies=False, exclude=args.exclude)
    except MergeConflictError:
        tty.info(
            "Some file blocked the merge, adding the '-i' flag will "
            "ignore this conflict. For more information see e.g. "
            "https://github.com/spack/spack/issues/9029"
        )
        raise
