# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDjango(PythonPackage):
    """The Web framework for perfectionists with deadlines."""

    homepage = "https://www.djangoproject.com/"
    pypi = "Django/Django-5.0.1.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("5.1.1", sha256="021ffb7fdab3d2d388bc8c7c2434eb9c1f6f4d09e6119010bbb1694dda286bc2")
    version("5.0.9", sha256="6333870d342329b60174da3a60dbd302e533f3b0bb0971516750e974a99b5a39")
    version("5.0.1", sha256="8c8659665bc6e3a44fefe1ab0a291e5a3fb3979f9a8230be29de975e57e8f854")
    version("3.0.5", sha256="d4666c2edefa38c5ede0ec1655424c56dc47ceb04b6d8d62a7eac09db89545c1")
    version("3.0.4", sha256="50b781f6cbeb98f673aa76ed8e572a019a45e52bdd4ad09001072dfd91ab07c8")
    version("3.0.3", sha256="2f1ba1db8648484dd5c238fb62504777b7ad090c81c5f1fd8d5eb5ec21b5f283")
    version("3.0.2", sha256="8c3575f81e11390893860d97e1e0154c47512f180ea55bd84ce8fa69ba8051ca")
    version("3.0.1", sha256="315b11ea265dd15348d47f2cbb044ef71da2018f6e582fed875c889758e6f844")
    version("2.2.12", sha256="69897097095f336d5aeef45b4103dceae51c00afa6d3ae198a2a18e519791b7a")
    version("2.2.11", sha256="65e2387e6bde531d3bb803244a2b74e0253550a9612c64a60c8c5be267b30f50")
    version("2.2.10", sha256="1226168be1b1c7efd0e66ee79b0e0b58b2caa7ed87717909cd8a57bb13a7079a")

    depends_on("python@3.10:", when="@5:", type=("build", "run"))
    depends_on("py-setuptools@61:69.2", when="@5.1:", type="build")
    depends_on("py-setuptools@40.8:", when="@5:5.0", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-asgiref@3.8.1:3", when="@5.1:", type=("build", "run"))
    depends_on("py-asgiref@3.7:3", when="@5:", type=("build", "run"))
    depends_on("py-asgiref", type=("build", "run"))
    depends_on("py-sqlparse@0.3.1:", when="@5:", type=("build", "run"))
    depends_on("py-sqlparse", type=("build", "run"))
    depends_on("py-tzdata", when="@5: platform=windows", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pytz", when="@:3", type=("build", "run"))
