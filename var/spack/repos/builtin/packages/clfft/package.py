# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Clfft(CMakePackage):
    """a software library containing FFT functions written in OpenCL"""

    homepage = "https://github.com/clMathLibraries/clFFT"
    url = "https://github.com/clMathLibraries/clFFT/archive/v2.12.2.tar.gz"

    license("Apache-2.0")

    version("2.12.2", sha256="e7348c146ad48c6a3e6997b7702202ad3ee3b5df99edf7ef00bbacc21e897b12")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("client", default=True, description="build client and callback client")

    depends_on("opencl@1.2:")
    depends_on("boost@1.33.0:", when="+client")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+client")

    patch(
        "https://github.com/clMathLibraries/clFFT/commit/eea7dbc888367b8dbea602ba539eb1a9cbc118d9.patch?full_index=1",
        sha256="9ee126955f0bb9469c8302d8b08672d60a493d3373dbad06bdfda0b5c7893488",
        when="@2.12.2",
    )

    root_cmakelists_dir = "src"

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            # https://github.com/clMathLibraries/clFFT/issues/237
            flags.append("-fpermissive")
        return (flags, None, None)

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_CLIENT", "client"),
            self.define_from_variant("BUILD_CALLBACK_CLIENT", "client"),
        ]
        return args
