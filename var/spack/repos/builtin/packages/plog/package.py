# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Plog(CMakePackage):
    """Portable, simple and extensible C++ logging library."""

    homepage = "https://github.com/SergiusTheBest/plog"
    url = "https://github.com/SergiusTheBest/plog/archive/refs/tags/1.1.10.tar.gz"

    maintainers("plexoos")

    license("MIT", checked_by="plexoos")

    version("1.1.10", sha256="55a090fc2b46ab44d0dde562a91fe5fc15445a3caedfaedda89fe3925da4705a")
    version("1.1.9", sha256="058315b9ec9611b659337d4333519ab4783fad3f2f23b1cc7bb84d977ea38055")

    depends_on("cxx", type="build")
