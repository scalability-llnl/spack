# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySemver(PythonPackage):
    """A Python module for semantic versioning.
    Simplifies comparing versions."""

    homepage = "https://semver.org/"
    pypi = "semver/semver-2.8.1.tar.gz"

    license("BSD-3-Clause")

    version("3.0.1", sha256="9ec78c5447883c67b97f98c3b6212796708191d22e4ad30f4570f840171cbce1")
    version("2.8.1", sha256="5b09010a66d9a3837211bb7ae5a20d10ba88f8cb49e92cb139a69ef90d5060d8")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", when="@3:", type="build")
