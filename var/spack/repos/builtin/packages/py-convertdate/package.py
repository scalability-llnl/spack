# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConvertdate(PythonPackage):
    """Converts between Gregorian dates and other calendar
    systems.Calendars included: Baha'i, French Republican, Hebrew,
    Indian Civil, Islamic, ISO, Julian, Mayan and Persian."""

    homepage = "https://github.com/fitnr/convertdate/"
    pypi = "convertdate/convertdate-2.2.0.tar.gz"

    license("MIT")

    version("2.2.0", sha256="9d2b0cd8d5382d2458d4cfa59665abba398a9e9bfd3a01c6f61b7b47768d28bf")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytz@2014.10:2019.13", type=("build", "run"))
    depends_on("py-pymeeus@0.3.6:1", type=("build", "run"))
