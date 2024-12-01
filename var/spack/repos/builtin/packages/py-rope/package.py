# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRope(PythonPackage):
    """a python refactoring library."""

    homepage = "https://github.com/python-rope/rope"
    pypi = "rope/rope-0.10.5.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.11.0", sha256="a108c445e1cd897fe19272ab7877d172e7faf3d4148c80e7d20faba42ea8f7b2")
    version("0.10.7", sha256="a09edfd2034fd50099a67822f9bd851fbd0f4e98d3b87519f6267b60e50d80d1")
    version("0.10.6", sha256="9700e163f3b05ef4c68133a39d436c253a84b35baf662c2d63407da7bfa08edf")
    version("0.10.5", sha256="2ff6099e65798f9e27da5026cc7136b4d9b340fc817031ccb4318f61f448127f")

    patch("fix_readme_unicode.patch", when="@0.10.5:0.11.0")

    depends_on("py-setuptools", type="build")
