# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAvroPython3(PythonPackage):
    """Apache Avro is a data serialization system.
    Note: lang/py3 version (this package) will be deprecated and lang/py
    functions will be made available for both python2 and python3."""

    homepage = "https://github.com/apache/avro/tree/master/lang/py3"
    pypi = "avro-python3/avro-python3-1.10.0.tar.gz"

    license("Apache-2.0")

    version("1.10.0", sha256="a455c215540b1fceb1823e2a918e94959b54cb363307c97869aa46b5b55bde05")
    version("1.9.1", sha256="daab2cea71b942a1eb57d700d4a729e9d6cd93284d4dd4d65a378b9f958aa0d2")

    depends_on("python@3.5:", when="@1.10:", type=("build", "run"))
    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-isort", when="@1.10:", type="build")
    depends_on("py-pycodestyle", when="@1.10:", type="build")
