# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpentree(PythonPackage):
    """Library for interacting with Open Tree of Life resources."""

    homepage = "https://github.com/OpenTreeOfLife/python-opentree"
    pypi = "opentree/opentree-1.0.1.tar.gz"

    maintainers("snehring")

    version("1.0.1", sha256="a765ae37cd72c232c292506c170656aaaa4be81e6de6ccd4845eec01bfe45e4d")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-requests@2.18:", type=("build", "run"))
    depends_on("py-dendropy@4.4.0:", type=("build", "run"))
