# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResponses(PythonPackage):
    """A utility library for mocking out the `requests` Python library."""

    homepage = "https://github.com/getsentry/responses"
    pypi = "responses/responses-0.13.3.tar.gz"

    maintainers("dorton21")

    license("Apache-2.0")

    version("0.13.3", sha256="18a5b88eb24143adbf2b4100f328a2f5bfa72fbdacf12d97d41f07c26c45553d")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.0:", type=("build", "run"))
    depends_on("py-urllib3@1.25.10:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
