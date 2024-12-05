# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCherrypy(PythonPackage):
    """CherryPy is a pythonic, object-oriented HTTP framework."""

    homepage = "https://cherrypy.readthedocs.io/en/latest/"
    pypi = "CherryPy/CherryPy-18.1.1.tar.gz"

    license("BSD-3-Clause")

    version("18.1.1", sha256="6585c19b5e4faffa3613b5bf02c6a27dcc4c69a30d302aba819639a2af6fa48b")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-more-itertools", type=("build", "run"))
    depends_on("py-zc-lockfile", type=("build", "run"))
    depends_on("py-cheroot@6.2.4:", type=("build", "run"))
    depends_on("py-portend@2.1.1:", type=("build", "run"))
    depends_on("python@3.5:", when="@18.0.0:", type=("build", "run"))
