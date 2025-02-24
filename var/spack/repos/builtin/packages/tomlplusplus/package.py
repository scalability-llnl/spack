# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tomlplusplus(CMakePackage):
    """Header-only TOML config file parser and serializer for C++17"""

    homepage = "https://marzer.github.io/tomlplusplus/"
    url = "https://github.com/marzer/tomlplusplus/archive/refs/tags/v3.4.0.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("3.4.0", sha256="8517f65938a4faae9ccf8ebb36631a38c1cadfb5efa85d9a72e15b9e97d25155")

    depends_on("cxx", type="build")
    depends_on("cmake@3.14:", type="build")
