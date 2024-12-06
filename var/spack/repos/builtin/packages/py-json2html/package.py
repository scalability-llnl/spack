# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJson2html(PythonPackage):
    """Python wrapper to convert JSON into a human readable HTML Table
    representation."""

    homepage = "https://github.com/softvar/json2html"
    pypi = "json2html/json2html-1.3.0.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("1.3.0", sha256="8951a53662ae9cfd812685facdba693fc950ffc1c1fd1a8a2d3cf4c34600689c")

    depends_on("py-setuptools", type="build")
