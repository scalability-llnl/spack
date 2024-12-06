# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPetname(PythonPackage):
    """Generate human-readable, random object names."""

    homepage = "https://launchpad.net/python-petname"
    pypi = "petname/petname-2.6.tar.gz"

    version("2.6", sha256="981c31ef772356a373640d1bb7c67c102e0159eda14578c67a1c99d5b34c9e4c")
    version("2.2", sha256="be1da50a6aa01e39840e9a4b79b527a333b256733cb681f52669c08df7819ace")

    depends_on("py-setuptools", type="build")
