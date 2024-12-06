# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToml(PythonPackage):
    """A Python library for parsing and creating TOML configuration files.
    For more information on the TOML standard, see
    https://github.com/toml-lang/toml.git"""

    homepage = "https://github.com/uiri/toml.git"
    url = "https://github.com/uiri/toml/archive/0.10.2.tar.gz"

    license("MIT")

    version("0.10.2", sha256="71d4039bbdec91e3e7591ec5d6c943c58f9a2d17e5f6783acdc378f743fcdd2a")
    version("0.10.0", sha256="c3821b94be15da61d631bfff45b5c58074f01149792182e68f8690829cabfcf6")
    version("0.9.3", sha256="633a90ecb1f5665b58f0c94153fcf519313ef53e1de0eac90929cd6b6a014235")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
