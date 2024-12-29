# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOutdated(PythonPackage):
    """This is a mini-library which, given a package name and a version, checks if
    it's the latest version available on PyPI."""

    homepage = "https://github.com/alexmojaki/outdated"
    pypi = "outdated/outdated-0.2.2.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("0.2.2", sha256="4b7fdec88e36711120d096d485fc4d5035e4e5ffbd907cf3a6ce2af43058b970")

    depends_on("py-setuptools@44:", type=("build", "run"))
    depends_on("py-setuptools-scm@3.4.3:+toml", type="build")
    depends_on("py-littleutils", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
