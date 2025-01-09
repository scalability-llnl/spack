# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import os
import pathlib
import pickle

import archspec.cpu

from llnl.util.filesystem import mkdirp

import spack.config as config
import spack.environment as ev
import spack.platforms
import spack.solver.asp
import spack.util.spack_yaml as syaml


def _dump_section(section, stream):
    data = syaml.syaml_dict()
    data[section] = config.CONFIG.get_config(section, scope=None)
    syaml.dump_config(data, stream=stream, default_flow_style=False, blame=False)


def _system_pickles(dst):
    data = [spack.platforms.host(), archspec.cpu.host(), spack.solver.asp.all_libcs()]
    with open(dst, "wb") as f:
        pickle.dump(data, f)


def _make_env(dst_dir):
    user_specs = []

    env = ev.active_environment()
    if env:
        with env:
            user_specs = env.user_specs

    env_yaml = {
        "spack": {
            "specs": user_specs.specs_as_yaml_list,
            "view": False,
            "packages:": config.get("packages"),
            "compilers:": config.get("compilers"),
            "concretizer:": config.get("concretizer"),
        }
    }
    with open(os.path.join(dst_dir, "spack.yaml"), mode="wb") as f:
        syaml.dump_config(env_yaml, stream=f, default_flow_style=False, blame=False)


def main():
    parser = argparse.ArgumentParser(
        description="Collect details for simulating this system elsewhere"
    )
    parser.add_argument(
        "dest", help="Put all simulation resources in this dir (for target system to use)"
    )
    args = parser.parse_args()

    if os.path.exists(args.dest):
        raise ValueError(f"Dest already exists: {args.dest}")

    root = pathlib.Path(args.dest)
    cfg = root / "config"
    mkdirp(cfg)
    with open(cfg / "packages.yaml", "w") as f:
        _dump_section("packages", f)
    with open(cfg / "compilers.yaml", "w") as f:
        _dump_section("compilers", f)
    with open(cfg / "concretizer.yaml", "w") as f:
        _dump_section("concretizer", f)

    _make_env(root)
    _system_pickles(root / "arch.pkl")


if __name__ == "__main__":
    main()
