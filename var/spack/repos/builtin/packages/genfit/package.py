# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Genfit(CMakePackage):
    """GenFit is an experiment-independent framework for track reconstruction in
        particle and nuclear physics"""

    homepage = "https://github.com/GenFit/GenFit"
    url      = "https://github.com/GenFit/GenFit/archive/02-00-00.tar.gz"
    git      = "https://github.com/GenFit/GenFit.git"

    maintainers = ['mirguest']

    tags = ["hep"]

    version('master', branch='master')
    version('02-00-00', sha256='0bfd5dd152ad0573daa4153a731945824e0ce266f844988b6a8bebafb7f2dacc')
    # Untagged version from 2017-06-23 known to work with root@6.16.00
    version('b496504a', sha256='e1582b35782118ade08498adc03f3fda01979ff8bed61e0520edae46d7bfe477')

    depends_on('root')
    depends_on('root@:6.16.00', when='@b496504a')
    depends_on('eigen')

    def cmake_args(self):
        args = []
        # normally, as a cmake package root should be
        # automatically picked up after 'depends_on'
        # as it is added to CMAKE_PREFIX_PATH
        # but genfit cooks its own root cmake config
        # so this workaround is needed for now.
        root_prefix = self.spec["root"].prefix
        args.append('-DROOT_DIR=%s' % root_prefix)

        return args
