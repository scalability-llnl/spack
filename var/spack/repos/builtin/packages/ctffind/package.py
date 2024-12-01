# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ctffind(AutotoolsPackage):
    """Fast and accurate defocus estimation from electron micrographs."""

    homepage = "https://grigoriefflab.umassmed.edu/ctffind4"
    url = "https://grigoriefflab.umassmed.edu/system/tdf?path=ctffind-4.1.8.tar.gz&file=1&type=node&id=26"

    license("BSD-3-Clause")

    version(
        "4.1.14",
        sha256="db17b2ebeb3c3b2b3764e42b820cd50d19ccccf6956c64257bfe5d5ba6b40cb5",
        extension="tar.gz",
    )
    version(
        "4.1.8",
        sha256="bec43c0b8d32878c740d6284ef6d9d22718c80dc62270be18d1d44e8b84b2729",
        extension="tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://grigoriefflab.umassmed.edu/system/tdf?path=ctffind-{0}.tar.gz&file=1&type=node&id=26"
        return url.format(version)

    depends_on("wxwidgets")
    depends_on("fftw-api")
    depends_on("libtiff")
    depends_on("jpeg")

    patch("configure.patch", when="@4.1.8")
    patch("no_sincos_asm.patch", when="@4.1.14 target=power9le")
    patch("no_sincos_asm.patch", when="@4.1.14 target=aarch64:")
    patch("fix_return_types.patch", when="@4.1.13:4.1.14")

    def configure_args(self):
        config_args = []

        if self.spec["fftw-api"].name in INTEL_MATH_LIBRARIES:
            config_args.extend(
                [
                    "--enable-mkl",
                    "CPPFLAGS=-I{0}".format(
                        join_path(self.spec["fftw-api"].headers.directories[0], "fftw")
                    ),
                ]
            )
        else:
            config_args.extend(
                [
                    "--disable-mkl",
                    "CPPFLAGS={0}".format(self.spec["fftw-api"].headers.include_flags),
                ]
            )

        return config_args
