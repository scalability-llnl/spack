# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorlover(PythonPackage):
    """Color scales in Python for humans."""

    homepage = "https://github.com/plotly/colorlover"
    pypi = "colorlover/colorlover-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="b8fb7246ab46e1f5e6715649453c1762e245a515de5ff2d2b4aab7a6e67fa4e2")

    depends_on("py-setuptools", type="build")
