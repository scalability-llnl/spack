# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnftnl(AutotoolsPackage):
    """A library for low-level interaction with nftables Netlink's API
    over libmnl."""

    homepage = "https://git.netfilter.org/libnftnl/"
    url      = "http://ftp.netfilter.org/pub/libnftnl/libnftnl-1.1.5.tar.bz2"

    version('1.1.6', sha256='c1eb5a696fc1d4b3b412770586017bc01af93da3ddd25233d34a62979dee1eca')
    version('1.1.5', sha256='66de4d05227c0a1a731c369b193010d18a05b1185c2735211e0ecf658eeb14f3')
    version('1.1.4', sha256='c8c7988347adf261efac5bba59f8e5f995ffb65f247a88cc144e69620573ed20')

    depends_on('pkgconfig', type='build')
    depends_on('libmnl@1.0.3:')
