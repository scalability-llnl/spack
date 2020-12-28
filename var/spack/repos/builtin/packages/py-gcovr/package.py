# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGcovr(PythonPackage):
    """Gcovr provides a utility for managing the use of the GNU gcov utility
    and generating summarized code coverage results. This command is inspired
    by the Python coverage.py package, which provides a similar utility for
    Python."""

    homepage = "https://gcovr.com/"
    url      = "https://pypi.io/packages/source/g/gcovr/gcovr-4.2.tar.gz"

    version('4.2', sha256='5aae34dc81e51600cfecbbbce3c3a80ce3f7548bc0aa1faa4b74ecd18f6fca3f')

    depends_on('python@2.7:,3.5:', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
