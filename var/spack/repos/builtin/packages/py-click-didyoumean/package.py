# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyClickDidyoumean(PythonPackage):
    """Enable git-like did-you-mean feature in click"""

    homepage = "https://github.com/click-contrib/click-didyoumean"
    pypi = "click-didyoumean/click-didyoumean-0.0.3.tar.gz"

    license("MIT")

    version("0.0.3", sha256="112229485c9704ff51362fe34b2d4f0b12fc71cc20f6d2b3afabed4b8bfa6aeb")

    depends_on("python@3.0:", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-setuptools", type="build")
