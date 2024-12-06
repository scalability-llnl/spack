# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsodate(PythonPackage):
    """This module implements ISO 8601 date, time and duration parsing. The
    implementation follows ISO8601:2004 standard, and implements only date/time
    representations mentioned in the standard. If something is not mentioned
    there, then it is treated as non existent, and not as an allowed option."""

    homepage = "https://github.com/gweis/isodate/"
    pypi = "isodate/isodate-0.6.0.tar.gz"

    version("0.6.1", sha256="48c5881de7e8b0a0d648cb024c8062dc84e7b840ed81e864c7614fd3c127bde9")
    version("0.6.0", sha256="2e364a3d5759479cdb2d37cce6b9376ea504db2ff90252a2e5b7cc89cc9ff2d8")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
