# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBeancount(PythonPackage):
    """A double-entry bookkeeping computer language that lets you define
    financial transaction records in a text file, read them in memory,
    generate a variety of reports from them, and provides a web
    interface.."""

    homepage = "http://furius.ca/beancount/"
    pypi = "beancount/beancount-2.3.3.tar.gz"

    license("GPL-2.0-only")

    version("2.3.3", sha256="d9a29839ea867d1dda7af1f4bf5d3959aa7c1574cd4a0bc86f69ee64c555c71c")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))

    depends_on("py-bottle", type=("build", "run"))
    depends_on("py-lxml+htmlsoup", type=("build", "run"))
    depends_on("py-ply", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-python-magic", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-chardet", type=("build", "run"))
    depends_on("py-google-api-python-client", type=("build", "run"))
