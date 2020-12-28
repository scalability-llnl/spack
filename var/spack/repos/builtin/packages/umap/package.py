# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Umap(CMakePackage):
    """Umap is a library that provides an mmap()-like interface to a
    simple, user-space page fault handler based on the userfaultfd Linux
    feature (starting with 4.3 linux kernel)."""

    homepage = "https://github.com/LLNL/umap"
    url      = "https://github.com/LLNL/umap/archive/v2.1.0.tar.gz"
    git      = "https://github.com/LLNL/umap.git"

    version('develop', branch='develop')
    version('2.1.0', sha256='dfdc5b717aecdbfbb0da22e8567b9f2ffbc3607000a31122bf7c5ab3b85cecd9')
    version('2.0.0', sha256='85c4bc68e8790393847a84eb54eaf6fc321acade382a399a2679d541b0e34150')
    version('1.0.0', sha256='c746de3fae5bfc5bbf36234d5e888ea45eeba374c26cd8b5a817d0c08e454ed5')
    version('0.0.4', sha256='bffaa03668c95b608406269cba6543f5e0ba37b04ac08a3fc4593976996bc273')
    version('0.0.3', sha256='8e80835a85ad69fcd95f963822b1616c782114077d79c350017db4d82871455c')
    version('0.0.2', sha256='eccc987b414bc568bd33b569ab6e18c328409499f11e65ac5cd5c3e1a8b47509')
    version('0.0.1', sha256='49020adf55aa3f8f03757373b21ff229d2e8cf4155d54835019cd4745c1291ef')

    variant('logging', default=False, description='Build with logging enabled.')
    variant('tests', default=False, description='Build test programs.')

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DENABLE_LOGGING=%s" % ('On' if '+logging' in spec else 'Off'),
            "-DENABLE_TESTS=%s"   % ('On' if '+tests' in spec else 'Off'),
        ]
        return args
