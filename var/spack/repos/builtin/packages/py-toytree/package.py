# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToytree(PythonPackage):
    """A minimalist tree manipulation and plotting library for use inside
    jupyter notebooks. Toytree combines a popular tree data structure
    based on the ete3 library with modern plotting tools based on the
    toyplot plotting library.
    """

    homepage = "https://github.com/eaton-lab/toytree"
    pypi = "toytree/toytree-2.0.1.tar.gz"

    maintainers("snehring")

    version("2.0.1", sha256="4f1452a76441857a13f72c99bf7d9f0a394cd8eae7fc02ee5349d946f2507101")

    depends_on("py-setuptools", type="build")

    depends_on("py-toyplot", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
