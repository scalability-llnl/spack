# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClikit(PythonPackage):
    """CliKit is a group of utilities to build beautiful and testable
    command line interfaces."""

    homepage = "https://github.com/sdispater/clikit"
    pypi = "clikit/clikit-0.6.2.tar.gz"

    license("MIT")

    version("0.6.2", sha256="442ee5db9a14120635c5990bcdbfe7c03ada5898291f0c802f77be71569ded59")

    depends_on("python@2.7,3.4:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-pastel@0.2.0:0.2", type=("build", "run"))
    depends_on("py-pylev@1.3:1", type=("build", "run"))
    depends_on("py-crashtest@0.3.0:0.3", when="^python@3.6:3", type=("build", "run"))
