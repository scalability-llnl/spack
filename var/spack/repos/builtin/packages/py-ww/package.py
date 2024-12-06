# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWw(PythonPackage):
    """Wrappers for Python builtins with higher-level APIs."""

    homepage = "https://github.com/tygs/ww/"
    pypi = "ww/ww-0.2.1.tar.gz"

    license("MIT")

    version("0.2.1", sha256="3664f1f91bf927fe597ab153e8df73c8954927258b3737220efd1cb9912ebd7e")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")

    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-formatizer", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
