# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrxPython(PythonPackage):
    """Experiments with new file format for tractography."""

    homepage = "https://tee-ar-ex.github.io/trx-python/"
    pypi = "trx-python/trx-python-0.2.9.tar.gz"

    maintainers("ChristopherChristofi")

    license("BSD-2-Clause")

    version("0.2.9", sha256="16b4104d7c991879c601f60e8d587decac50ce60388aae8d0c754a92136d1caf")

    depends_on("py-setuptools@42.0:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type=("build", "run"))
    depends_on("py-setuptools-scm-git-archive", type="build")
    depends_on("py-packaging@19.0:", type="build")
    depends_on("py-cython@0.29:", type="build")
    depends_on("py-deepdiff", type=("build", "run"))
    depends_on("py-nibabel@5:", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"))
