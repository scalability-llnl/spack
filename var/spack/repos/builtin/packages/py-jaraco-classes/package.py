# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaracoClasses(PythonPackage):
    """Utility functions for Python class constructs"""

    homepage = "https://github.com/jaraco/jaraco.classes"
    pypi = "jaraco.classes/jaraco.classes-3.2.2.tar.gz"

    license("MIT")

    version("3.2.3", sha256="89559fa5c1d3c34eff6f631ad80bb21f378dbcbb35dd161fd2c6b93f5be2f98a")
    version("3.2.2", sha256="6745f113b0b588239ceb49532aa09c3ebb947433ce311ef2f8e3ad64ebb74594")

    depends_on("py-setuptools@56:", type="build")
    depends_on("py-setuptools-scm@3.4.1: +toml", type="build")

    depends_on("py-more-itertools", type=("build", "run"))
