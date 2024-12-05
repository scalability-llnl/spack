# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlperfLogging(PythonPackage):
    """MLPerf Compliance Logging Utilities and Helper Functions."""

    homepage = "https://github.com/mlperf/logging"
    url = "https://github.com/mlperf/logging/archive/0.7.1.tar.gz"

    license("Apache-2.0")

    version("0.7.1", sha256="32fb6885d8bbf20e1225dc7ec57dc964649df696278cdd2d575aeef8e891f7bb")

    depends_on("py-setuptools", type="build")
