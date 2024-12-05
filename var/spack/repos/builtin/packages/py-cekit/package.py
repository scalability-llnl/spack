# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCekit(PythonPackage):
    """CEKit is a Container image creation tool.
    CEKit helps to build container images from image definition files
    with strong focus on modularity and code reuse."""

    homepage = "https://github.com/cekit/cekit/"
    url = "https://github.com/cekit/cekit/archive/3.7.0.tar.gz"

    license("MIT")

    version("3.7.0", sha256="2a778b50427f1d7478d5cd54a5df97fb1b8d540892a1e70d7f9a9c7b878f89ca")
    version("3.6.0", sha256="d046f25b533ffa1602e3c53e58cc90108bd8fb1f8d0c4fae92f28cf71f81add0")
    version("3.5.0", sha256="696a90098cde8a59b8e2c06e1b031ee1fd86e696d1e9894e836da2a1432bfd20")
    version("3.4.0", sha256="90817c5bf780235ce70b0228740511ecb9171540bffa4ca86721d3a6155d5901")
    version("3.3.2", sha256="a17fcfb1c49d32846f78627b10b45a44d1cb7d99280edd873836c9a721bf30a8")
    version("3.3.1", sha256="d31b7800417ec265131fc54df8a1cf275739fe29f3a3f96123dc996667d85368")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@3.10:", type=("build", "run"))
    depends_on("py-jinja2@2.7:", type=("build", "run"))
    depends_on("py-pykwalify@1.6.0:", type=("build", "run"))
    depends_on("py-colorlog@2.10.0:", type=("build", "run"))
    depends_on("py-click@6.7:", type=("build", "run"))
    depends_on("py-packaging@19.0:", type=("build", "run"))
