# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyContexttimer(PythonPackage):
    """A timer as a context manager.

    contexttimer provides you with a couple of utilities to quickly measure the
    execution time of a code block or a function.
    """

    homepage = "https://github.com/brouberol/contexttimer"
    pypi = "contexttimer/contexttimer-0.3.3.tar.gz"

    version("0.3.3", sha256="35a1efd389af3f1ca509f33ff23e17d98b66c8fde5ba2a4eb8a8b7fa456598a5")

    depends_on("py-setuptools", type="build")
