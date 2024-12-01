# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Castep(MakefilePackage):
    """
    CASTEP is a leading code for calculating the
    properties of materials from first principles.
    Using density functional theory, it can simulate
    a wide range of properties of materials
    proprieties including energetics, structure at
    the atomic level, vibrational properties,
    electronic response properties etc.
    """

    homepage = "http://castep.org"
    url = f"file://{os.getcwd()}/CASTEP-21.11.tar.gz"
    manual_download = True

    version("21.11", sha256="d909936a51dd3dff7a0847c2597175b05c8d0018d5afe416737499408914728f")
    version(
        "19.1.1.rc2", sha256="1fce21dc604774e11b5194d5f30df8a0510afddc16daf3f8b9bbb3f62748f86a"
    )

    variant("mpi", default=True, description="Enable MPI build")
    depends_on("rsync", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api")
    depends_on("mpi", type=("build", "link", "run"), when="+mpi")

    parallel = True

    def edit(self, spec, prefix):
        if spec.satisfies("%gcc"):
            dlmakefile = FileFilter("LibSource/dl_mg-2.0.3/platforms/castep.inc")
            dlmakefile.filter(r"MPIFLAGS = -DMPI", "MPIFLAGS = -fallow-argument-mismatch -DMPI")
            if self.spec.satisfies("@20:"):
                platfile = FileFilter("obj/platforms/linux_x86_64_gfortran.mk")
            else:
                platfile = FileFilter("obj/platforms/linux_x86_64_gfortran9.0.mk")
            platfile.filter(r"^\s*OPT_CPU\s*=.*", "OPT_CPU = ")
            platfile.filter(r"^\s*FFLAGS_E\s*=.*", "FFLAGS_E = -fallow-argument-mismatch ")
        elif spec.satisfies("%intel"):
            if self.spec.satisfies("@20:"):
                platfile = FileFilter("obj/platforms/linux_x86_64_ifort.mk")
            else:
                platfile = FileFilter("obj/platforms/linux_x86_64_ifort19.mk")
            platfile.filter(r"^\s*OPT_CPU\s*=.*", "OPT_CPU = ")

    @property
    def build_targets(self):
        spec = self.spec
        targetlist = [f"PWD={self.stage.source_path}"]

        if spec.satisfies("+mpi"):
            targetlist.append("COMMS_ARCH=mpi")

        targetlist.append(f"FFTLIBDIR={spec['fftw-api'].prefix.lib}")
        targetlist.append(f"MATHLIBDIR={spec['blas'].prefix.lib}")

        if spec.satisfies("^mkl"):
            targetlist.append("FFT=mkl")
            if self.spec.satisfies("@20:"):
                targetlist.append("MATHLIBS=mkl")
            else:
                targetlist.append("MATHLIBS=mkl10")
        else:
            targetlist.append("FFT=fftw3")
            targetlist.append("MATHLIBS=openblas")

        if spec.satisfies("target=x86_64:"):
            if spec.satisfies("platform=linux"):
                if spec.satisfies("%gcc"):
                    if self.spec.satisfies("@20:"):
                        targetlist.append("ARCH=linux_x86_64_gfortran")
                    else:
                        targetlist.append("ARCH=linux_x86_64_gfortran9.0")
                if spec.satisfies("%intel"):
                    if self.spec.satisfies("@20:"):
                        targetlist.append("ARCH=linux_x86_64_ifort")
                    else:
                        targetlist.append("ARCH=linux_x86_64_ifort19")

        return targetlist

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("install", "install-tools", *self.build_targets, "INSTALL_DIR={0}".format(prefix.bin))
