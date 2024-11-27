# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Foundationdb(CMakePackage):
    """FoundationDB is a distributed database designed to handle large
    volumes of structured data across clusters of commodity servers.
    It organizes data as an ordered key-value store and employs ACID
    transactions for all operations."""

    homepage = "https://www.foundationdb.org/"
    url = "https://github.com/apple/foundationdb/archive/6.3.3.tar.gz"

    license("Apache-2.0")

    version("6.3.4", sha256="80a3d7f005b42e7b63abd27728f4d7f4088eea65aafb6942424c97a704b60fd4")
    version("6.3.3", sha256="1fd46c2281ea283d17fc5044c57a3dbef371a3ed31733abf38610c459a4ed79d")
    version("6.3.2", sha256="e930510937f8db3aba73262494eedcafb75cd3f523a8b5cd8254250af5da6086")
    version("6.3.1", sha256="1162cf93f72c809fa43f0ec6722b01169a9522ec5de95aa52a76b485009a3c95")
    version("6.3.0", sha256="307f99014fe0bb8fbb05399c303f5a7a5007ceee207810857a7b5e6a7df7c8e8")
    version("6.2.24", sha256="9225316e43691ff344224824384acfdf16ff2aac5468d6d810e38846051d5db8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.13.0:", type="build")
    depends_on("mono")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    generator("ninja")

    def cmake_args(self):
        args = ["-DUSE_WERROR=ON"]
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            ninja("install")
            install("fdb.cluster", prefix.bin)
