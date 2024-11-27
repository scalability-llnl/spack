# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonBenedict(PythonPackage):
    """A dict subclass with keylist/keypath support, I/O shortcuts
    and many utilities."""

    homepage = "https://github.com/fabiocaccamo/python-benedict"
    pypi = "python-benedict/python-benedict-0.22.2.tar.gz"

    license("MIT")

    version("0.23.2", sha256="b7bdffd92ba1c9b9e044bda08ed545a48a45bd7a5207f93b4b2a8eb2660d1b4c")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-ftfy", type=("build", "run"))
    depends_on("py-mailchecker", type=("build", "run"))
    depends_on("py-phonenumbers", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-python-fsutil", type=("build", "run"))
    depends_on("py-python-slugify", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-xmltodict", type=("build", "run"))
