# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGunicorn(PythonPackage):
    """WSGI HTTP Server for UNIX"""

    homepage = "https://gunicorn.org"
    pypi = "gunicorn/gunicorn-20.1.0.tar.gz"

    license("MIT")

    version("20.1.0", sha256="e0a968b5ba15f8a328fdfd7ab1fcb5af4470c28aaf7e55df02a99bc13138e6e8")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@3:", type=("build", "run"))
