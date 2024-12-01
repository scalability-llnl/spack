# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParsedatetime(PythonPackage):
    """Parse human-readable date/time strings."""

    homepage = "https://github.com/bear/parsedatetime"
    pypi = "parsedatetime/parsedatetime-2.5.tar.gz"

    version("2.5", sha256="d2e9ddb1e463de871d32088a3f3cea3dc8282b1b2800e081bd0ef86900451667")

    depends_on("py-setuptools", type="build")
