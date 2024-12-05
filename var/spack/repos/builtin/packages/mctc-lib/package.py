# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MctcLib(MesonPackage):
    """Modular computation toolchain library for quantum chemistry file IO"""

    homepage = "https://github.com/grimme-lab/mctc-lib"
    url = "https://github.com/grimme-lab/mctc-lib/releases/download/v0.3.0/mctc-lib-0.3.0.tar.xz"
    git = "https://github.com/grimme-lab/mctc-lib"

    maintainers("awvwgk")

    license("Apache-2.0")

    version("main", branch="main")
    version("0.3.1", sha256="a5032a0bbbbacc952037c5215b71aa6b438767a84bafb60fda25ba43c8835513")
    version("0.3.0", sha256="81f3edbf322e6e28e621730a796278498b84af0f221f785c537a315312059bf0")

    depends_on("fortran", type="build")  # generated

    variant("json", default=False, description="Enable support for JSON")

    depends_on("meson@0.57.2:", type="build")
    depends_on("json-fortran@8:", when="+json")
    depends_on("pkgconfig", type="build")

    def meson_args(self):
        return ["-Djson={0}".format("enabled" if "+json" in self.spec else "disabled")]
