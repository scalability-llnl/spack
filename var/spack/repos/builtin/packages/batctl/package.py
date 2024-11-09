# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Batctl(MakefilePackage):
    """B.A.T.M.A.N. advanced control and management tool"""

    homepage = "https://github.com/open-mesh-mirror/batctl"
    url = "https://github.com/open-mesh-mirror/batctl/archive/v2019.5.tar.gz"

    license("GPL-2.0-only AND MIT AND ISC", checked_by="tgamblin")

    version("2019.5", sha256="ffe5857a33068ec174140c154610d76d833524d840a2fc2d1a15e16686213cad")
    version("2019.4", sha256="a3564eb9727335352dc0cfa2f2b29474c2c837384689ac5fcb387784a56e7685")
    version("2019.3", sha256="2bd93fa14925a8dc63a67e64266c8ccd2fa3ac44b10253d93e6f8a630350070c")
    version("2019.2", sha256="fb656208ff7d4cd8b1b422f60c9e6d8747302a347cbf6c199d7afa9b80f80ea3")

    depends_on("c", type="build")  # generated

    depends_on("libnl")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("batctl", prefix.bin)
