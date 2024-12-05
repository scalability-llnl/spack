# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProglog(PythonPackage):
    """Proglog is a progress logging system for Python. It
    allows to build complex libraries while giving the user
    control on the management of logs, callbacks and progress
    bars."""

    homepage = "https://pypi.org/project/proglog/"
    pypi = "proglog/proglog-0.1.9.tar.gz"

    license("MIT")

    version("0.1.9", sha256="d8c4ccbf2138e0c5e3f3fc0d80dc51d7e69dcfe8bfde4cacb566725092a5b18d")

    depends_on("py-setuptools", type="build")
    depends_on("py-tqdm", type=("build", "run"))
