# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfection(PythonPackage):
    """The sweetest config system for Python"""

    homepage = "https://github.com/explosion/confection"
    pypi = "confection/confection-0.0.4.tar.gz"

    license("MIT")

    version("0.0.4", sha256="b1ddf5885da635f0e260a40b339730806dfb1bd17d30e08764f35af841b04ecf")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pydantic@1.7.4:1.7,1.9:1.10", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.1:4.4", type=("build", "run"), when="^python@3.7")
    depends_on("py-srsly@2.4:2", type=("build", "run"))
