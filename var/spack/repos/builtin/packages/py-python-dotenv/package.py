# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonDotenv(PythonPackage):
    """Read key-value pairs from a .env file and set them as environment variables"""

    homepage = "https://github.com/theskumar/python-dotenv"
    pypi = "python-dotenv/python-dotenv-0.19.2.tar.gz"

    maintainers("jcpunk")

    license("BSD-3-Clause")

    version("1.0.1", sha256="e324ee90a023d808f1959c46bcbc04446a10ced277783dc6ee09987c37ec10ca")
    version("0.19.2", sha256="a5de49a31e953b45ff2d2fd434bbc2670e8db5273606c1e737cc6b93eff3655f")

    variant("cli", default=False, description="Add commandline tools")

    depends_on("py-setuptools", type="build")
    depends_on("py-click@5:", when="+cli", type=("build", "run"))
