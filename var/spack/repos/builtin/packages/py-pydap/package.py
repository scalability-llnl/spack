# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydap(PythonPackage):
    """An implementation of the Data Access Protocol."""

    homepage = "https://www.pydap.org/en/latest/"
    pypi = "Pydap/Pydap-3.2.2.tar.gz"

    license("MIT")

    version("3.2.2", sha256="86326642e24f421595a74b0f9986da76d7932b277768f501fe214d72592bdc40")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-webob", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-six@1.4.0:", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
