# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Ethminer(CMakePackage):
    """The ethminer is an Ethereum GPU mining worker."""

    homepage = "https://github.com/ethereum-mining/ethminer"
    url = "https://github.com/ethereum-mining/ethminer/archive/v0.12.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.12.0", sha256="71122c8aa1be2c29e46d7f07961fa760b1eb390e4d9a2a21cf900f6482a8755a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("opencl", default=True, description="Enable OpenCL mining.")
    variant("cuda", default=False, description="Enable CUDA mining.")
    variant("stratum", default=True, description="Build with Stratum protocol support.")

    depends_on("python")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("json-c")
    depends_on("curl")
    depends_on("zlib-api")
    depends_on("cuda", when="+cuda")
    depends_on("mesa", when="+opencl")

    def cmake_args(self):
        return [
            self.define_from_variant("ETHASHCL", "opencl"),
            self.define_from_variant("ETHASHCUDA", "cuda"),
            self.define_from_variant("ETHSTRATUM", "stratum"),
        ]
