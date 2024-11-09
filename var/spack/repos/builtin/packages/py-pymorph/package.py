# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymorph(PythonPackage):
    """Pymorph is a collection of pure python implementations of many image
    morphology functions.
    """

    homepage = "https://luispedro.org/software/pymorph/"
    pypi = "pymorph/pymorph-0.96.tar.gz"

    version("0.96", sha256="5dd648e4cb4c3495ee6031bc8020ed8216f3d6cb8c0dcd0427b215b75d7d29ad")

    depends_on("py-setuptools", type="build")
