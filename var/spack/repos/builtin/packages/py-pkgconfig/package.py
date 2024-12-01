# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPkgconfig(PythonPackage):
    """Interface Python with pkg-config."""

    homepage = "https://github.com/matze/pkgconfig"
    pypi = "pkgconfig/pkgconfig-1.2.2.tar.gz"

    license("MIT")

    version("1.5.5", sha256="deb4163ef11f75b520d822d9505c1f462761b4309b1bb713d08689759ea8b899")
    version("1.5.1", sha256="97bfe3d981bab675d5ea3ef259045d7919c93897db7d3b59d4e8593cba8d354f")
    version("1.4.0", sha256="048c3b457da7b6f686b647ab10bf09e2250e4c50acfe6f215398a8b5e6fcdb52")
    version("1.2.2", sha256="3685ba02a9b72654a764b728b559f327e1dbd7dc6ebc310a1bd429666ee202aa")

    depends_on("python@3.3:", when="@1.5.5:", type=("build", "run"))
    depends_on("python@2.7,3.3:", when="@1.5:", type=("build", "run"))
    depends_on("python@2.6:2.7,3.3:", when="@1.4:", type=("build", "run"))
    depends_on("py-poetry-core@1:", when="@1.5.2:", type="build")
    depends_on("py-poetry@0.12:", when="@1.5.0:1.5.1", type="build")
    depends_on("py-setuptools", when="@:1.4", type="build")
    depends_on("pkgconfig", type=("build", "run"))
