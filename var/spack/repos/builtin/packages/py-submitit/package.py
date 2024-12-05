# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySubmitit(PythonPackage):
    """Python toolbox for submitting jobs to Slurm."""

    homepage = "https://github.com/facebookincubator/submitit"
    pypi = "submitit/submitit-1.3.3.tar.gz"

    license("MIT")

    version("1.4.5", sha256="d12cbbfc98a8c1777c4f6e87f73f063dafdba15653bca2984223b038d41f8223")
    version("1.3.3", sha256="efaa77b2df9ea9ee02545478cbfc377853ddf8016bff59df6988bebcf51ffa7e")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"), when="@:1.4.1")
    depends_on("py-flit-core@3.2:3", type="build", when="@1.4.2:")

    depends_on("py-cloudpickle@1.2.1:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.2:", type=("build", "run"))
