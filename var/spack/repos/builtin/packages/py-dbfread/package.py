# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDbfread(PythonPackage):
    """DBF is a file format used by databases such dBase, Visual FoxPro, and
    FoxBase+. This library reads DBF files and returns the data as native
    Python data types for further processing. It is primarily intended for
    batch jobs and one-off scripts."""

    homepage = "https://dbfread.readthedocs.io/en/latest/"
    pypi = "dbfread/dbfread-2.0.7.tar.gz"

    license("MIT")

    version("2.0.7", sha256="07c8a9af06ffad3f6f03e8fe91ad7d2733e31a26d2b72c4dd4cfbae07ee3b73d")

    depends_on("py-setuptools", type="build")
