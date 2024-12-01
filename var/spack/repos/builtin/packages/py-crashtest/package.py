# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCrashtest(PythonPackage):
    """Crashtest is a Python library that makes exceptions handling
    and inspection easier."""

    homepage = "https://github.com/sdispater/crashtest"
    pypi = "crashtest/crashtest-0.3.1.tar.gz"

    license("MIT")

    version("0.4.1", sha256="80d7b1f316ebfbd429f648076d6275c877ba30ba48979de4191714a75266f0ce")
    version("0.4.0", sha256="d629b00f1d4e79c316909f4eb763bbcb29b510d65fbde1365a1ceb93ab7fa4c8")
    version("0.3.1", sha256="42ca7b6ce88b6c7433e2ce47ea884e91ec93104a4b754998be498a8e6c3d37dd")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("python@3.7:3", when="@0.4.0:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-poetry-core@1.1.0:", when="@0.4.1:", type="build")
