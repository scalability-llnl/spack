# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyroPpl(PythonPackage):
    """A Python library for probabilistic modeling and inference."""

    homepage = "https://pyro.ai/"
    pypi = "pyro-ppl/pyro-ppl-1.8.1.tar.gz"

    maintainers("adamjstewart", "meyersbs")

    license("Apache-2.0")

    version("1.8.4", sha256="766fad61e52df48885de96d41213da1f8e8c1b79ecf308ad53189fcd15c1cb41")
    version("1.8.1", sha256="d7c049eb2e7485a612b4dd99c24c309cc860c7cbc6b1973387034f5436d1c8d6")
    version("1.8.0", sha256="68e4ea30f219227dd88e55de2550d3f8c20a20adbdb67ad1e13b50868bb2ac0c")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", when="@1.8.1:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-opt-einsum@2.3.2:", type=("build", "run"))
    depends_on("py-pyro-api@0.1.1:", type=("build", "run"))
    depends_on("py-torch@1.11:", when="@1.8.1:", type=("build", "run"))
    depends_on("py-torch@1.9:", type=("build", "run"))
    depends_on("py-tqdm@4.36:", type=("build", "run"))
