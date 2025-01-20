# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import llnl.util.filesystem
import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.fetch_strategy
import spack.mirrors.mirror
import spack.repo
import spack.spec
import spack.stage
import spack.util.compression
import spack.util.path
import spack.util.url
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
        default=None,
        help="clone the package even if the path already exists",
    )

    subparser.add_argument(
        "-f", "--force", help="remove any files or directories that block cloning source code"
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


def _retrieve_develop_from_cache(spec, dst):
    """Check mirrors for a develop/ subdir.

    Other than this check, mirrors are generally bypassed when
    retrieving source for developed packages.
    """
    mirrors = spack.mirrors.mirror.MirrorCollection(source=True).values()
    # Note: stages have a notion of one "main" download site, with
    # possibly many alternatives. It doesn't quite fit the model of
    # cached `spack develop` packages
    for mirror in mirrors:
        if not mirror.fetch_url.startswith("file://"):
            continue
        mirror_root = spack.util.url.local_file_path(mirror.fetch_url)
        dev_cache_id = spec.format_path("{name}-{version}")
        where_it_might_be = os.path.join(mirror_root, "develop", dev_cache_id) + ".tar.gz"
        if os.path.exists(where_it_might_be):
            llnl.util.filesystem.mkdirp(dst)
            decompress_single_dir_archive_into(where_it_might_be, dst)
            return True

    return False


def decompress_single_dir_archive_into(archive_file, dst):
    """You have a /path/to/archive.tar.gz

    It expands to x/...
    We want all of ... (but not x) in `dst`
    """
    import llnl.util.filesystem

    import spack.stage

    decompressor = spack.util.compression.decompressor_for(archive_file)

    with spack.stage.Stage("decompress") as stage:
        with llnl.util.filesystem.exploding_archive_catch(stage):
            decompressor(archive_file)
        llnl.util.filesystem.mv_contents_from(stage.source_path, dst)


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


def develop(parser, args):
    # Note: we could put develop specs in any scope, but I assume
    # users would only ever want to do this for either (a) an active
    # env or (b) a specified config file (e.g. that is included by
    # an environment)
    # TODO: when https://github.com/spack/spack/pull/35307 is merged,
    # an active env is not required if a scope is specified
    env = spack.cmd.require_active_env(cmd_name="develop")
    if not args.spec:
        if args.clone is False:
            raise SpackError("No spec provided to spack develop command")

        # download all dev specs
        for name, entry in env.dev_specs.items():
            path = entry.get("path", name)
            abspath = spack.util.path.canonicalize_path(path, default_wd=env.path)

            if os.path.exists(abspath):
                msg = "Skipping developer download of %s" % entry["spec"]
                msg += " because its path already exists."
                tty.msg(msg)
                continue

            # Both old syntax `spack develop pkg@x` and new syntax `spack develop pkg@=x`
            # are currently supported.
            spec = spack.spec.parse_with_version_concrete(entry["spec"])
            if not _retrieve_develop_from_cache(spec, abspath):
                _retrieve_develop_source(spec, abspath)

        if not env.dev_specs:
            tty.warn("No develop specs to download")

        return

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        raise SpackError("spack develop requires at most one named spec")

    spec = specs[0]

    version = spec.versions.concrete_range_as_version
    if not version:
        # look up the maximum version so infintiy versions are preferred for develop
        version = max(spec.package_class.versions.keys())
        tty.msg(f"Defaulting to highest version: {spec.name}@{version}")
    spec.versions = spack.version.VersionList([version])

    # If user does not specify --path, we choose to create a directory in the
    # active environment's directory, named after the spec
    path = args.path or spec.name
    if not os.path.isabs(path):
        abspath = spack.util.path.canonicalize_path(path, default_wd=env.path)
    else:
        abspath = path

    # clone default: only if the path doesn't exist
    clone = args.clone
    if clone is None:
        clone = not os.path.exists(abspath)

    if not clone and not os.path.exists(abspath):
        raise SpackError("Provided path %s does not exist" % abspath)

    if clone:
        if os.path.exists(abspath):
            if args.force:
                shutil.rmtree(abspath)
            else:
                msg = "Path %s already exists and cannot be cloned to." % abspath
                msg += " Use `spack develop -f` to overwrite."
                raise SpackError(msg)

        if not _retrieve_develop_from_cache(spec, abspath):
            _retrieve_develop_source(spec, abspath)

    tty.debug("Updating develop config for {0} transactionally".format(env.name))
    with env.write_transaction():
        if args.build_directory is not None:
            spack.config.add(
                "packages:{}:package_attributes:build_directory:{}".format(
                    spec.name, args.build_directory
                ),
                env.scope_name,
            )
        _update_config(spec, path)
