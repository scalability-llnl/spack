# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastapiUtils(PythonPackage):
    """Reusable utilities for FastAPI"""

    homepage = "https://fastapi-utils.davidmontague.xyz"
    pypi = "fastapi-utils/fastapi-utils-0.2.1.tar.gz"

    license("MIT")

    version("0.2.1", sha256="0e6c7fc1870b80e681494957abf65d4f4f42f4c7f70005918e9181b22f1bd759")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry@0.12:", type="build")

    depends_on("py-fastapi", type=("build", "run"))
    depends_on("py-pydantic@1", type=("build", "run"))
    depends_on("py-sqlalchemy@1.3.12:1", type=("build", "run"))
