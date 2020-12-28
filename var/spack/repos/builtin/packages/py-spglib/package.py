# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpglib(PythonPackage):
    """Python bindings for C library for finding and handling
    crystal symmetries."""

    homepage = "http://atztogo.github.io/spglib/"
    url      = "https://pypi.io/packages/source/s/spglib/spglib-1.9.9.18.tar.gz"

    version('1.9.9.18', sha256='cbbb8383320b500dc6100b83d5e914a26a97ef8fc97c82d8921b10220e4126cd')

    # Most Python packages only require setuptools as a build dependency.
    # However, spglib requires setuptools during runtime as well.
    depends_on('py-setuptools@18.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
