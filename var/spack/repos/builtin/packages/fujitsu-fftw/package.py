# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.error import SpackError
from spack.package import *
from spack.pkg.builtin.fftw import FftwBase


def target_check(spec):
    if spec.target != "a64fx":
        error_msg = "It can only be built on an A64FX machine.\n"
        raise SpackError(error_msg)


class FujitsuFftw(FftwBase):
    """FFTW (Fujitsu Optimized version) is a comprehensive collection of
    fast C routines for computing the Discrete Fourier Transform (DFT)
    and various special cases thereof.

    It is an open-source implementation of the Fast Fourier transform
    algorithm. It can compute transforms of real and complex-values
    arrays of arbitrary size and dimension.
    Fujitsu Optimized FFTW is the optimized FFTW implementation targeted
    for A64FX CPUs.

    For single precision build, please use precision value as float.
    Example : spack install fujitsufftw precision=float
    """

    _name = "fujitsu-fftw"
    homepage = "https://github.com/fujitsu/fftw3"
    url = "https://github.com/fujitsu/fftw3/archive/sve-v1.0.0.tar.gz"

    version("1.1.0", sha256="47b01a20846802041a9533a115f816b973cc9b15b3e827a2f0caffaae34a6c9d")
    version("1.0.0", sha256="b5931e352355d8d1ffeb215922f4b96de11b8585c423fceeaffbf3d5436f6f2f")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Builds a shared version of the library")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("debug", default=False, description="Builds a debug version of the library")

    depends_on("texinfo")

    provides("fftw-api@3")

    conflicts("precision=quad", when="%fj", msg="Fujitsu Compiler doesn't support quad precision")
    conflicts(
        "precision=long_double",
        when="%fj",
        msg="ARM-SVE vector instructions only works in single or double precision",
    )
    requires("%fj")

    def autoreconf(self, spec, prefix):
        if spec.target != "a64fx":
            target_check(spec)

        touch = which("touch")
        touch("ChangeLog")
        autoreconf = which("autoreconf")
        autoreconf("-ifv")

    def configure(self, spec, prefix):
        """Configure function"""
        # Base options
        options = [
            "CFLAGS=-Ofast",
            "FFLAGS=-Kfast",
            "--enable-sve",
            "--enable-armv8-cntvct-el0",
            "--enable-fma",
            "--enable-fortran",
            "--prefix={0}".format(prefix),
            "ac_cv_prog_f77_v=-###",
        ]

        if spec.satisfies("+shared"):
            options.append("--enable-shared")
        else:
            options.append("--disable-shared")

        if spec.satisfies("+openmp"):
            options.append("--enable-openmp")
            options.append("OPENMP_CFLAGS=-Kopenmp")
        else:
            options.append("--disable-openmp")

        if spec.satisfies("+threads"):
            options.append("--enable-threads")
        else:
            options.append("--disable-threads")

        if spec.satisfies("+mpi"):
            options.append("--enable-mpi")
        else:
            options.append("--disable-mpi")

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            "float": ["--enable-float"],
            "double": None,
            "long_double": ["--enable-long-double"],
            "quad": ["--enable-quad-precision"],
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable("../configure")
        for precision in self.selected_precisions:
            opts = (enable_precision[precision] or []) + options[:]
            with working_dir(precision, create=True):
                configure(*opts)
