# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pfft(AutotoolsPackage):
    """PFFT is a software library for computing massively parallel,
    fast Fourier transformations on distributed memory architectures.
    PFFT can be understood as a generalization of FFTW-MPI to
    multidimensional data decomposition."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software.php.en"
    url = (
        "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software/pfft-1.0.8-alpha.tar.gz"
    )

    license("GPL-3.0-or-later")

    version(
        "1.0.8-alpha", sha256="6c43960ad72fcff7e49b87c604c5f471fb5890f1bd11ce750ab52f035e7c5317"
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("fftw+mpi+pfft_patches")
    depends_on("mpi")

    def configure(self, spec, prefix):
        options = ["--prefix={0}".format(prefix)]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        configure = Executable("../configure")

        fftw = spec["fftw"]
        if "precision=double" in fftw:
            with working_dir("double", create=True):
                configure(*options)
        if "precision=float" in fftw:
            with working_dir("float", create=True):
                configure("--enable-float", *options)
        if "precision=long_double" in fftw:
            with working_dir("long-double", create=True):
                configure("--enable-long-double", *options)

    def build(self, spec, prefix):
        fftw = spec["fftw"]
        if "precision=double" in fftw:
            with working_dir("double"):
                make()
        if "precision=float" in fftw:
            with working_dir("float"):
                make()
        if "precision=long_double" in fftw:
            with working_dir("long-double"):
                make()

    def check(self):
        spec = self.spec
        fftw = spec["fftw"]
        if "precision=double" in fftw:
            with working_dir("double"):
                make("check")
        if "precision=float" in fftw:
            with working_dir("float"):
                make("check")
        if "precision=long_double" in fftw:
            with working_dir("long-double"):
                make("check")

    def install(self, spec, prefix):
        fftw = spec["fftw"]
        if "precision=double" in fftw:
            with working_dir("double"):
                make("install")
        if "precision=float" in fftw:
            with working_dir("float"):
                make("install")
        if "precision=long_double" in fftw:
            with working_dir("long-double"):
                make("install")
