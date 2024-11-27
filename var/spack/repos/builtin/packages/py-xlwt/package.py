# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXlwt(PythonPackage):
    """Library to create spreadsheet files compatible with
    MS Excel 97/2000/XP/2003 XLS files, on any platform,
    with Python 2.6, 2.7, 3.3+."""

    pypi = "xlwt/xlwt-1.3.0.tar.gz"

    version("1.3.0", sha256="c59912717a9b28f1a3c2a98fd60741014b06b043936dcecbc113eaaada156c88")

    depends_on("py-setuptools", type="build")
