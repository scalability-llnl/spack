# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReadchar(PythonPackage):
    """Library to easily read single chars and key strokes."""

    homepage = "https://github.com/magmax/python-readchar"
    pypi = "readchar/readchar-4.0.5.tar.gz"

    license("MIT")

    version("4.0.5", sha256="08a456c2d7c1888cde3f4688b542621b676eb38cd6cfed7eb6cb2e2905ddc826")

    depends_on("py-setuptools@41:", type=("build", "run"))
