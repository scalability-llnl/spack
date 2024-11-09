# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPywin32(PythonPackage):
    """Python for Window Extensions."""

    homepage = "https://github.com/mhammond/pywin32"
    url = "https://github.com/mhammond/pywin32/archive/refs/tags/b306.tar.gz"

    license("PSF-2.0")

    version("306", sha256="16e5ad3efbbf997080f67c3010bd4eb0067d499bbade9be1b240b7e85325c167")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
