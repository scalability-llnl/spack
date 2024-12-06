# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRsa(PythonPackage):
    """Pure-Python RSA implementation"""

    homepage = "https://stuvel.eu/rsa"
    pypi = "rsa/rsa-3.4.2.tar.gz"

    license("Apache-2.0")

    version("4.9", sha256="e38464a49c6c85d7f1351b0126661487a7e0a14a50f1675ec50eb34d4f20ef21")
    version("4.7.2", sha256="9d689e6ca1b3038bc82bf8d23e944b6b6037bc02301a574935b2dd946e0353b9")
    version("4.0", sha256="1a836406405730121ae9823e19c6e806c62bbad73f890574fff50efa4122c487")
    version("3.4.2", sha256="25df4e10c263fb88b5ace923dd84bf9aa7f5019687b5e55382ffcdb8bede9db5")

    depends_on("py-setuptools", when="@:4.7.2", type=("build", "run"))
    depends_on("py-poetry-core@1:", when="@4.9:", type="build")
    depends_on("py-pyasn1@0.1.3:", type=("build", "run"))
    depends_on("python@3.5:3", when="@4.7.2:", type=("build", "run"))
    depends_on("python@3.6:3", when="@4.9:", type=("build", "run"))
