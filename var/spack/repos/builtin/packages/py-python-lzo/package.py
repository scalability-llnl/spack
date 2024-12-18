# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLzo(PythonPackage):
    """This module provides Python bindings for the LZO data compression
    library."""

    homepage = "https://github.com/jd-boyd/python-lzo"
    pypi = "python-lzo/python-lzo-1.12.tar.gz"

    license("GPL-2.0-only")

    version("1.15", sha256="a57aaa00c5c3a0515dd9f7426ba2cf601767dc19dc023d8b99d4a13b0a327b49")
    version("1.12", sha256="97a8e46825e8f1abd84c2a3372bc09adae9745a5be5d3af2692cd850dac35345")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@42:", when="@1.13:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("lzo")
