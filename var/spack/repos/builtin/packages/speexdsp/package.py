# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Speexdsp(AutotoolsPackage):
    """SpeexDSP is a patent-free, Open Source/Free Software DSP library."""

    homepage = "https://github.com/xiph/speexdsp"
    url = "https://github.com/xiph/speexdsp/archive/SpeexDSP-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version("1.2.1", sha256="d17ca363654556a4ff1d02cc13d9eb1fc5a8642c90b40bd54ce266c3807b91a7")
    version("1.2.0", sha256="d7032f607e8913c019b190c2bccc36ea73fc36718ee38b5cdfc4e4c0a04ce9a4")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("fftw-api")

    patch("mkl.patch")

    def patch(self):
        filter_file(
            "libspeexdsp_la_LIBADD = $(LIBM)",
            "libspeexdsp_la_LIBADD = $(LIBM) $(FFT_LIBS)",
            "libspeexdsp/Makefile.am",
            string=True,
        )

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = []

        if "intel-mkl" in self.spec:
            # get the blas libs explicitly to avoid scalapack getting returned
            args.extend(
                [
                    "--with-fft=proprietary-intel-mkl",
                    "CPPFLAGS={0}".format(self.spec["intel-mkl"].headers.cpp_flags),
                    "LDFLAGS={0}".format(self.spec["blas"].libs.ld_flags),
                ]
            )
        elif "fftw" in self.spec:
            args.append("--with-fft=gpl-fftw3")

        return args
