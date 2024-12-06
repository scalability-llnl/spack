# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeyring(PythonPackage):
    """The Python keyring library provides an easy way to access the system keyring
    service from python. It can be used in any application that needs safe password
    storage."""

    homepage = "https://github.com/jaraco/keyring"
    pypi = "keyring/keyring-23.0.1.tar.gz"

    license("MIT")

    version("24.3.0", sha256="e730ecffd309658a08ee82535a3b5ec4b4c8669a9be11efb66249d8e0aeb9a25")
    version("23.13.1", sha256="ba2e15a9b35e21908d0aaf4e0a47acc52d6ae33444df0da2b49d41a46ef6d678")
    version("23.9.1", sha256="39e4f6572238d2615a82fcaa485e608b84b503cf080dc924c43bbbacb11c1c18")
    version("23.5.0", sha256="9012508e141a80bd1c0b6778d5c610dd9f8c464d75ac6774248500503f972fb9")
    version("23.2.1", sha256="6334aee6073db2fb1f30892697b1730105b5e9a77ce7e61fca6b435225493efe")
    version("23.2.0", sha256="1e1970dcecde00c59ff6033d69cee3b283cd0d7cbad78b0dc4cdd15c8a28bcf8")
    version("23.1.0", sha256="b7e0156667f5dcc73c1f63a518005cd18a4eb23fe77321194fefcc03748b21a4")
    version("23.0.1", sha256="045703609dd3fccfcdb27da201684278823b72af515aedec1a8515719a038cb8")
    version("21.7.0", sha256="a144f7e1044c897c3976202af868cb0ac860f4d433d5d0f8e750fa1a2f0f0b50")
    version("20.0.1", sha256="963bfa7f090269d30bdc5e25589e5fd9dad2cf2a7c6f176a7f2386910e5d0d8d")
    version("18.0.1", sha256="67d6cc0132bd77922725fae9f18366bb314fd8f95ff4d323a4df41890a96a838")

    depends_on("py-setuptools@56:", when="@23.1:", type="build")
    depends_on("py-setuptools@42:", when="@21:", type="build")
    depends_on("py-setuptools@34.4:", type="build")
    depends_on("py-setuptools-scm@3.4.1:+toml", when="@21:", type="build")
    depends_on("py-setuptools-scm@1.15:", type="build")

    depends_on("py-secretstorage@3.2:", when="@21: platform=linux", type=("build", "run"))
    depends_on("py-secretstorage", when="platform=linux", type=("build", "run"))
    depends_on("py-jeepney@0.4.2:", when="@21: platform=linux", type=("build", "run"))
    depends_on(
        "py-importlib-metadata@4.11.4:", when="@23.10: ^python@:3.11", type=("build", "run")
    )
    depends_on("py-importlib-metadata@3.6:", when="@23: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-metadata@1:", when="@21:22", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@20:", type=("build", "run"))
    depends_on("py-jaraco-classes", when="@23.9.1:", type=("build", "run"))
    depends_on("py-importlib-resources", when="@23.13: ^python@:3.8", type=("build", "run"))

    # TODO: additional dependency on pywin32-ctypes required for Windows

    # Historical dependencies
    depends_on("py-entrypoints", when="@18", type=("build", "run"))
