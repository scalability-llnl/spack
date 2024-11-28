# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTree(PythonPackage):
    """A package for creating and drawing trees."""

    homepage = "https://github.com/PixelwarStudio/PyTree"
    pypi = "Tree/Tree-0.2.4.tar.gz"

    license("MIT")

    version("0.2.4", sha256="f84d8ec9bf50dd69f551da78925a23d110864e7706551f590cdade27646f7883")

    depends_on("pil", type=("build", "run"))
    depends_on("py-svgwrite", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
