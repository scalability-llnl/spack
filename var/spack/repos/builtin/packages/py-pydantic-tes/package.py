# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPydanticTes(PythonPackage):
    """Pydantic Models for the GA4GH Task Execution Service"""

    homepage = "https://github.com/jmchilton/pydantic-tes"
    pypi = "pydantic-tes/pydantic-tes-0.1.5.tar.gz"

    license("MIT")

    version("0.1.5", sha256="557cc77bdbeae86a6bd155af2d0aeaa5050cd9e3f7d9b17b817f14dd814a7423")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
