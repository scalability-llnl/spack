# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GamessRiMp2Miniapp(MakefilePackage):
    """The GAMESS RI-MP2 mini-app computes the correlation energy with the
    Hartree-Fock energy and wave-function given as inputs. The inputs
    were generated from GAMESS."""

    tags = ["proxy-app"]

    homepage = "https://github.com/jkwack/GAMESS_RI-MP2_MiniApp"
    url = "https://github.com/jkwack/GAMESS_RI-MP2_MiniApp/archive/1.5.tar.gz"

    version("1.5", sha256="0ff4e8e556caa99ce1ab85c53e78932a32d2e2fa3c5d883fa321d5000f8a731e")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("lapack")

    build_directory = "build_and_run"

    @property
    def build_targets(self):
        targets = [
            "rimp2-serial",
            "SDIR=../source",
            "FFLAGS_SERIAL=-cpp " + self.compiler.openmp_flag,
            "LDFLAGS_ESSL={0}".format(self.spec["lapack"].libs.ld_flags),
        ]

        return targets

    def edit(self, spec, prefix):
        with working_dir("build_and_run"):
            copy("Makefile_OLCF", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("build_and_run"):
            install("rimp2-serial", prefix.bin)
