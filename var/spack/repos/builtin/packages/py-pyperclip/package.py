# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyperclip(PythonPackage):
    """A cross-platform clipboard module for Python."""

    homepage = "https://github.com/asweigart/pyperclip"
    url      = "https://pypi.io/packages/source/p/pyperclip/pyperclip-1.7.0.tar.gz"

    version('1.7.0', sha256='979325468ccf682104d5dcaf753f869868100631301d3e72f47babdea5700d1c')

    depends_on('py-setuptools', type='build')
