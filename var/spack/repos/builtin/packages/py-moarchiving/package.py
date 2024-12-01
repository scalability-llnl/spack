# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMoarchiving(PythonPackage):
    """
    Biobjective Archive class with hypervolume indicator and uncrowded
    hypervolume improvement computation.
    """

    homepage = "https://github.com/CMA-ES/moarchiving"
    pypi = "moarchiving/moarchiving-0.6.0.tar.gz"

    maintainers("LydDeb")

    version("0.6.0", sha256="705ded992d399bc1ac703e68391bded6f64e1bde81b2bb25061eaa6208b5b29a")

    variant("arbitrary_precision", default=False, description="Build with Fraction support")

    depends_on("py-setuptools", type="build")
    depends_on("py-fraction", when="+arbitrary_precision", type=("build", "run"))
