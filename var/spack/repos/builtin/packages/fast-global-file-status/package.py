# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FastGlobalFileStatus(AutotoolsPackage):
    """provides a scalable mechanism to retrieve such information of a file,
    including its degree of distribution or replication and consistency."""

    homepage = "https://github.com/LLNL/FastGlobalFileStatus"
    url = "https://github.com/LLNL/FastGlobalFileStatus/files/2271592/fastglobalfilestatus-1.1.tar.gz"
    git = "https://github.com/LLNL/FastGlobalFileStatus.git"
    maintainers("lee218llnl")

    version("master", branch="master")
    version(
        "1.1.1",
        sha256="397de583a99e60aae8b4485d3decac6e23f50c658a6353fea149d6dd50d3ecee",
        url="https://github.com/LLNL/FastGlobalFileStatus/releases/download/v1.1.1/fastglobalfilestatus-1.1.1.tar.gz",
    )
    version("1.1", sha256="e6fba4a0b7f055899fa0e05d93a435c7f1f2ec1158b9a6647dc8d2bcf9c2e164")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("mrnet")
    # we depend on mpa@master for bug fixes since mpa 1.1
    depends_on("mount-point-attributes@1.1.1:")
    depends_on("mpi")
    depends_on("openssl")
    depends_on("elf")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-mpa=%s" % spec["mount-point-attributes"].prefix,
            "--with-mrnet=%s" % spec["mrnet"].prefix,
        ]
        return args
