# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutomat(PythonPackage):
    """Self-service finite-state machines for the programmer on the go."""

    homepage = "https://github.com/glyph/Automat"
    pypi = "Automat/Automat-20.2.0.tar.gz"

    license("MIT")

    version("20.2.0", sha256="7979803c74610e11ef0c0d68a2942b152df52da55336e0c9d58daf1831cbdf33")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-m2r", type="build")

    depends_on("py-attrs@19.2.0:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
