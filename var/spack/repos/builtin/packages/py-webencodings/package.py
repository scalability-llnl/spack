# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebencodings(PythonPackage):
    """This is a Python implementation of the WHATWG Encoding standard."""

    homepage = "https://github.com/gsnedders/python-webencodings"
    pypi = "webencodings/webencodings-0.5.1.tar.gz"

    license("BSD-2-Clause")

    version("0.5.1", sha256="b36a1c245f2d304965eb4e0a82848379241dc04b865afcc4aab16748587e1923")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
