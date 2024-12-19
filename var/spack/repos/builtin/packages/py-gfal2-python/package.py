# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGfal2Python(PythonPackage):
    """Python2 and 3 bindings for gfal2."""

    homepage = "https://github.com/cern-fts/gfal2-python"
    pypi = "gfal2-python/gfal2-python-1.13.0.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("1.13.0", sha256="5be42cc894fa20af3d6f6dbb30dfd4d29ab49bd5f15b3e3e754aa25c5ed17997")

    depends_on("cxx", type="build")
    depends_on("python", type="build")

    depends_on("py-setuptools", type="build")
    depends_on("cmake", type="build")

    depends_on("boost +python")
    depends_on("glib")
    depends_on("gfal2")

    def patch(self):
        filter_file(
            r"\'-DSKIP_TESTS=TRUE\',",
            "'-DSKIP_TESTS=TRUE', f'-DPython_EXECUTABLE={sys.executable}',",
            "setup.py",
        )
