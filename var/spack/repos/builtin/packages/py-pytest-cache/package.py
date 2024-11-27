# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestCache(PythonPackage):
    """pytest plugin to provide cross-test run caching functionality to
    plugins and test runs.
    """

    homepage = "https://bitbucket.org/hpk42/pytest-cache/src/default/"
    pypi = "pytest-cache/pytest-cache-1.0.tar.gz"

    license("MIT")

    version("1.0", sha256="be7468edd4d3d83f1e844959fd6e3fd28e77a481440a7118d430130ea31b07a9")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@2.2:", type=("build", "run"))
    depends_on("py-execnet@1.2:", type=("build", "run"))
