# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbProto(AutotoolsPackage):
    """xcb-proto provides the XML-XCB protocol descriptions that libxcb uses to
    generate the majority of its code and API."""

    homepage = "http://xcb.freedesktop.org/"
    url      = "https://xorg.freedesktop.org/archive/individual/proto/xcb-proto-1.14.1.tar.xz"

    version('1.14.1', sha256='f04add9a972ac334ea11d9d7eb4fc7f8883835da3e4859c9afa971efdf57fcc3')
    version('1.14', sha256='186a3ceb26f9b4a015f5a44dcc814c93033a5fc39684f36f1ecc79834416a605')
    version('1.13', sha256='0698e8f596e4c0dbad71d3dc754d95eb0edbb42df5464e0f782621216fa33ba7')
    version('1.12', sha256='cfa49e65dd390233d560ce4476575e4b76e505a0e0bacdfb5ba6f8d0af53fd59')
    version('1.11', sha256='d12152193bd71aabbdbb97b029717ae6d5d0477ab239614e3d6193cc0385d906')

    # TODO: uncomment once build deps can be resolved separately
    # See #7646, #4145, #4063, and #2548 for details
    # extends('python')

    patch('xcb-proto-1.12-schema-1.patch', when='@1.12')

    def url_for_version(self, version):
        if version >= Version('1.14'):
            url = 'https://xorg.freedesktop.org/archive/individual/proto/xcb-proto-{0}.tar.xz'
        else:
            url = 'http://xcb.freedesktop.org/dist/xcb-proto-{0}.tar.gz'

        return url.format(version)
