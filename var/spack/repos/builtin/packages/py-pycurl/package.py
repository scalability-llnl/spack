# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycurl(PythonPackage):
    """PycURL is a Python interface to libcurl. PycURL can be used to fetch
    objects identified by a URL from a Python program."""

    homepage = "http://pycurl.io/"
    pypi = "pycurl/pycurl-7.43.0.tar.gz"

    license("curl")

    version("7.45.1", sha256="a863ad18ff478f5545924057887cdae422e1b2746e41674615f687498ea5b88a")
    version("7.44.1", sha256="5bcef4d988b74b99653602101e17d8401338d596b9234d263c728a0c3df003e8")
    version("7.43.0", sha256="aa975c19b79b6aa6c0518c0cc2ae33528900478f0b500531dbcdbf05beec584c")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("python@3.5:", when="@7.44.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("curl@7.19.0:")
