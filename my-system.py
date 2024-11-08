# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.environment as ev
import spack.config as config
import spack.platforms
from spack.spec import Spec
import spack.util.spack_yaml as syaml

from llnl.util.filesystem import mkdirp

import archspec.cpu

import argparse
import pathlib
import pickle
import os


def _dump_section(section, stream):
    data = syaml.syaml_dict()
    data[section] = config.CONFIG.get_config(section, scope=None)
    syaml.dump_config(data, stream=stream, default_flow_style=False, blame=None)

def _system_pickles(dst):
    data = [
        spack.platforms.host(),
        archspec.cpu.host()
    ]
    with open(dst, "wb") as f:
        pickle.dump(data, f)

def main():
    parser = argparse.ArgumentParser(description="Collect details for simulating this system elsewhere")
    parser.add_argument("dest", help="Put all simulation resources in this dir (for target system to use)")
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

    _system_pickles(root / "arch.pkl")


if __name__ == "__main__":
    main()