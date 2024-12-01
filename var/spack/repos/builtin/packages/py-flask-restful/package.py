# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskRestful(PythonPackage):
    """Simple framework for creating REST APIs"""

    homepage = "https://www.github.com/flask-restful/flask-restful/"
    pypi = "Flask-RESTful/Flask-RESTful-0.3.8.tar.gz"

    license("BSD-3-Clause")

    version("0.3.9", sha256="ccec650b835d48192138c85329ae03735e6ced58e9b2d9c2146d6c84c06fa53e")

    depends_on("py-setuptools", type="build")
    depends_on("py-aniso8601@0.82:", type=("build", "run"))
    depends_on("py-flask@0.8:", type=("build", "run"))
    depends_on("py-six@1.3.0:", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
