# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPynacl(PythonPackage):
    """Python binding to the Networking and Cryptography (NaCl) library."""

    homepage = "https://github.com/pyca/pynacl/"
    pypi = "PyNaCl/PyNaCl-1.4.0.tar.gz"

    version("1.5.0", sha256="8ac7448f09ab85811607bdd21ec2464495ac8b7c66d146bf545b0f08fb9220ba")
    version("1.4.0", sha256="54e9a2c849c742006516ad56a88f5c74bf2ce92c9f67435187c3c5953b346505")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@1.5.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@40.8:", type="build", when="@1.5.0:")
    depends_on("py-six", type=("build", "run"), when="@1.4.0")
    depends_on("py-cffi@1.4.1:", type=("build", "run"))
