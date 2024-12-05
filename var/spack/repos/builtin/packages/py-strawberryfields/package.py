# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyStrawberryfields(PythonPackage):
    """Open source library for continuous-variable quantum computation"""

    homepage = "https://github.com/XanaduAI/StrawberryFields"
    pypi = "StrawberryFields/StrawberryFields-0.23.0.tar.gz"

    maintainers("marcodelapierre")

    license("Apache-2.0")

    version("0.23.0", sha256="bfe94867cdee8e2904752573f1ff46b78d9f373da16a1cfa31e1bd6cdf2e3cb0")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-networkx@2.0:", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-numpy@1.17.4:", type=("build", "run"))
    depends_on("py-python-dateutil@2.8.0:", type=("build", "run"))
    depends_on("py-quantum-blackbird@0.3.0:", type=("build", "run"))
    depends_on("py-requests@2.22.0:", type=("build", "run"))
    depends_on("py-scipy@1.0.0:", type=("build", "run"))
    depends_on("py-sympy@1.5:", type=("build", "run"))
    depends_on("py-thewalrus@0.18.0:", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-urllib3@1.25.3:", type=("build", "run"))
    depends_on("py-quantum-xir@0.1.1:", type=("build", "run"))
    depends_on("py-xanadu-cloud-client@0.2.1:", type=("build", "run"))
