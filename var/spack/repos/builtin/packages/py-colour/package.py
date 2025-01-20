# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColour(PythonPackage):
    """converts and manipulates various color representation (HSL, RVB, web, X11, ...)"""

    homepage = "http://github.com/vaab/colour"
    pypi = "colour/colour-0.1.5.tar.gz"

    license("BSD-2-Clause")

    version("0.1.5", sha256="af20120fefd2afede8b001fbef2ea9da70ad7d49fafdb6489025dae8745c3aee")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-d2to1")
