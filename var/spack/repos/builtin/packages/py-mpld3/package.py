# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpld3(PythonPackage):
    """An interactive D3js-based viewer which brings matplotlib graphics
    to the browser."""

    homepage = "https://mpld3.github.io/"
    pypi = "mpld3/mpld3-0.3.tar.gz"

    license("BSD-3-Clause")

    version("0.5.8", sha256="1a167dbef836dd7c66d8aa71c06a32d50bffa18725f304d93cb74fdb3545043b")
    version("0.5.5", sha256="b080f3535238a71024c0158280ab4f6091717c45347c41c907012f8dd6da1bd5")
    version("0.3", sha256="4d455884a211bf99b37ecc760759435c7bb6a5955de47d8daf4967e301878ab7")

    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@1.3:", type=("build", "run"))
    depends_on("py-matplotlib@2.2.2:", type=("build", "run"), when="@0.5.5:")
    depends_on("py-jinja2@2.7:", type=("build", "run"))
