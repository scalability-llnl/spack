# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libcerf(AutotoolsPackage, SourceforgePackage):
    """A self-contained C library providing complex error functions, based
    on Faddeeva's plasma dispersion function w(z). Also provides Dawson's
    integral and Voigt's convolution of a Gaussian and a Lorentzian

    """

    homepage = "https://sourceforge.net/projects/libcerf/"
    sourceforge_mirror_path = "libcerf/libcerf-1.3.tgz"

    version("1.3", sha256="d7059e923d3f370c89fb4d19ed4f827d381bc3f0e36da5595a04aeaaf3e6a859")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def configure_args(self):
        spec = self.spec
        options = []
        # Clang reports unused functions as errors, see
        # http://clang.debian.net/status.php?version=3.8.1&key=UNUSED_FUNCTION
        if spec.satisfies("%clang") or spec.satisfies("%apple-clang"):
            options.append("CFLAGS=-Wno-unused-function")
        # fujitsu compiler has a error about unused functions too.
        if spec.satisfies("%fj"):
            options.append("CFLAGS=-Wno-unused-function")

        return options
