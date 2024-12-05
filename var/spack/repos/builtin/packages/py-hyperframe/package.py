# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperframe(PythonPackage):
    """HTTP/2 framing layer for Python"""

    homepage = "https://github.com/python-hyper/hyperframe/"
    pypi = "hyperframe/hyperframe-6.0.0.tar.gz"

    license("MIT")

    version("6.0.0", sha256="742d2a4bc3152a340a49d59f32e33ec420aa8e7054c1444ef5c7efff255842f1")
    version("5.2.0", sha256="a9f5c17f2cc3c719b917c4f33ed1c61bd1f8dfac4b1bd23b7c80b3400971b41f")

    depends_on("python@3.6.1:", type=("build", "run"), when="@6:")
    depends_on("py-setuptools", type="build")
