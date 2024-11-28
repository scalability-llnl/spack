# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonJose(PythonPackage):
    """JOSE implementation in Python"""

    homepage = "https://github.com/mpdavis/python-jose"
    pypi = "python-jose/python-jose-3.3.0.tar.gz"

    license("MIT")

    version("3.3.0", sha256="55779b5e6ad599c6336191246e95eb2293a9ddebd555f796a65f838f07e5d78a")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-rsa", type=("build", "run"))
    depends_on("py-ecdsa@:0.14.1,0.16.0:", type=("build", "run"))
    depends_on("py-pyasn1", type=("build", "run"))
