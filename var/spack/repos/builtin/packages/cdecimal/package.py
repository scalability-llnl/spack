# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cdecimal(AutotoolsPackage):
    """cdecimal is a fast drop-in replacement for the decimal module in
    Python's standard library."""

    homepage = "https://www.bytereef.org/mpdecimal/"
    url      = "https://www.bytereef.org/software/mpdecimal/releases/cdecimal-2.3.tar.gz"

    version('2.3', sha256='d737cbe43ed1f6ad9874fb86c3db1e9bbe20c0c750868fde5be3f379ade83d8b')

    patch('darwin_install_name.patch', when='platform=darwin')
