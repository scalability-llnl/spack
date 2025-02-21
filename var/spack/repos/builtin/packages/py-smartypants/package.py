# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmartypants(PythonPackage):
    """smartypants is a Python fork of SmartyPants."""

    homepage = "https://github.com/leohemsted/smartypants.py"

    # PyPI only has the wheel
    url = "https://github.com/leohemsted/smartypants.py/archive/refs/tags/v2.0.1.tar.gz"

    license("BSD-3-Clause")

    version("2.0.1", sha256="b98191911ff3b4144ef8ad53e776a2d0ad24bd508a905c6ce523597c40022773")

    depends_on("py-setuptools", type="build")
