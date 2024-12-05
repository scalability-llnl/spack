# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFava(PythonPackage):
    """Fava is a web interface for the double-entry bookkeeping software
    Beancount with a focus on features and usability."""

    homepage = "https://beancount.github.io/fava/"
    pypi = "fava/fava-1.18.tar.gz"

    license("MIT")

    version("1.18", sha256="21336b695708497e6f00cab77135b174c51feb2713b657e0e208282960885bf5")

    # Some of the dependencies are not listed as required at
    # build or run time, but actually are.
    # - py-setuptools
    # - py-importlib
    # - py-pytest
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type=("build"))

    depends_on("py-babel@2.6.0:", type=("build", "run"))
    depends_on("py-beancount@2.3.0:", type=("build", "run"))
    depends_on("py-cheroot", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-flask@0.10.1:", type=("build", "run"))
    depends_on("py-flask-babel@1.0.0:", type=("build", "run"))
    depends_on("py-jinja2@2.10:", type=("build", "run"))
    depends_on("py-markdown2@2.3.0:", type=("build", "run"))
    depends_on("py-ply", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-simplejson@3.2.0:", type=("build", "run"))
    depends_on("py-werkzeug@0.15.0:", type=("build", "run"))
