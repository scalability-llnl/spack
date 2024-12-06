# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEcmwfOpendata(PythonPackage):
    """A package to download ECMWF open data."""

    homepage = "https://github.com/ecmwf/ecmwf-opendata"
    pypi = "ecmwf-opendata/ecmwf-opendata-0.3.3.tar.gz"

    license("Apache-2.0")

    version("0.3.3", sha256="6f3181c7872b72e5529d2b4b7ec6ff08d37c37beee0a498f7f286410be178c6a")

    depends_on("py-setuptools", type="build")
    depends_on("py-multiurl@0.2.1:", type=("build", "run"))
