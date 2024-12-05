# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWord2number(PythonPackage):
    """This is a Python module to convert number words (eg.
    twenty one) to numeric digits (21). It works for positive
    numbers upto the range of 999,999,999,999 (i.e.
    billions)."""

    homepage = "https://w2n.readthedocs.io"
    pypi = "word2number/word2number-1.1.zip"

    license("MIT")

    version("1.1", sha256="70e27a5d387f67b04c71fbb7621c05930b19bfd26efd6851e6e0f9969dcde7d0")

    depends_on("py-setuptools", type="build")
