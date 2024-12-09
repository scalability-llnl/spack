# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDocoptNg(PythonPackage):
    """Command-line interface description language."""

    homepage = "https://github.com/jazzband/docopt-ng"
    pypi = "docopt-ng/docopt_ng-0.6.2.tar.gz"

    license("MIT", checked_by="matz-e")

    version("0.9.0", sha256="91c6da10b5bb6f2e9e25345829fb8278c78af019f6fc40887ad49b060483b1d7")

    depends_on("py-pdm-backend", type="build")
