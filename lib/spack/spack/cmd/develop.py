# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
from typing import Optional

import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.fetch_strategy
import spack.repo
import spack.spec
import spack.stage
import spack.util.path
import spack.version
from spack.cmd.common import arguments
from spack.error import SpackError

description = "add a spec to an environment's dev-build information"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument("-p", "--path", help="source location of package")
    subparser.add_argument("-b", "--build-directory", help="build directory for the package")

    clone_group = subparser.add_mutually_exclusive_group()
    clone_group.add_argument(
        "--no-clone",
        action="store_false",
        dest="clone",
        default=None,
        help="do not clone, the package already exists at the source path",
    )
    clone_group.add_argument(
        "--clone",
        action="store_true",
        dest="clone",
        default=True,
        help="clone the package even if the path already exists",
    )

    subparser.add_argument(
        "-f", "--force", help="remove any files or directories that block cloning source code"
    )

    subparser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="traverse edges of the graph to mark everything up to the root as a develop spec",
    )

    arguments.add_common_arguments(subparser, ["spec"])


def _update_config(spec, path):
    find_fn = lambda section: spec.name in section

    entry = {"spec": str(spec)}
    if path != spec.name:
        entry["path"] = path

    def change_fn(section):
        section[spec.name] = entry

    spack.config.change_or_add("develop", find_fn, change_fn)


def _retrieve_develop_source(spec: spack.spec.Spec, abspath: str) -> None:
    # "steal" the source code via staging API. We ask for a stage
    # to be created, then copy it afterwards somewhere else. It would be
    # better if we can create the `source_path` directly into its final
    # destination.
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    # We construct a package class ourselves, rather than asking for
    # Spec.package, since Spec only allows this when it is concrete
    package = pkg_cls(spec)
    source_stage: spack.stage.Stage = package.stage[0]
    if isinstance(source_stage.fetcher, spack.fetch_strategy.GitFetchStrategy):
        source_stage.fetcher.get_full_repo = True
        # If we retrieved this version before and cached it, we may have
        # done so without cloning the full git repo; likewise, any
        # mirror might store an instance with truncated history.
        source_stage.default_fetcher_only = True

    source_stage.fetcher.set_package(package)
    package.stage.steal_source(abspath)


def _impl_develop(spec: spack.spec.Spec, src_path: str, clone: bool = True, force: bool = False):
    """
    Implementation of developing a spec
    """
    version = spec.versions.concrete_range_as_version
    if not version:
        # look up the maximum version so infintiy versions are preferred for develop
        version = max(spec.package_class.versions.keys())
        tty.msg(f"Defaulting to highest version: {spec.name}@{version}")
    spec.versions = spack.version.VersionList([version])

    if clone is None:
        clone = not os.path.exists(src_path)

    if clone:
        _clone(spec, src_path, force)

    if not clone and not os.path.exists(src_path):
        raise SpackError(f"Provided path {src_path} does not exist")


def _update_env(
    env: spack.environment.Environment,
    spec: spack.spec.Spec,
    path: str,
    build_dir: Optional[str] = None,
):
    tty.debug(f"Updating develop config for {env.name} transactionally")
    with env.write_transaction():
        if build_dir is not None:
            spack.config.add(
                f"packages:{spec.name}:package_attributes:build_directory:{build_dir}",
                env.scope_name,
            )
        _update_config(spec, path)


def _clone(spec: spack.spec.Spec, abspath: str, force: bool = False):
    if os.path.exists(abspath):
        if force:
            shutil.rmtree(abspath)
        else:
            msg = f"Skipping developer download of {spec.name}"
            msg += f" because its path {abspath} already exists."
            tty.msg(msg)
            return

    # cloning can take a while and it's nice to get a message for the longer clones
    tty.msg(f"Cloning source code for {spec}")
    _retrieve_develop_source(spec, abspath)


def _abs_code_path(
    env: spack.environment.Environment, spec: spack.spec.Spec, path: Optional[str] = None
):
    src_path = path if path else spec.name
    return spack.util.path.canonicalize_path(src_path, default_wd=env.path)


def _code_path(spec: spack.spec.Spec, path: Optional[str] = None):
    return path if path else spec.name


def _dev_spec_generator(args, env):
    """generator to get develop specs and src path"""
    if not args.spec:
        if args.clone is False:
            raise SpackError("No spec provided to spack develop command")
        else:
            for name, entry in env.dev_specs.items():
                path = entry.get("path", name)
                abspath = spack.util.path.canonicalize_path(path, default_wd=env.path)
                # Both old syntax `spack develop pkg@x` and new syntax `spack develop pkg@=x`
                # are currently supported.
                spec = spack.spec.parse_with_version_concrete(entry["spec"])
                yield spec, abspath, False
    else:
        specs = spack.cmd.parse_specs(args.spec)
        if (args.path or args.build_directory) and len(specs) > 1:
            raise SpackError(
                "spack develop requires at most one named spec when using the --path or --build-directory arguments"
            )
        else:
            for spec in specs:
                yield spec, _abs_code_path(env, spec, args.path), True


def develop(parser, args):
    env = spack.cmd.require_active_env(cmd_name="develop")

    # only update yaml if this is a write operation
    update_config = bool(args.spec)

    for spec, abspath, update_config in _dev_spec_generator(args, env):
        if args.recursive:
            concrete_specs = env.all_matching_specs(spec)
            if not concrete_specs:
                tty.msg(
                    "No matching specs found in the environment. "
                    "Recursive develop requires a concretized environment"
                )
            else:
                for s in concrete_specs:
                    for parent in s.traverse_edges(direction="parents", root=True):
                        tty.debug(f"Recursive develop for {parent_args.spec}")
                        _impl_develop(
                            parent,
                            _abs_code_path(env, parent, args.path),
                            clone=args.clone,
                            force=args.force,
                        )
                        if update_config:
                            _update_env(
                                env, parent, _code_path(parent, args.path), args.build_directory
                            )
                return
        else:
            _impl_develop(spec, abspath, clone=args.clone, force=args.force)
            if update_config:
                _update_env(env, spec, _code_path(spec, args.path), args.build_directory)
