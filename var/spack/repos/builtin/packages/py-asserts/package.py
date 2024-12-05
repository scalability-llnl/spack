# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsserts(PythonPackage):
    """Stand-alone Assertions."""

    homepage = "https://github.com/srittau/python-asserts"
    url = "https://github.com/srittau/python-asserts/archive/v0.10.0.tar.gz"

    license("MIT")

    version("0.10.0", sha256="3466cf32c36d97ee2802121438003693546f590be81095317d0d698066bb5df7")
    version("0.9.1", sha256="a73ea6b2ddc77364a5f0e13197f00662485944a6dd31c1f7555ff2f99c0f7319")
    version("0.9.0", sha256="e3b8b06309234f9a7c6e4679e0f3cc127cf18da95c30fbb524ff47d439e22b17")
    version("0.8.6", sha256="8a477746dbc501ac0d1fe9e593a1faafa7d361ceca79d994d3b2ebeecc7fbf32")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
