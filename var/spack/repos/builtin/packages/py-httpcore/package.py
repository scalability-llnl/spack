# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpcore(PythonPackage):
    """The HTTP Core package provides a minimal low-level HTTP client,
    which does one thing only. Sending HTTP requests."""

    homepage = "https://github.com/encode/httpcore"
    url      = "https://pypi.io/packages/source/h/httpcore/httpcore-0.11.0.tar.gz"

    version('0.11.0', sha256='35ffc735d746b83f8fc6d36f82600e56117b9e8adc65d0c0423264b6ebfef7bf')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-sniffio@1.0:')
    depends_on('py-h11@0.8:0.9')
