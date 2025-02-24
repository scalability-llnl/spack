# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVerspec(PythonPackage):
    """verspec is a Python library for handling software versions and
    specifiers, adapted from the packaging package."""

    homepage = "https://github.com/jimporter/verspec"
    pypi = "verspec/verspec-0.1.0.tar.gz"

    license("BSD-2-Clause")

    version("0.1.0", sha256="c4504ca697b2056cdb4bfa7121461f5a0e81809255b41c03dda4ba823637c01e")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
