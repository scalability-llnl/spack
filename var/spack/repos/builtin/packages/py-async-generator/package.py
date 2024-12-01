# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsyncGenerator(PythonPackage):
    """Provides async generator functionality to python 3.5."""

    pypi = "async_generator/async_generator-1.10.tar.gz"

    license("Apache-2.0")

    version("1.10", sha256="6ebb3d106c12920aaae42ccb6f787ef5eefdcdd166ea3d628fa8476abe712144")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:")
