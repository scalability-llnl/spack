# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathPy(PythonPackage):
    """A module wrapper for os.path"""

    homepage = "https://github.com/jaraco/path.py"
    pypi = "path.py/path.py-12.0.1.tar.gz"

    license("MIT")

    version("12.0.1", sha256="9f2169633403aa0423f6ec000e8701dd1819526c62465f5043952f92527fea0f")
    version("5.2", sha256="9916ae9aa603ce7e131e4ac76c25bcdbf6208f8fe5cc565a5022b85dc9d7022c")

    depends_on("py-setuptools", type="build")

    def url_for_version(self, version):
        if version >= Version("7.6.1"):
            return "https://pypi.io/packages/source/p/path.py/path.py-{0}.tar.gz".format(version)
        else:
            return "https://github.com/jaraco/path.py/archive/{0}.tar.gz".format(version)
