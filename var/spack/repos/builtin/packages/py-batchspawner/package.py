# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBatchspawner(PythonPackage):
    """This is a custom spawner for Jupyterhub that is designed for
    installations on clusters using batch scheduling software."""

    homepage = "https://github.com/jupyterhub/batchspawner"
    pypi = "batchspawner/batchspawner-1.1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.1.0", sha256="9bae72f7c1bd9bb11aa58ecc3bc9fae5475a10fdd92dc0c0d67fa7eb95c9dd3a")

    depends_on("python@3.3:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-async-generator@1.8:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jupyterhub@0.5:", type=("build", "run"))
