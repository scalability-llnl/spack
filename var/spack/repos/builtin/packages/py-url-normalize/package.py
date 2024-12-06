# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUrlNormalize(PythonPackage):
    """URL normalization for Python."""

    homepage = "https://github.com/niksite/url-normalize"
    pypi = "url-normalize/url-normalize-1.4.3.tar.gz"

    license("MIT")

    version("1.4.3", sha256="d23d3a070ac52a67b83a1c59a0e68f8608d1cd538783b401bc9de2c0fac999b2")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry@0.12:", type="build")

    depends_on("py-six", type=("build", "run"))
