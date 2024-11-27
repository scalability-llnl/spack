# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPamela(PythonPackage):
    """Python wrapper for PAM"""

    pypi = "pamela/pamela-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="65c9389bef7d1bb0b168813b6be21964df32016923aac7515bdf05366acbab6c")

    depends_on("py-setuptools", type="build")
