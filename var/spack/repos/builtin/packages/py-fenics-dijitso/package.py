# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsDijitso(PythonPackage):
    """A Python module for distributed just-in-time shared library building"""

    homepage = "https://bitbucket.org/fenics-project/dijitso"
    url = "https://bitbucket.org/fenics-project/dijitso/downloads/dijitso-2019.1.0.tar.gz"
    git = "https://bitbucket.org/fenics-project/dijitso.git"
    maintainers("js947", "chrisrichardson")

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("2019.1.0", sha256="eaa45eec4457f3f865d72a926b7cba86df089410e78de04cd89b15bb405e8fd9")
    version("2018.1.0", sha256="2084ada1e7bd6ecec0999b15a17db98c72e26f1ccbf3fcbe240b1a035a1a2e64")
    version("2017.2.0", sha256="05a893d17f8a50067d303b232e41592dce2840d6499677ad8b457ba58a679b58")
    version("2017.1.0", sha256="ef23952539d349fbd384d41302abc94413d485ca7e8c29e8a0debc2aadaf8657")
    version("2016.2.0", sha256="1bfa0ac0d47dae75bbde8fabb1145d3caa2e6c28a1e4097ad5550a91a8a205e4")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
