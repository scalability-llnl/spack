# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPastedeploy(PythonPackage):
    """Load, configure, and compose WSGI applications and servers"""

    homepage = "https://docs.pylonsproject.org/projects/pastedeploy"
    pypi = "PasteDeploy/PasteDeploy-3.0.1.tar.gz"

    license("MIT")

    version("3.0.1", sha256="5f4b4d5fddd39b8947ea727161e366bf55b90efc60a4d1dd7976b9031d0b4e5f")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@41:", type="build")

    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
