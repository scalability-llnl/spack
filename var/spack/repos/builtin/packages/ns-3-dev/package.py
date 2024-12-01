# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ns3Dev(CMakePackage):
    """ns-3 is a discrete-event network simulator"""

    homepage = "https://www.nsnam.org/"
    url = "https://gitlab.com/nsnam/ns-3-dev/-/archive/ns-3.30.1/ns-3-dev-ns-3.30.1.tar.bz2"

    maintainers("yee29")

    license("GPL-2.0-or-later")

    version("3.40", sha256="96526e7ae6cb746d02af0cad04f63daff926dad5d30a6fe0d3c7943989ba4e59")
    version("3.37", sha256="d72defeeddbba14397cd4403565992d98cd7b7d9c680c22fee56022706878720")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("boost", default=True, description="Compile with Boost libraries")

    depends_on("gsl")
    depends_on("harfbuzz")
    depends_on("libxml2")
    depends_on("sqlite")

    depends_on("boost", when="+boost")

    depends_on("ccache", type="run")

    depends_on("pkgconfig", type="build")

    def cmake_args(self):
        return [
            self.define("NS3_COLORED_OUTPUT", True),
            self.define("NS3_GTK3", False),
            self.define("NS3_MPI", False),
            self.define("NS3_PYTHON_BINDINGS", False),
            self.define("NS3_FAST_LINKERS", False),
            self.define("NS3_SQLITE", True),
            self.define("CCACHE", self.spec["ccache"].prefix.bin.ccache),
        ]
