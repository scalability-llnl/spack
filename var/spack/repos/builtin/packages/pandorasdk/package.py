# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pandorasdk(CMakePackage):
    """Metadata package to bring together and build multiple Pandora libraries.
    NOTE: for proper version control with spack, this should be broken up and
    the subpackages installed individually."""

    url = "https://github.com/PandoraPFA/PandoraSDK/archive/v03-04-00.tar.gz"
    homepage = "https://github.com/PandoraPFA/PandoraSDK"
    git = "https://github.com/PandoraPFA/PandoraSDK.git"

    tags = ["hep"]

    maintainers("jmcarcell", "wdconinc")

    version("master", branch="master")
    version("3.4.2", sha256="e076adb2e3d28d3ac5dcc06bcc6e96815d23ef7782e1a87842b1e3e96e194994")
    version("3.4.1", sha256="9607bf52a9d79d88d28c45d4f3336e066338b36ab81b4d2d125226f4ad3a7aaf")
    version("3.4.0", sha256="1e30db056d4a43f8659fccdda00270af14593425d933f91e91d5c97f1e124c6b")

    depends_on("cxx", type="build")  # generated

    depends_on("pandorapfa")

    def cmake_args(self):
        args = [
            self.define("LC_PANDORA_CONTENT", True),
            self.define("LAR_PANDORA_CONTENT", True),
            self.define("CMAKE_MODULE_PATH", self.spec["pandorapfa"].prefix.cmakemodules),
            self.define("CMAKE_CXX_FLAGS", "-std=c++17"),
        ]
        return args

    def url_for_version(self, version):
        # contrary to iLCSoft packages, here the patch version is kept when 0
        base_url = self.url[: self.url.rfind("/")]
        major = str(version[0]).zfill(2)
        minor = str(version[1]).zfill(2)
        patch = str(version[2]).zfill(2)
        url = base_url + "/v%s-%s-%s.tar.gz" % (major, minor, patch)
        return url
