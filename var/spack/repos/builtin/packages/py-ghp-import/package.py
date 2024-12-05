# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGhpImport(PythonPackage):
    """Copy your docs directly to the gh-pages branch."""

    homepage = "https://github.com/c-w/ghp-import"
    pypi = "ghp-import/ghp-import-2.1.0.tar.gz"

    license("Apache-2.0")

    version("2.1.0", sha256="9c535c4c61193c2df8871222567d7fd7e5014d835f97dc7b7439069e2413d343")

    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil@2.8.1:", type=("build", "run"))
