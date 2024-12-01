# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwesomeSlugify(PythonPackage):
    """Python flexible slugify function"""

    homepage = "https://github.com/dimka665/awesome-slugify"
    pypi = "awesome-slugify/awesome-slugify-1.6.5.tar.gz"

    version("1.6.5", sha256="bbdec3fa2187917473a2efad092b57f7125a55f841a7cf6a1773178d32ccfd71")

    depends_on("py-setuptools", type="build")

    depends_on("py-regex", type=("build", "run"))
    depends_on("py-unidecode@0.04.14:0.04", type=("build", "run"))
