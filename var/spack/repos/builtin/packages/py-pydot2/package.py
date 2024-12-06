# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydot2(PythonPackage):
    """Python interface to Graphviz's Dot"""

    pypi = "pydot2/pydot2-1.0.33.tar.gz"

    license("MIT")

    version("1.0.33", sha256="02c0e681a1c437077e2bb2522fb81fa322e53ba7002cfda8b894db0392a1bc9b")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyparsing", type=("build", "run"))
