# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladWebapp(PythonPackage):
    """DataLad extension for exposing commands via a web request API"""

    homepage = "https://github.com/datalad/datalad-webapp"
    pypi = "datalad_webapp/datalad_webapp-0.3.tar.gz"

    version("0.3", sha256="7bbb2ce58a7e0e6d1a7a2f33d7e50fe7e73cd764380e70fdc2d9f651c3d0e312")

    depends_on("py-setuptools", type="build")
    depends_on("py-datalad@0.12.5:", type=("build", "run"))
    depends_on("py-flask@1.0:", type=("build", "run"))
    depends_on("py-flask-restful", type=("build", "run"))
    depends_on("py-pytest-cov", type=("build", "run"))
