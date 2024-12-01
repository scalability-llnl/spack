# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPprintpp(PythonPackage):
    """A drop-in replacement for pprint that's actually pretty"""

    homepage = "https://github.com/wolever/pprintpp"
    pypi = "pprintpp/pprintpp-0.4.0.tar.gz"

    version("0.4.0", sha256="ea826108e2c7f49dc6d66c752973c3fc9749142a798d6b254e1e301cfdbc6403")

    depends_on("py-setuptools", type="build")
