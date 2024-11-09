# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Libpulsar(CMakePackage):
    """libpulsar is a C/C++ client library implementation of the Apache Pulsar
    protocol."""

    homepage = "https://github.com/apache/pulsar"
    url = "https://github.com/apache/pulsar/archive/v2.7.0.tar.gz"

    maintainers("aahmed-se")

    license("Apache-2.0")

    version("2.7.0", sha256="5bf8e5115075e12c848a9e4474cd47067c3200f7ff13c45f624f7383287e8e5e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zstd")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("protobuf")
    depends_on("pkgconfig")
    depends_on("openssl")
    depends_on("cmake @3.14:", type="build")
    depends_on("curl", type=("build", "link"))

    root_cmakelists_dir = "pulsar-client-cpp"

    def cmake_args(self):
        args = ["-DBUILD_PYTHON_WRAPPER=OFF", "-DBUILD_TESTS=OFF"]
        return args
