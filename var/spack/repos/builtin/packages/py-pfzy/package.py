# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPfzy(PythonPackage):
    """Python port of the fzy fuzzy string matching algorithm."""

    homepage = "https://github.com/kazhala/pfzy"
    pypi = "pfzy/pfzy-0.3.4.tar.gz"

    license("MIT")

    version("0.3.4", sha256="717ea765dd10b63618e7298b2d98efd819e0b30cd5905c9707223dceeb94b3f1")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
