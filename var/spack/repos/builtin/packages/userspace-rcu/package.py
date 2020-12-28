# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UserspaceRcu(AutotoolsPackage):
    """liburcu is a LGPLv2.1 userspace RCU (read-copy-update) library. This
    data synchronization library provides read-side access which scales
    linearly with the number of cores."""

    homepage = "http://liburcu.org/"
    url      = "https://github.com/urcu/userspace-rcu/archive/v0.11.1.tar.gz"

    version('0.11.1', sha256='a0ed8995edfbeac5f5eb2f152a8f3654040ecfc99a746bfe3da3bccf435b7d5d')
    version('0.11.0', sha256='7834e4692565b491b9d2d258095d6c05089c9bae8a1bef280c338d15ba02e9ac')
    version('0.10.2', sha256='e117c416fced894e24720cc1b38247074a13020f19d6704b38e554cbcb993d06')
    version('0.9.6',  sha256='4d9e4ca40c079e0b0e9f912a9092589b97fbaf80eb6537e9ae70d48c09472efa')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    patch('examples.patch', sha256='49aa8fa99d3a1315c639d2a90014079c34a7d0a6dde110b6cbb7b02f87324742')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap')
