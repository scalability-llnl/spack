# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXonsh(PythonPackage):
    """Python-powered, cross-platform, Unix-gazing shell language and command prompt."""

    homepage = "https://xon.sh/"
    pypi = "xonsh/xonsh-0.11.0.tar.gz"

    maintainers("mdorier")

    version("0.11.0", sha256="0d9c3d9a4e8b8199ae697fbc9d1e0ae55085cdbdd4306d04813350996f9c15dc")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
