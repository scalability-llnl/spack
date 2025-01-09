# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlawfinder(PythonPackage, SourceforgePackage):
    """a program that examines source code looking for security weaknesses"""

    homepage = "https://dwheeler.com/flawfinder/"
    sourceforge_mirror_path = "project/flawfinder/flawfinder-2.0.19.tar.gz"

    license("GPL-2.0+")

    version("2.0.19", sha256="fe550981d370abfa0a29671346cc0b038229a9bd90b239eab0f01f12212df618")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
