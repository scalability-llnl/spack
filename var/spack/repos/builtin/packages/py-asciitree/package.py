# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsciitree(PythonPackage):
    """Draws ASCII trees."""

    homepage = "https://github.com/mbr/asciitree"
    pypi = "asciitree/asciitree-0.3.3.tar.gz"

    license("MIT")

    version("0.3.3", sha256="4aa4b9b649f85e3fcb343363d97564aa1fb62e249677f2e18a96765145cc0f6e")

    depends_on("py-setuptools", type="build")
