# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLap(PythonPackage):
    """lap is a linear assignment problem solver using
    Jonker-Volgenant algorithm for dense (LAPJV) or sparse (LAPMOD)
    matrices."""

    homepage = "https://github.com/gatagat/lap"
    pypi = "lap/lap-0.4.0.tar.gz"

    license("BSD-2-Clause")

    version("0.4.0", sha256="c4dad9976f0e9f276d8a676a6d03632c3cb7ab7c80142e3b27303d49f0ed0e3b")

    depends_on("cxx", type="build")  # generated
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.21:", type="build")
    depends_on("py-numpy@1.10.1:", type=("build", "run"))
