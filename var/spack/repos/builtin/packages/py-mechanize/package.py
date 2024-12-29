# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMechanize(PythonPackage):
    """Stateful programmatic web browsing."""

    homepage = "https://github.com/python-mechanize/mechanize"
    pypi = "mechanize/mechanize-0.4.3.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("0.4.10", sha256="1dea947f9be7ea0ab610f7bbc4a4e36b45d6bfdfceea29ad3d389a88a1957ddf")
    version("0.4.3", sha256="d7d7068be5e1b3069575c98c870aaa96dd26603fe8c8697b470e2f65259fddbf")
    version("0.2.5", sha256="2e67b20d107b30c00ad814891a095048c35d9d8cb9541801cebe85684cc84766")

    depends_on("py-setuptools", type="build")
    depends_on("py-html5lib@0.999999999:", when="@0.4:", type=("build", "run"))
    depends_on("python@2.7:", type=("build", "run"))
