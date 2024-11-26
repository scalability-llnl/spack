# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySwaggerSpecValidator(PythonPackage):
    """
    A Python library that validates Swagger Specs against
    the Swagger 1.2 or Swagger 2.0 specification.
    """

    homepage = "https://github.com/Yelp/swagger_spec_validator"
    pypi = "swagger-spec-validator/swagger-spec-validator-2.7.6.tar.gz"

    version("2.7.6", sha256="73f33e631a58f407265f2f813d194f2762a2b86f9aa905e7eee3df9b7f9428d3")

    depends_on("py-setuptools", type="build")
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pyrsistent@:0.16", when="^python@:3.0", type="build")
