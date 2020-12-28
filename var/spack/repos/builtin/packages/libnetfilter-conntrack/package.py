# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibnetfilterConntrack(AutotoolsPackage):
    """libnetfilter_conntrack is a userspace library providing a programming
    interface (API) to the in-kernel connection tracking state table."""

    homepage = "http://netfilter.org"
    url      = "https://github.com/Distrotech/libnetfilter_conntrack/archive/libnetfilter_conntrack-1.0.4.tar.gz"

    version('1.0.4', sha256='68168697b9d6430b7797ddd579e13a2cef06ea15c154dfd14e18be64e035ea6e')
    version('1.0.3', sha256='e2129d7c0346c7140355d643da8e3409cbd755689ea889bc0d6dbd557f1b5671')
    version('1.0.2', sha256='97f641a2e47053bd87bc817292519d6661e8f84a22d3314724b83b9f5eaddbff')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')
    depends_on('libmnl@1.0.3:')
    depends_on('libnfnetlink@1.0.0:')
