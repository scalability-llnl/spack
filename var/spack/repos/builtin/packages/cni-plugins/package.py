# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CniPlugins(Package):
    """Standard networking plugins for container networking"""

    homepage = "https://github.com/containernetworking/plugins"
    url = "https://github.com/containernetworking/plugins/archive/v1.0.1.tar.gz"
    maintainers("bernhardkaindl")

    license("Apache-2.0")

    version("1.3.0", sha256="f9871b9f6ccb51d2b264532e96521e44f926928f91434b56ce135c95becf2901")
    version("1.2.0", sha256="f3496ddda9c7770a0b695b67ae7ee80a4ee331ac2745af4830054b81627f79b7")
    version("1.1.1", sha256="c86c44877c47f69cd23611e22029ab26b613f620195b76b3ec20f589367a7962")
    version("1.0.1", sha256="2ba3cd9f341a7190885b60d363f6f23c6d20d975a7a0ab579dd516f8c6117619")

    depends_on("c", type="build")  # generated

    depends_on("go", type="build")

    def install(self, spec, prefix):
        utils = "github.com/containernetworking/plugins/pkg/utils/buildversion"
        which("./build_linux.sh")(
            "-ldflags", "-extldflags -static -X {0}.BuildVersion={1}".format(utils, self.version)
        )
        install_tree("bin", prefix.bin)
