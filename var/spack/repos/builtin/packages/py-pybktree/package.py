# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybktree(PythonPackage):
    """pybktree: pure-Python BK-tree data structure to allow fast querying of close matches"""

    homepage = "https://github.com/benhoyt/pybktree"
    pypi = "pybktree/pybktree-1.1.tar.gz"

    license("MIT")

    version("1.1", sha256="eec0037cdd3d7553e6d72435a4379bede64be17c6712f149e485169638154d2b")

    depends_on("py-setuptools", type="build")
