# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Openmolcas(CMakePackage):
    """OpenMolcas is a quantum chemistry software package.
    The key feature of OpenMolcas is the multiconfigurational approach to
    the electronic structure."""

    homepage = "https://gitlab.com/Molcas/OpenMolcas"
    url = "https://github.com/Molcas/OpenMolcas/archive/v19.11.tar.gz"

    license("LGPL-2.1-or-later")

    version("23.06", sha256="31727161c15ea588217c6511a3007792c74c35391849fa0296c2288d836cf951")
    version("21.02", sha256="d0b9731a011562ff4740c0e67e48d9af74bf2a266601a38b37640f72190519ca")
    version("19.11", sha256="8ebd1dcce98fc3f554f96e54e34f1e8ad566c601196ee68153763b6c0a04c7b9")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Build with mpi support.")

    depends_on("hdf5")
    depends_on("lapack")
    depends_on("openblas+ilp64")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("mpi", when="+mpi")
    depends_on("globalarrays", when="+mpi")

    patch("CMakeLists.txt.patch", when="target=aarch64:")

    def setup_build_environment(self, env):
        env.set("MOLCAS", self.prefix)

    def setup_run_environment(self, env):
        env.set("MOLCAS", self.prefix)
        if self.spec.version >= Version("21.02"):
            env.append_path("PATH", self.prefix)

    def cmake_args(self):
        args = ["-DLINALG=OpenBLAS", "-DOPENBLASROOT=%s" % self.spec["openblas"].prefix]
        if "+mpi" in self.spec:
            mpi_args = [
                "-DMPI=ON",
                "-DGA=ON",
                "-DGA_INCLUDE_PATH=%s" % self.spec["globalarrays"].prefix.include,
                "-DLIBGA=%s" % os.path.join(self.spec["globalarrays"].prefix.lib, "libga.so"),
                "-DLIBARMCI=%s"
                % os.path.join(self.spec["globalarrays"].prefix.lib, "libarmci.so"),
            ]
            args.extend(mpi_args)
        return args
