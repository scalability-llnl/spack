# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyfaidx(PythonPackage):
    """pyfaidx: efficient pythonic random access to fasta subsequences"""

    pypi = "pyfaidx/pyfaidx-0.5.5.2.tar.gz"

    maintainers("snehring")

    license("BSD-3-Clause")

    version("0.8.1.2", sha256="d8452470455b1e778f93969447db8ea24deb4624c7c40769516459cb6f87bc33")
    version("0.6.4", sha256="7ba3bdcb1df4ba749f7665b34e6a052aa4e842406a0df95e6df4717cc123f392")
    version("0.5.5.2", sha256="9ac22bdc7b9c5d995d32eb9dc278af9ba970481636ec75c0d687d38c26446caa")

    depends_on("python@3.7:", type=("build", "run"), when="@0.8.1.2:")

    depends_on("py-setuptools@0.7:", type="build")
    depends_on("py-setuptools@45:", type="build", when="@0.8.1.2:")
    depends_on("py-setuptools-scm", type="build", when="@0.8.1.2:")
    depends_on("py-importlib-metadata", type="build", when="@0.8.1.2:")
    depends_on("py-packaging", type=("build", "run"), when="@0.8.1.2:")

    depends_on("py-six", type=("build", "run"), when="@:0.6.4")
