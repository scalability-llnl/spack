# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetupmeta(PythonPackage):
    """Simplify your setup.py."""

    homepage = "https://github.com/codrsquad/setupmeta"
    pypi = "setupmeta/setupmeta-3.3.0.tar.gz"

    license("MIT")

    version("3.4.0", sha256="f986a1d9c5b595a840d71d888950c7cc6bbb586b4145d04e7992501e280e07c3")
    version("3.3.2", sha256="221463a64d2528ba558f14b087410e05a7ef0dab17d19004f124a262d6e007f5")
    version("3.3.0", sha256="32914af4eeffb8bf1bd45057254d9dff4d16cb7ae857141e07698f7ac19dc960")

    depends_on("py-setuptools", type=("build", "run"))
