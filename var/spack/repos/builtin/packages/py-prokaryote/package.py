# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProkaryote(PythonPackage):
    """CellProfiler's Java dependencies."""

    homepage = "https://github.com/CellProfiler/prokaryote"
    pypi = "prokaryote/prokaryote-2.4.4.tar.gz"

    maintainers("omsai")

    license("GPL-3.0-or-later", checked_by="omsai")

    version("2.4.4", sha256="0a147b8b9a0a7279aa773e6a8fe459eb49f6de479f7afe7203dc4ac10dc8b587")

    depends_on("python@2.7:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
