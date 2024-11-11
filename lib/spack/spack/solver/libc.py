# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import os
import shutil
import tempfile
import typing
from typing import Optional

import llnl.util.tty as tty

import spack.util.libc

if typing.TYPE_CHECKING:
    import spack.spec


class CompilerPropertyDetector:

    _CACHE = {}

    def __init__(self, compiler_spec: "spack.spec.Spec"):
        assert compiler_spec.external, "only external compiler specs are allowed, so far"
        assert compiler_spec.concrete, "only concrete compiler specs are allowed, so far"
        self.spec = compiler_spec

    @contextlib.contextmanager
    def compiler_environment(self):
        """Sets the environment to run this compiler"""
        import spack.schema.environment
        import spack.util.module_cmd

        # Avoid modifying os.environ if possible.
        environment = self.spec.extra_attributes.get("environment", {})
        modules = self.spec.external_modules or []
        if not self.spec.external_modules and not environment:
            yield
            return

        # store environment to replace later
        backup_env = os.environ.copy()

        try:
            # load modules and set env variables
            for module in modules:
                spack.util.module_cmd.load_module(module)

            # apply other compiler environment changes
            spack.schema.environment.parse(environment).apply_modifications()

            yield
        finally:
            # Restore environment regardless of whether inner code succeeded
            os.environ.clear()
            os.environ.update(backup_env)

    def _compile_dummy_c_source(self) -> Optional[str]:
        import spack.util.executable

        assert self.spec.external, "only external compiler specs are allowed, so far"
        compiler_pkg = self.spec.package
        cc = compiler_pkg.cc if compiler_pkg.cc else compiler_pkg.cxx
        if not cc:  # or not self.spec.verbose_flag:
            return None

        try:
            tmpdir = tempfile.mkdtemp(prefix="spack-implicit-link-info")
            fout = os.path.join(tmpdir, "output")
            fin = os.path.join(tmpdir, "main.c")

            with open(fin, "w") as csource:
                csource.write(
                    "int main(int argc, char* argv[]) { (void)argc; (void)argv; return 0; }\n"
                )
            cc_exe = spack.util.executable.Executable(cc)

            # FIXME (compiler as nodes): this operation should be encapsulated somewhere else
            compiler_flags = self.spec.extra_attributes.get("flags", {})
            for flag_type in [
                "cflags" if cc == compiler_pkg.cc else "cxxflags",
                "cppflags",
                "ldflags",
            ]:
                current_flags = compiler_flags.get(flag_type, "").strip()
                if current_flags:
                    cc_exe.add_default_arg(*current_flags.split(" "))

            with self.compiler_environment():
                return cc_exe("-v", fin, "-o", fout, output=str, error=str)
        except spack.util.executable.ProcessError as pe:
            tty.debug(f"ProcessError: Command exited with non-zero status: {pe.long_message}")
            return None
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def compiler_verbose_output(self):
        key = self.spec.dag_hash()
        if key not in self._CACHE:
            self._CACHE[key] = self._compile_dummy_c_source()
        return self._CACHE[key]

    def default_libc(self) -> Optional["spack.spec.Spec"]:
        """Determine libc targeted by the compiler from link line"""
        output = self.compiler_verbose_output()

        if not output:
            return None

        dynamic_linker = spack.util.libc.parse_dynamic_linker(output)

        if not dynamic_linker:
            return None

        return spack.util.libc.libc_from_dynamic_linker(dynamic_linker)
