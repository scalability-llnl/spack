# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQmtest(PythonPackage):
    """A general purpose testing framework"""

    homepage = "https://github.com/MentorEmbedded/qmtest"
    url = "https://github.com/MentorEmbedded/qmtest/archive/refs/tags/2.4.1.tar.gz"

    maintainers("haralmha")

    license("GPL-2.0-only")

    version("2.4.1", sha256="098f705aea9c8f7f5b6b5fe131974cee33b50cad3e13977e39708f306ce9ac91")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Patch to fix python 3.10 and above compatibility
    patch("wininst.patch", when="@2.4.1^python@3.10:")

    depends_on("python@2.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
