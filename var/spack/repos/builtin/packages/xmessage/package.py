# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmessage(AutotoolsPackage, XorgPackage):
    """xmessage displays a message or query in a window.  The user can click
    on an "okay" button to dismiss it or can select one of several buttons
    to answer a question.  xmessage can also exit after a specified time."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xmessage"
    xorg_mirror_path = "app/xmessage-1.0.4.tar.gz"

    version('1.0.4', sha256='883099c3952c8cace5bd11d3df2e9ca143fc07375997435d5ff4f2d50353acca')

    depends_on('libxaw')
    depends_on('libxt')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
