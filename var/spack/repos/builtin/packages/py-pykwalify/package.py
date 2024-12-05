# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPykwalify(PythonPackage):
    """
    Python lib/cli for JSON/YAML schema validation
    """

    homepage = "https://github.com/grokzen/pykwalify"
    pypi = "pykwalify/pykwalify-1.7.0.tar.gz"

    license("MIT")

    version("1.7.0", sha256="7e8b39c5a3a10bc176682b3bd9a7422c39ca247482df198b402e8015defcceb2")
    version("1.6.1", sha256="191fd3f457f23c0aa8538c3a5c0249f70eeb1046e88d0eaaef928e09c44dff8d")

    depends_on("py-setuptools", type="build")
    depends_on("py-docopt@0.6.2:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.11.0:", type=("build", "run"))
    depends_on("py-python-dateutil@2.4.2:", type=("build", "run"))
    depends_on("py-pyyaml@3.11:", type=("build", "run"), when="@1.6.1")

    conflicts("^py-ruamel-yaml@0.16.0:", when="@1.6.1")
