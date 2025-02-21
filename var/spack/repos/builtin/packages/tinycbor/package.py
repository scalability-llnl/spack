# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tinycbor(MakefilePackage):
    """Concise Binary Object Representation (CBOR) Library"""

    homepage = "https://github.com/intel/tinycbor"
    url = "https://github.com/intel/tinycbor/archive/refs/tags/v0.6.0.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("0.6.0", sha256="512e2c9fce74f60ef9ed3af59161e905f9e19f30a52e433fc55f39f4c70d27e4")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    build_targets = ["CC=cc", "CXX=cxx"]

    @property
    def install_targets(self):
        return ["install", f"prefix={self.prefix}"]
