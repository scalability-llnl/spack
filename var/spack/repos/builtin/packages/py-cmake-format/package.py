# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCmakeFormat(PythonPackage):
    """cmake-format project provides Quality Assurance (QA) tools for
    cmake. Tools include cmake-annotate, cmake-format, cmake-lint,
    and ctest-to."""

    homepage = "https://pypi.python.org/pypi/cmake-format"
    url      = "https://pypi.io/packages/source/c/cmake_format/cmake_format-0.6.9.tar.gz"

    version('0.6.10', sha256='82f0ef16236225cb43f45bfb6983ef7f6f72634727a1a6c26290402527bdd793')
    version('0.6.9', sha256='b2f8bf2e9c6651126f2f2954b7803222b0faf6b8649eabc4d965ea97483a4d20')

    depends_on('py-setuptools',  type=('build', 'run'))
    depends_on('py-six@1.13.0:', type=('build', 'run'))
