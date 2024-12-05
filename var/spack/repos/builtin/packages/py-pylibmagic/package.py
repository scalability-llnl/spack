# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPylibmagic(PythonPackage):
    """scikit-build project with CMake for compiling libmagic"""

    homepage = "https://github.com/kratsg/pylibmagic"
    pypi = "pylibmagic/pylibmagic-0.2.2.tar.gz"

    version("0.2.2", sha256="17551b5259db4045c63e595577d42df172e35147e26160a47f4a5ba3933281e7")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools_scm@3.4:+toml", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("cmake", type="build")
    depends_on("ninja", type="build")

    depends_on("py-importlib-resources", when="^python@:3.8", type=("build", "run"))
    depends_on("py-typing-extensions@3.7:", when="^python@:3.7", type=("build", "run"))
