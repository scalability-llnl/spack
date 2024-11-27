# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinecache2(PythonPackage):
    """Backports of the linecache module"""

    homepage = "https://github.com/testing-cabal/linecache2"
    pypi = "linecache2/linecache2-1.0.0.tar.gz"

    version("1.0.0", sha256="4b26ff4e7110db76eeb6f5a7b64a82623839d595c2038eeda662f2a2db78e97c")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
