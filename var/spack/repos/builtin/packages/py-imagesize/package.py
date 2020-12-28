# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImagesize(PythonPackage):
    """Parses image file headers and returns image size. Supports PNG, JPEG,
    JPEG2000, and GIF image file formats."""

    homepage = "https://github.com/shibukawa/imagesize_py"
    url      = "https://pypi.io/packages/source/i/imagesize/imagesize-0.7.1.tar.gz"

    version('1.1.0',  sha256='f3832918bc3c66617f92e35f5d70729187676313caa60c187eb0f28b8fe5e3b5')
    version('0.7.1', sha256='0ab2c62b87987e3252f89d30b7cedbec12a01af9274af9ffa48108f2c13c6062')

    depends_on('py-setuptools', type='build')
