# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCligj(PythonPackage):
    """Common arguments and options for GeoJSON processing commands, using Click."""

    homepage = "https://github.com/mapbox/cligj"
    pypi = "cligj/cligj-0.7.2.tar.gz"

    license("BSD-3-Clause")

    version("0.7.2", sha256="a4bc13d623356b373c2c27c53dbd9c68cae5d526270bfa71f6c6fa69669c6b27")
    version("0.5.0", sha256="6c7d52d529a78712491974f975c33473f430c0f7beb18c0d7a402a743dcb460a")
    version("0.4.0", sha256="12ad07994f5c1173b06087ffbaacec52f9ebe4687926e5aacfc22b6b0c8b3f54")

    depends_on("python@2.7:2,3.3:3", when="@0.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click@4:", type=("build", "run"))
    depends_on("py-click@4:7", when="@0.5.0", type=("build", "run"))
