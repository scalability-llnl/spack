# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wrk(MakefilePackage):
    """Wrk is a modern HTTP benchmarking tool capable
    of generating significant load when run on a single
    multi-core CPU."""

    homepage = "https://github.com/wg/wrk"
    url = "https://github.com/wg/wrk/archive/4.1.0.tar.gz"

    license("Apache-2.0")

    version("4.1.0", sha256="6fa1020494de8c337913fd139d7aa1acb9a020de6f7eb9190753aa4b1e74271e")
    version("4.0.2", sha256="a4a6ad6727733023771163e7250189a9a23e6253b5e5025191baa6092d5a26fb")
    version("4.0.1", sha256="c03bbc283836cb4b706eb6bfd18e724a8ce475e2c16154c13c6323a845b4327d")
    version("4.0.0", sha256="8fa8fb05f4663d03c1ca7804367eb602882f9630441bd56e8e9aaf3a2bd26067")
    version("3.1.2", sha256="da88a25f0eeb9e1fd6a9dcf4a96859e9e758f9446f0787cf7c95e4ccde14eefc")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("wrk", prefix.bin)
