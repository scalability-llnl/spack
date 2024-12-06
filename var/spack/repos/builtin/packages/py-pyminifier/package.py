# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyminifier(PythonPackage):
    """Pyminifier is a Python code minifier, obfuscator, and compressor."""

    homepage = "https://liftoff.github.io/pyminifier/"
    pypi = "pyminifier/pyminifier-2.1.tar.gz"

    license("GPL-3.0-or-later")

    version("2.1", sha256="e192618fe901830e9298825b32828bc9555ae8649e05af37bfab2db328546777")

    depends_on("py-setuptools", type="build")
