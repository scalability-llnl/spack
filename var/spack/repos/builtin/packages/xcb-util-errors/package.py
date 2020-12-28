# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilErrors(AutotoolsPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-errors-1.0.tar.gz"

    version('1.0', sha256='7752a722e580efdbada30632cb23aed35c18757399ac3b547b59fd7257cf5e33')

    depends_on('libxcb@1.4:')

    depends_on('xcb-proto', type='build')
    depends_on('pkgconfig', type='build')
