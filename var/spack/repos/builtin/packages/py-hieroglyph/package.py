# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHieroglyph(PythonPackage):
    """Hieroglyph is an extension for Sphinx which builds HTML
    presentations from ReStructured Text documents.
    """

    homepage = "https://github.com/nyergler/hieroglyph"
    pypi = "hieroglyph/hieroglyph-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("2.1.0", sha256="b4b5db13a9d387438e610c2ca1d81386ccd206944d9a9dd273f21874486cddaf")
    version("1.0.0", sha256="8e137f0b1cd60c47b870011089790d3c8ddb74fcf409a75ddf2c7f2516ff337c")

    depends_on("python@3:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-sphinx@1.2:", when="@1.0.0:1.9", type=("build", "run"))
    depends_on("py-sphinx@2.0:", when="@2.0.0:", type=("build", "run"))
    depends_on("py-six", when="@1.0.0:1.9", type=("build", "run"))
