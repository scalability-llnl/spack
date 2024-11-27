# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_fluidsim_core import PyFluidsimCore


class PyFluidsim(PythonPackage):
    """Framework for studying fluid dynamics with simulations."""

    pypi = "fluidsim/fluidsim-0.8.3.tar.gz"

    maintainers("paugier")
    license("CECILL", checked_by="paugier")

    version("0.8.3", sha256="ff3df8c2e8c96a694b5656125e778fc5f6561699bae3b264cbb75e2070b94169")
    version("0.8.2", sha256="eb36c2d7d588fbb088af026683a12bb14aa126bbbc91b999009130d6cb7920f9")
    version("0.8.1", sha256="44c70f388c429856f5df24705cddb2e024d7d1376d2153e113ef111af90b857b")
    version("0.8.0", sha256="01f6d489ce44fe4dc47357506ba227ae0e87b346758d8f067c13f319d0a9a881")

    variant("native", default=False, description="Compile with -march=native and -Ofast.")

    with default_args(type=("build", "run")):
        extends("python@3.9:")
        depends_on("py-transonic@0.6.4:")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-pythran@0.9.7:")

    with default_args(type="run"):
        for _v in PyFluidsimCore.versions:
            depends_on(f"py-fluidsim-core@{_v}", when=f"@{_v}")
        depends_on("py-fluidfft@0.4.0:")
        depends_on("py-xarray")
        depends_on("py-rich")
        depends_on("py-scipy")

    def config_settings(self, spec, prefix):
        settings = {"setup-args": {"-Dnative": spec.variants["native"].value}}
        return settings
