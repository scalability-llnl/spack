# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev

from spack.error import SpackError

description = "add a spec to an environment's dev-build information"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-p', '--path', help='Source location of package')

    clone_group = subparser.add_mutually_exclusive_group()
    clone_group.add_argument(
        '--no-clone', action='store_false', dest='clone', default=None,
        help='Do not clone. The package already exists at the source path')
    clone_group.add_argument(
        '--clone', action='store_true', dest='clone', default=None,
        help='Clone the package even if the path already exists')

    subparser.add_argument(
        '-f', '--force',
        help='Remove any files or directories that block cloning source code')

    arguments.add_common_arguments(subparser, ['spec'])


def develop(parser, args):
    env = ev.get_env(args, 'develop', required=True)

    if not args.spec:
        if args.clone is False:
            raise SpackError("No spec provided to spack develop command")

        # download all dev specs
        for entry in env.dev_specs:
            path = entry.get('path', spack.spec.Spec(entry['spec']).name)
            abspath = path if os.path.isabs(path) else os.path.join(
                env.path, path)

            if os.path.exists(abspath):
                msg = "Skipping developer download of %s" % entry['spec']
                msg += " because its path already exists."
                tty.msg(msg)
                continue

            stage = spack.spec.Spec(entry['spec']).package.stage
            stage.steal_source(abspath)

        if not env.dev_specs:
            tty.warn("No develop specs to download")

        return

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        raise SpackError("spack develop requires at most one named spec")

    spec = specs[0]
    if not spec.versions.concrete:
        raise SpackError("Packages to develop must have a concrete version")

    # default path is relative path to spec.name
    path = args.path or spec.name

    # get absolute path to check
    abspath = path
    if not os.path.isabs(abspath):
        abspath = os.path.join(env.path, path)

    # clone default: only if the path doesn't exist
    clone = args.clone
    if clone is None:
        clone = not os.path.exists(abspath)

    if not clone and not os.path.exists(abspath):
        raise SpackError("Provided path %s does not exist" % abspath)

    if clone and os.path.exists(abspath):
        if args.force:
            shutil.rmtree(abspath)
        else:
            msg = "Path %s already exists and cannot be cloned to." % abspath
            msg += " Use `spack develop -f` to overwrite."
            raise SpackError(msg)

    with env.write_transaction():
        changed = env.develop(spec, path, clone)
        if changed:
            env.write()
