# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfStandard(PythonPackage):
    """Standards document describing ASDF, Advanced Scientific Data Format"""

    homepage = "https://asdf-standard.readthedocs.io/"
    pypi = "asdf_standard/asdf_standard-1.0.3.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version("1.1.1", sha256="01535bc2b15bfc09ec8a62d4999f9cf32dc49dc71660c8425640228fd8776102")
    version("1.0.3", sha256="afd8ff9a70e7b17f6bcc64eb92a544867d5d4fe1f0076719142fdf62b96cfd44")

    with when("@1.1.1:"):
        depends_on("python@3.9:", type=("build", "run"))

        depends_on("py-setuptools@61:", type="build")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    depends_on("py-importlib-resources@3:", type=("build", "run"), when="@1.0.3 ^python@:3.8")
