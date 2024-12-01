# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFypp(PythonPackage):
    """Python powered Fortran preprocessor."""

    homepage = "https://github.com/aradi/fypp"
    url = "https://github.com/aradi/fypp/archive/2.1.1.zip"

    license("BSD-2-Clause")

    version("3.1", sha256="bac9d02be308b6bff7fd17da835f01fb9ce9b2dddaaad1ccd22ac7628b2dc53c")
    version("2.1.1", sha256="3744ad17045e91466bbb75a33ce0cab0f65bc2c377127067a932cdf15655e049")

    depends_on("py-setuptools", type="build")
