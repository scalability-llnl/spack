# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtomicwrites(PythonPackage):
    """Atomic file writes."""

    homepage = "https://github.com/untitaker/python-atomicwrites"
    pypi = "atomicwrites/atomicwrites-1.3.0.tar.gz"

    license("MIT")

    version("1.4.1", sha256="81b2c9071a49367a7f770170e5eec8cb66567cfbbc8c73d20ce5ca4a8d71cf11")
    version("1.4.0", sha256="ae70396ad1a434f9c7046fd2dd196fc04b12f9e91ffb859164193be8b6168a7a")
    version("1.3.0", sha256="75a9445bac02d8d058d5e1fe689654ba5a6556a1dfd8ce6ec55a0ed79866cfa6")
    version("1.1.5", sha256="240831ea22da9ab882b551b31d4225591e5e447a68c5e188db5b89ca1d487585")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
