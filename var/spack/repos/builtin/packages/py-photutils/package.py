# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPhotutils(PythonPackage):
    """
    Photutils is an Astropy package for detection and photometry of astronomical
    sources.
    """

    homepage = "https://github.com/astropy/photutils"
    pypi = "photutils/photutils-1.5.0.tar.gz"

    license("BSD-3-Clause")

    version("1.5.0", sha256="014f7aa5a571401094d5cf9ffb57803b48869233feb80476ce377ecb91113689")

    depends_on("c", type="build")  # generated

    maintainers("meyersbs")

    # From setup.cfg
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy@1.18:", type=("build", "run"))
    depends_on("py-astropy@5.0:", type=("build", "run"))
    # From pyproject.toml
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-cython@0.29.22:", type="build")
    depends_on("py-extension-helpers", type="build")
