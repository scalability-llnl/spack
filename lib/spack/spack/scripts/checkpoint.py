# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import inspect
import json
import os

import spack
import spack.environment as ev
import spack.traverse as traverse
import spack.util.crypto as crypto

_checkpoint_file = "checkpoint.json"


class Checkpoint:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, Checkpoint):
            raise ValueError(f"Can only compare to other {self.__class__}")
        return self.data == other.data

    @staticmethod
    def from_save(env):
        path = os.path.join(env.path, _checkpoint_file)
        if not os.path.exists(path):
            raise ValueError("A checkpoint does not yet exist")
        with open(path, "r") as f:
            (manifest_checksum, cfg_hashes, pkg_hashes) = json.load(f)
            data = [
                manifest_checksum,
                frozenset(tuple(x) for x in cfg_hashes),
                frozenset(tuple(x) for x in pkg_hashes),
            ]
        return Checkpoint(data)

    @staticmethod
    def from_env(env):
        data = [_checksum(env.manifest_path), get_config_hashes(), get_package_hashes(env)]
        return Checkpoint(data)

    def write(self, env):
        path = os.path.join(env.path, _checkpoint_file)
        with open(path, "w") as f:
            (manifest_checksum, cfg_hashes, pkg_hashes) = self.data
            write_data = [manifest_checksum, list(cfg_hashes), list(pkg_hashes)]
            json.dump(write_data, f)


def _get_config_scopes():
    return [
        x
        for x in spack.config.CONFIG.scopes.values()
        if not isinstance(x, spack.config.InternalConfigScope)
    ]


def _checksum(path):
    fn = crypto.hash_fun_for_algo("sha256")
    return crypto.checksum(fn, path)


def get_config_hashes():
    # packages.yaml
    # repos.yaml
    # concretize.yaml (could swap reuse behavior)
    # compilers.yaml (could change flags)
    # (not) config.yaml

    cfg_paths = set()

    scopes = _get_config_scopes()
    for scope in scopes:
        for section in ["packages", "repos", "concretizer", "compilers"]:
            cfg_path = scope.get_section_filename(section)
            if cfg_path and os.path.exists(cfg_path):
                cfg_paths.add(cfg_path)

    path_to_hash = frozenset((x, _checksum(x)) for x in cfg_paths)
    return path_to_hash


def get_package_hashes(env):
    concrete_roots = list(y for x, y in env.concretized_specs())

    package_files = set()

    for spec in traverse.traverse_nodes(concrete_roots, key=traverse.by_dag_hash):
        if spec.external:
            continue

        inheritance_hierarchy = inspect.getmro(spec.package.__class__)

        cutoff = inheritance_hierarchy.index(spack.package_base.PackageBase)

        package_files.update(inspect.getfile(x) for x in inheritance_hierarchy[:cutoff])

    path_to_hash = frozenset((x, _checksum(x)) for x in package_files)
    return path_to_hash


def update_checkpoint(env):
    new_state = Checkpoint.from_env(env)
    new_state.write(env)


def check_checkpoint(env):
    prior_state = Checkpoint.from_save(env)
    new_state = Checkpoint.from_env(env)
    if prior_state != new_state:
        return "unequal"
    else:
        return "equal"


def main():
    parser = argparse.ArgumentParser(description="Checkpoint an active env")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    subparsers.add_parser("update", help="Update checkpoint")

    subparsers.add_parser("check", help="Check if env would reconcretize differently")

    args = parser.parse_args()

    env = ev.active_environment()
    if not env:
        raise ValueError("An active env is required.")

    if args.command == "update":
        update_checkpoint(env)
    elif args.command == "check":
        print(check_checkpoint(env))


if __name__ == "__main__":
    main()
