# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMistletoe(PythonPackage):
    """A fast, extensible Markdown parser in pure Python."""

    homepage = "https://github.com/miyuchina/mistletoe"
    pypi = "mistletoe/mistletoe-1.2.1.tar.gz"

    license("MIT")

    version("1.2.1", sha256="7d0c1ab3747047d169f9fc4b925d1cba3f5c13eaf0b90c365b72e47e59d00a02")

    depends_on("python@3.5:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
