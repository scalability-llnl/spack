# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rkcommon(CMakePackage):
    """This project represents a common set of C++ infrastructure and CMake utilities
    used by various components of Intel® oneAPI Rendering Toolkit."""

    homepage = "https://github.com/RenderKit/rkcommon"
    url = "https://github.com/RenderKit/rkcommon/archive/v1.4.1.tar.gz"
    git = "https://github.com/RenderKit/rkcommon.git"

    license("Apache-2.0")

    version("1.14.2", sha256="79334ef3dadddb03ec0483fbf49bf690fb8902d5c2732d977b2c116651484cc6")
    version("1.14.0", sha256="5aef75afc8d4fccf9e70df4cbdf29a1b28b39ee51b5588b94b83a14c6a166d83")
    version("1.13.0", sha256="8ae9f911420085ceeca36e1f16d1316a77befbf6bf6de2a186d65440ac66ff1f")
    version("1.12.0", sha256="6abb901073811cdbcbe336772e1fcb458d78cab5ad8d5d61de2b57ab83581e80")
    version("1.11.0", sha256="9cfeedaccdefbdcf23c465cb1e6c02057100c4a1a573672dc6cfea5348cedfdd")
    version("1.10.0", sha256="57a33ce499a7fc5a5aaffa39ec7597115cf69ed4ff773546b5b71ff475ee4730")
    version("1.9.0", sha256="b68aa02ef44c9e35c168f826a14802bb5cc6a9d769ba4b64b2c54f347a14aa53")
    version("1.8.0", sha256="f037c15f7049610ef8bca37500b2ab00775af60ebbb9d491ba5fc2e5c04a7794")
    version("1.7.0", sha256="b24d063541ccbfd69e6d77485b509d1bbffd9744e735dbd9bd8647eb8751c5b7")
    version("1.6.1", sha256="b61c10f26fba3e6f00305d5828b3bac523d559c5c0e6f79893b19e8c0e30074e")
    version("1.6.0", sha256="24d0c9c58a4d2f22075850df170ec5732cfaa0a16f22f90dbd6538232be009b0")
    version("1.5.1", sha256="27dc42796aaa4ea4a6322f14ad64a46e83f42724c20c0f7b61d069ac91310295")
    version("1.5.0", sha256="3556e90301d4361f871b87ddf898b9d675deaa717cab541f99012e14557986bd")
    version("1.4.2", sha256="2d1c0046cf583d3040fc9bb3b8ddcb1a2262d3f48aebd0973e6bd6cabb487f9e")
    version("1.4.1", sha256="f5968f5865fa5fe938843e1db621795524e7d31b37ce6024ba2978bb293ddfcf")

    depends_on("cxx", type="build")  # generated

    depends_on("tbb")

    def cmake_args(self):
        args = [self.define("INSTALL_DEPS", False)]
        return args
