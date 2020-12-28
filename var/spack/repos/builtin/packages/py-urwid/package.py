# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrwid(PythonPackage):
    """A full-featured console UI library"""
    homepage = "http://urwid.org/"
    url      = "https://pypi.io/packages/source/u/urwid/urwid-1.3.0.tar.gz"

    version('1.3.0', sha256='29f04fad3bf0a79c5491f7ebec2d50fa086e9d16359896c9204c6a92bc07aba2')

    depends_on('py-setuptools', type='build')
