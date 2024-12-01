# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsi2html(PythonPackage):
    """Convert text with ansi color codes to HTML"""

    homepage = "https://github.com/pycontribs/ansi2html"
    pypi = "ansi2html/ansi2html-1.6.0.tar.gz"

    maintainers("dorton21")

    license("LGPL-3.0-or-later")

    version("1.6.0", sha256="0f124ea7efcf3f24f1f9398e527e688c9ae6eab26b0b84e1299ef7f94d92c596")

    depends_on("py-setuptools", type="build")
    depends_on("py-pip", type="build")
