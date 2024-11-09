# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEcmwflibs(PythonPackage):
    """A Python package that wraps some of ECMWF libraries to be used by
    Python interfaces to ECMWF software.
    """

    homepage = "https://github.com/ecmwf/ecmwflibs"
    url = "https://github.com/ecmwf/ecmwflibs/archive/refs/tags/0.6.1.tar.gz"

    license("Apache-2.0")

    version("0.6.1", sha256="9f2153d1b4a07038b975b7d6bb89bbf9e88d6bc4e2ef4d4e067e58a2fb5270d3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-findlibs", type=("build", "run"))
    depends_on("eccodes")
    depends_on("magics")

    def patch(self):
        # Instruct setup.py where to find dependencies
        library_dirs = self.spec["eccodes"].libs.directories + self.spec["magics"].libs.directories
        include_dirs = (
            self.spec["eccodes"].headers.directories + self.spec["magics"].headers.directories
        )
        setup = FileFilter("setup.py")
        setup.filter("library_dirs=.*", f"library_dirs={library_dirs},")
        setup.filter("include_dirs=.*", f"include_dirs={include_dirs},")
