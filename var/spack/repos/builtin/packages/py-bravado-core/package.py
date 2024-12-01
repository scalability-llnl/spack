# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBravadoCore(PythonPackage):
    """
    bravado-core is a Python library that adds client-side and server-side
    support for the OpenAPI Specification v2.0.
    """

    homepage = "https://github.com/Yelp/bravado-core"
    pypi = "bravado-core/bravado-core-5.17.1.tar.gz"

    version("5.17.1", sha256="0da9c6f3814734622a55db3f62d08db6e188b25f3ebd087de370c91afb66a7f4")

    depends_on("python@:2,3.5.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-jsonref", type=("build", "run"))
    depends_on("py-jsonschema@2.5.1:", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-swagger-spec-validator@2.0.1:", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-msgpack@0.5.2:", type=("build", "run"))

    depends_on("py-pyrsistent@0.17:", when="^python@:3.4", type="build")
