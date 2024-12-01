# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrapheneTornado(PythonPackage):
    """Graphene Tornado integration."""

    homepage = "https://github.com/graphql-python/graphene-tornado"
    pypi = "graphene-tornado/graphene-tornado-2.6.1.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("2.6.1", sha256="953bf812267177224ce1ac2a93c669069d85a8fa187a9fac681b76b63dffebc2")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.10.0:", type=("build", "run"))
    depends_on("py-graphene@2.1:2", type=("build", "run"))
    depends_on("py-jinja2@2.10.1:", type=("build", "run"))
    depends_on("py-tornado@5.1.0:", type=("build", "run"))
    # py-werkzeug version requirements differ between setup.py (0.12.2)
    # and requirements.txt (0.15.3); the latter seems to be correct,
    # see also https://github.com/spack/spack/pull/41426
    depends_on("py-werkzeug@0.15.3", type=("build", "run"))
    depends_on("py-pytest", type=("build"))
