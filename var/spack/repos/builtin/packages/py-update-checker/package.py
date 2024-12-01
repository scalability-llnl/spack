# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUpdateChecker(PythonPackage):
    """A python module that will check for package updates."""

    homepage = "https://github.com/bboe/update_checker"
    pypi = "update_checker/update_checker-0.18.0.tar.gz"

    license("BSD-2-Clause")

    version("0.18.0", sha256="6a2d45bb4ac585884a6b03f9eade9161cedd9e8111545141e9aa9058932acb13")
    version("0.17", sha256="2def8db7f63bd45c7d19df5df570f3f3dfeb1a1f050869d7036529295db10e62")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", type=("build", "run"), when="@0.18.0:")
    depends_on("python@2.7:2.8,3.3:", type=("build", "run"), when="@0.17")
    depends_on("py-requests@2.3.0:", type=("build", "run"))
