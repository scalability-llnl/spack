# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGriddataformats(PythonPackage):
    """The gridDataFormats package provides classes to unify reading
    and writing n-dimensional datasets. One can read grid data from
    files, make them available as a Grid object, and write out the
    data again."""

    homepage = "http://www.mdanalysis.org/GridDataFormats"
    pypi = "GridDataFormats/GridDataFormats-0.5.0.tar.gz"

    maintainers("RMeli")

    license("LGPL-3.0-only")

    version("1.0.2", sha256="b93cf7f36fce33dbc428026f26dba560d5c7ba2387caca495bad920f90094502")
    version("1.0.1", sha256="ad2c9ab7d672a6d8c426de7d083eee4f3e2b0bd59391675d30683c768ab83cc4")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:3.11", when="@1.0.1", type=("build", "run"))
    depends_on("python@3.9:3.12", when="@1.0.2:", type=("build", "run"))
    depends_on("py-numpy@1.19:", when="@1.0.1", type=("build", "run"))
    depends_on("py-numpy@1.21:", when="@1.0.2:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
