# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskBabel(PythonPackage):
    """Implements i18n and l10n support for Flask."""

    homepage = "https://pythonhosted.org/Flask-Babel/"
    pypi = "Flask-Babel/Flask-Babel-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version("2.0.0", sha256="f9faf45cdb2e1a32ea2ec14403587d4295108f35017a7821a2b1acb8cfd9257d")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-flask", type=("build", "run"))
    depends_on("py-babel@2.3:", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-jinja2@2.5:", type=("build", "run"))
