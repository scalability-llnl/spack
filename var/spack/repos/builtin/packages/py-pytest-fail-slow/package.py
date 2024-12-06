# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestFailSlow(PythonPackage):
    """Fail tests that take too long to run."""

    homepage = "https://github.com/jwodder/pytest-fail-slow"
    pypi = "pytest-fail-slow/pytest-fail-slow-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="bc022f3f4f170b7e3e7d4dff45bd9e7855e4935ae396bb40b4521ce1ef8ea41c")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type="build")

    depends_on("py-pytest@6:", type=("build", "run"))
