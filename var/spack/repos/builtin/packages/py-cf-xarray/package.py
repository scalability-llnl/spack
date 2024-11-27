# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfXarray(PythonPackage):
    """A convenience wrapper for using CF attributes on xarray objects."""

    homepage = "https://cf-xarray.readthedocs.io/"
    pypi = "cf_xarray/cf_xarray-0.9.0.tar.gz"

    license("Apache-2.0")

    version("0.9.0", sha256="01213bdc5ed4d41eeb5da179d99076f49a905b1995daef2a0c7ec402b148675c")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    depends_on("py-xarray@2022.03:", type=("build", "run"))
