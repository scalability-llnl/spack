# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyShippinglabel(PythonPackage):
    """Utilities for handling packages."""

    homepage = "https://github.com/domdfcoding/shippinglabel"
    pypi = "shippinglabel/shippinglabel-1.5.0.tar.gz"

    license("MIT")

    version("1.5.0", sha256="b2332bf29853e29f877dab21f17f2a8632fd2b48f5f32a6fa0b254a6fdd0a451")

    depends_on("py-wheel@0.34.2:", type="build")
    depends_on("py-setuptools@40.6:", type="build")
    conflicts("^py-setuptools@61")
    depends_on("py-apeye@1:", type=("build", "run"))
    depends_on("py-dist-meta@0.1.2:", type=("build", "run"))
    depends_on("py-dom-toml@0.2.2:", type=("build", "run"))
    depends_on("py-domdf-python-tools@3.1:", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-platformdirs@2.3:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"))
