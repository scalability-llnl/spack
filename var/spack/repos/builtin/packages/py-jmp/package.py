# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJmp(PythonPackage):
    """JMP is a Mixed Precision library for JAX."""

    homepage = "https://github.com/deepmind/jmp"
    # pypi tarball has requirements.txt missing
    url = "https://github.com/deepmind/jmp/archive/refs/tags/v0.0.2.tar.gz"

    license("Apache-2.0")

    version("0.0.2", sha256="4d242fb14502b15a7c072e112bdcd7cb5d8b373d9733162eea23e0b9b7dbb6d0")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.19.5:", type=("build", "run"))
    depends_on("py-jax@0.1.71:", type=("build", "run"))
