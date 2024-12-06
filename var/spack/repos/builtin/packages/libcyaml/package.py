# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcyaml(MakefilePackage):
    """LibCYAML is a C library for reading and writing structured YAML
    documents. It is written in ISO C11 and licensed under the ISC licence."""

    homepage = "https://github.com/tlsa/libcyaml"
    url = "https://github.com/tlsa/libcyaml/archive/v1.1.0.tar.gz"

    license("ISC")

    version("1.4.1", sha256="8dbd216e1fce90f9f7cca341e5178710adc76ee360a7793ef867edb28f3e4130")
    version("1.4.0", sha256="e803fef0e254aa1f302c622c2d25cff989e04e9b2bebb7d22abd91386373122f")
    version("1.1.0", sha256="37a00ed8ec206b60a712acfd44196bef063b8f02e376d8e86f61a7007a81daea")

    depends_on("c", type="build")  # generated

    depends_on("libyaml")

    def build(self, spec, prefix):
        make("VARIANT=release")

    def install(self, spec, prefix):
        make("install", "VARIANT=release", f"PREFIX={prefix}")
