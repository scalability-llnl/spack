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
import spack.solver.asp  # noqa: F401
import spack.util.spack_yaml as syaml


def _dump_section(section, stream):
    data = syaml.syaml_dict()
    data[section] = config.CONFIG.get_config(section, scope=None)
    syaml.dump_config(data, stream=stream, default_flow_style=False, blame=False)


def _system_pickles(dst):
    import spack.compilers
    import spack.config

    compiler_save_libc = dict()
    for cmp in spack.compilers.all_compilers_from(spack.config.CONFIG):
        if spack.solver.asp.using_libc_compatibility() and cmp.default_libc:
            compiler_save_libc[str(cmp.spec)] = cmp.default_libc

    data = [
        spack.platforms.host(),
        archspec.cpu.host(),
        spack.solver.asp.all_libcs(),
        compiler_save_libc,
    ]
    with open(dst, "wb") as f:
        pickle.dump(data, f)


class MapLibc:
    def __init__(self, compiler_save_libc):
        self.compiler_save_libc = compiler_save_libc

    def simulate_default_libc(self, obj):
        return self.compiler_save_libc.get(str(obj.spec), None)


def _simulate_system(state_dir):
    import pickle

    import spack.compiler
    import spack.platforms
    import spack.solver.asp

    with open(os.path.join(state_dir, "arch.pkl"), "rb") as f:
        # spack.platforms.host()
        # archspec.cpu.host()
        # spack.solver.asp.all_libcs()
        # compiler_save_libc
        data = pickle.load(f)
        spack.platforms.host = lambda: data[0]
        archspec.cpu.host = lambda: data[1]
        spack.solver.asp.all_libcs = lambda: data[2]
        spack.solver.asp.c_compiler_runs = lambda x: True
        spack.compiler.Compiler._simulated_libc = data[3]


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


def generate(args):
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


def use(args):
    import spack.bootstrap as bootstrap
    import spack.main

    with bootstrap.ensure_bootstrap_configuration():
        bootstrap.ensure_clingo_importable_or_raise()

    _simulate_system(args.source)
    e = ev.Environment(args.source)
    with e:
        spack.main.SpackCommand(args.command[0])(*args.command[1:])


def main():
    parser = argparse.ArgumentParser(description="For simulating other systems/configs")

    sp = parser.add_subparsers(metavar="SUBCOMMAND", dest="simulate_command")

    gen_parser = sp.add_parser(
        "generate", help="Put all simulation resources in this dir (for target system to use)"
    )
    gen_parser.add_argument(
        "dest", help="Put all simulation resources in this dir (for target system to use)"
    )

    use_parser = sp.add_parser("use", help="Use a generated system")
    use_parser.add_argument("source", help="Directory generated by `my-system.py generate`")
    use_parser.add_argument("command", nargs=argparse.REMAINDER, help="command to run")

    args = parser.parse_args()

    action = {"generate": generate, "use": use}
    action[args.simulate_command](args)


if __name__ == "__main__":
    main()
