# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCounter(PythonPackage):
    """Counter package defines the "counter.Counter" class similar to
    bags or multisets in other languages."""

    homepage = "https://github.com/KelSolaar/Counter"
    pypi = "Counter/Counter-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="9e008590e360936a66c98e1a01e7a9a0ecf6af19cc588107121f5fb4613bb60c")

    depends_on("py-setuptools", type="build")
