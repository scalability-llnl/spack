# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyutilib(PythonPackage):
    """The PyUtilib project supports a collection of Python utilities,
    including a well-developed component architecture and extensions to the
    PyUnit testing framework. PyUtilib has been developed to support several
    Python-centric projects, especially Pyomo. PyUtilib is available under the
    BSD License."""

    homepage = "https://github.com/PyUtilib/pyutilib"
    url = "https://github.com/PyUtilib/pyutilib/archive/5.5.1.tar.gz"

    license("BSD-3-Clause")

    version("6.0.0", sha256="b758419b42f9f512330644ebf05d54a1d3c5671268c344204e02f32713342de5")
    version("5.6.2", sha256="3f9f500cf1f15a92e7eb0b3c3ca2af537a2a9e61fe70ad6be4d2d08d9e47764f")
    version("5.6.1", sha256="0d0d57921877dc292dd9de39596fabc83b5d072adf10a90c979f678662ddb752")
    version("5.6", sha256="ea1e263652d8199322759e169e4a40fc23964c49e82ae1470ab83a613a6e6b25")
    version("5.5.1", sha256="0e9070551abc82a90b977f9bf875a91ceebfdfa5d7327028ece60324ef66f3ab")
    version("5.5", sha256="442f5abbd2a61c6f51698e0450cddbb4fc10047f350a939218f0c4b92a90f8ef")
    version("5.4.1", sha256="7d6bf66d3ebaf8769e9395748f618a13a7e02cc88a62f8be8889f40816502b14")
    version("5.4", sha256="c778e89a22d882ebf0096eca3abc4cc312f6e1fa1b7869b416710a2f467cb4d6")
    version("5.3.5", sha256="8b9c2be34f80da0ae18ecc2e46ac7467d35b2e9f33411e7331c6edddea108906")
    version("5.3.4", sha256="475c97bf1213add6b7fefaa3f05affef3613e6aecc9fcb3cc0693304671b73c3")
    version("5.3.3", sha256="318f4d60c9552493fe81a4b2e0418d2cf43aaab68e6d23e2c9a68ef010c9cf21")

    depends_on("python@2.7:2,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-nose", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
