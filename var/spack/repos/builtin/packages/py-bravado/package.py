# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBravado(PythonPackage):
    """
    Bravado is a Yelp maintained fork of digium/swagger-py for use with
    OpenAPI Specification version 2.0 (previously known as Swagger).
    """

    homepage = "https://github.com/Yelp/bravado"
    pypi = "bravado/bravado-11.0.3.tar.gz"

    version("11.0.3", sha256="1bb6ef75d84140c851fffe6420baaee5037d840070cfe11d60913be6ab8e0530")

    depends_on("python@:2,3.5.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-bravado-core@5.16.1:", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests@2.17:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("py-monotonic", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
