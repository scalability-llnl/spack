# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenapiSchemaPydantic(PythonPackage):
    """OpenAPI (v3) specification schema as pydantic class"""

    homepage = "https://github.com/kuimono/openapi-schema-pydantic"
    pypi = "openapi-schema-pydantic/openapi-schema-pydantic-1.2.4.tar.gz"

    license("MIT")

    version("1.2.4", sha256="3e22cf58b74a69f752cc7e5f1537f6e44164282db2700cbbcd3bb99ddd065196")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pydantic@1.8.2:", type=("build", "run"))
