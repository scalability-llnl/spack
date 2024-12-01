# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCommonmark(PythonPackage):
    """commonmark.py is a pure Python port of jgm's commonmark.js, a Markdown
    parser and renderer for the CommonMark specification, using only native
    modules."""

    homepage = "https://github.com/readthedocs/commonmark.py"
    pypi = "commonmark/commonmark-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version("0.9.1", sha256="452f9dc859be7f06631ddcb328b6919c67984aca654e5fefb3914d54691aed60")
    version("0.9.0", sha256="867fc5db078ede373ab811e16b6789e9d033b15ccd7296f370ca52d1ee792ce0")

    depends_on("py-setuptools", type="build")
    depends_on("py-future", type=("build", "run"), when="@0.9.0")
