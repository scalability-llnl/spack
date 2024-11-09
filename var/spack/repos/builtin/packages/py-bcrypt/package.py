# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBcrypt(PythonPackage):
    """Modern password hashing for your software and your servers"""

    homepage = "https://github.com/pyca/bcrypt/"
    url = "https://github.com/pyca/bcrypt/archive/3.1.4.tar.gz"

    license("Apache-2.0")

    version("3.2.0", sha256="da18f9af11ec41c57daf3758f9d21bd90292c0cdb2a7ea4e6b803f39e753c350")
    version("3.1.7", sha256="3f7784000846dd85fd626c2cf50065f5078dd76b68f6bd7ba3f132b691035ff4")
    version("3.1.6", sha256="169d3e6edbf8717e8856748b72fb02abe8ce8e0b65d733b1509ae9942e77f2a9")
    version("3.1.4", sha256="ca122a2cdcdffb0fd04f9dfe3493766f298bef02dea2f190f35ea6fdee222b96")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", when="@3.2:", type="build")
    depends_on("python@2.7:2,3.4:", when="@3.1.6:", type="build")
    depends_on("py-setuptools@40.8:", when="@3.1.7:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.1:", type=("build", "run"))
    depends_on("py-six@1.4.1:", type=("build", "run"))
