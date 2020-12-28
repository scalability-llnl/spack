# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnfnetlink(AutotoolsPackage):
    """libnfnetlink is a userspace library that provides some low-level
    nfnetlink handling functions.  It is used as a foundation for other,
    netfilter subsystem specific libraries such as libnfnetlink_conntrack,
    libnfnetlink_log and libnfnetlink_queue."""

    homepage = "http://netfilter.org"
    url      = "https://github.com/Distrotech/libnfnetlink/archive/libnfnetlink-1.0.1.tar.gz"

    version('1.0.1',  sha256='11dd8a1045b03d47c878535eeb6b9eb34db295d21903a4dfd2c2cc63f45e675b')
    version('1.0.0',  sha256='1d43456e51d5ff2e8bc84b68d8acad3bb15603cfaa806ba9693eea4f2aa1abeb')
    version('0.0.41', sha256='84381ad3aec4fc4884c020c7774a241160d92ed50c9f93a2660db94e212cbb72')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
