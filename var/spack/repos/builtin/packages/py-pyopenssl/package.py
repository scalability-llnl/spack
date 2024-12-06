# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyopenssl(PythonPackage):
    """High-level wrapper around a subset of the OpenSSL library.

    Note: The Python Cryptographic Authority strongly suggests the use of
    pyca/cryptography where possible. If you are using pyOpenSSL for anything
    other than making a TLS connection you should move to cryptography and
    drop your pyOpenSSL dependency."""

    homepage = "https://pyopenssl.org/"
    pypi = "pyOpenSSL/pyOpenSSL-19.0.0.tar.gz"

    license("Apache-2.0")

    version("23.2.0", sha256="276f931f55a452e7dea69c7173e984eb2a4407ce413c918aa34b55f82f9b8bac")
    version("22.1.0", sha256="7a83b7b272dd595222d672f5ce29aa030f1fb837630ef229f62e72e395ce8968")
    version("19.0.0", sha256="aeca66338f6de19d1aa46ed634c3b9ae519a64b458f8468aec688e7e3c20f200")
    version("18.0.0", sha256="6488f1423b00f73b7ad5167885312bb0ce410d3312eb212393795b53c8caa580")

    depends_on("py-setuptools", type="build")

    depends_on("py-cryptography@38:41", when="@23.2:", type=("build", "run"))
    depends_on("py-cryptography@38", when="@22", type=("build", "run"))
    depends_on("py-cryptography@2.3:", when="@19", type=("build", "run"))
    depends_on("py-cryptography@2.2.1:", when="@18", type=("build", "run"))

    conflicts("^py-cryptography@40:40.0.1", when="@23.2:")

    # Historical dependencies
    depends_on("py-six@1.5.2:", when="@:19", type=("build", "run"))
