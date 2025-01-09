# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxFortran(PythonPackage):
    """Fortran domain and autodoc extensions to Sphinx"""

    homepage = "https://sphinx-fortran.readthedocs.io"
    pypi = "sphinx-fortran/sphinx-fortran-1.1.1.tar.gz"
    git = "https://github.com/VACUMM/sphinx-fortran.git"

    maintainers("rbberger")

    license("CeCILL-2.1")

    version("master", branch="master")
    version("1.1.1", sha256="e912e6b292e80768ad3cf580a560a4752c2c077eda4a1bbfc3a4ca0f11fb8ee1")

    depends_on("py-sphinx@1:")
    depends_on("py-numpy@1:")
    depends_on("py-six")
    depends_on("py-future")
