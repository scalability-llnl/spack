# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.cmd.common.deployment as deployment
import spack.environment as ev
import spack.store
from spack.filesystem_view import YamlFilesystemView
from spack.graph import topological_sort

description = "deactivate a package extension"
section = "extensions"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="run deactivation even if spec is NOT currently activated")
    subparser.add_argument(
        '-v', '--view', metavar='VIEW', type=str,
        help="the view to operate on")
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="deactivate all extensions of an extendable package, or "
        "deactivate an extension AND its dependencies")
    arguments.add_common_arguments(subparser, ['installed_spec'])


def deactivate(parser, args):
    deployment.confirm_command_if_deployment('deactivate')

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        tty.die("deactivate requires one spec.  %d given." % len(specs))

    env = ev.get_env(args, 'deactivate')
    spec = spack.cmd.disambiguate_spec(specs[0], env)
    pkg = spec.package

    if args.view:
        target = args.view
    elif pkg.is_extension:
        target = pkg.extendee_spec.prefix
    elif pkg.extendable:
        target = spec.prefix

    view = YamlFilesystemView(target, spack.store.layout)

    if args.all:
        if pkg.extendable:
            tty.msg("Deactivating all extensions of %s" % pkg.spec.short_spec)
            ext_pkgs = spack.store.db.activated_extensions_for(
                spec, view.extensions_layout)

            for ext_pkg in ext_pkgs:
                ext_pkg.spec.normalize()
                if ext_pkg.is_activated(view):
                    ext_pkg.do_deactivate(view, force=True)

        elif pkg.is_extension:
            if not args.force and \
               not spec.package.is_activated(view):
                tty.die("%s is not activated." % pkg.spec.short_spec)

            tty.msg("Deactivating %s and all dependencies." %
                    pkg.spec.short_spec)

            topo_order = topological_sort(spec)
            index = spec.index()

            for name in topo_order:
                espec = index[name]
                epkg = espec.package
                if epkg.extends(pkg.extendee_spec):
                    if epkg.is_activated(view) or args.force:
                        epkg.do_deactivate(view, force=args.force)

        else:
            tty.die(
                "spack deactivate --all requires an extendable package "
                "or an extension.")

    else:
        if not pkg.is_extension:
            tty.die("spack deactivate requires an extension.",
                    "Did you mean 'spack deactivate --all'?")

        if not args.force and \
           not spec.package.is_activated(view):
            tty.die("Package %s is not activated." % specs[0].short_spec)

        spec.package.do_deactivate(view, force=args.force)
