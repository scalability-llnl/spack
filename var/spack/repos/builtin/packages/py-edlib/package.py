# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEdlib(PythonPackage):
    """Lightweight, super fast library for sequence
    alignment using edit (Levenshtein) distance."""

    homepage = "https://pypi.org/project/edlib/"
    pypi = "edlib/edlib-1.3.9.tar.gz"

    license("MIT")

    version("1.3.9", sha256="64c3dfab3ebe3e759565a0cc71eb4df23cf3ce1713fd558af3c473dddc2a3766")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
