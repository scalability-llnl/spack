# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstropyHelpers(PythonPackage):
    """The astropy-helpers package includes many build,
    installation, and documentation-related tools used by the
    Astropy project, but packaged separately for use by other
    projects that wish to leverage this work."""

    homepage = "https://github.com/astropy/astropy-helpers"
    url = "https://github.com/astropy/astropy-helpers/archive/v4.0.1.tar.gz"

    license("BSD-3-Clause")

    version("4.0.1", sha256="88602971c3b63d6aaa6074d013f995d1e234acb3d517d70d7fcebd30cdaf5c89")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@30.3:", type="build")
