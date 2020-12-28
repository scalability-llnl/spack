# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyApplicationinsights(PythonPackage):
    """This project extends the Application Insights API surface to support
    Python."""

    homepage = "https://github.com/Microsoft/ApplicationInsights-Python"
    url      = "https://pypi.io/packages/source/a/applicationinsights/applicationinsights-0.11.9.tar.gz"

    version('0.11.9', sha256='30a11aafacea34f8b160fbdc35254c9029c7e325267874e3c68f6bdbcd6ed2c3')

    depends_on('py-setuptools', type='build')
