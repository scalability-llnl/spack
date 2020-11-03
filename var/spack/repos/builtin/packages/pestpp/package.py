# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pestpp(CMakePackage):
    """PEST++ is a software suite aimed at supporting complex numerical
    models in the decision-support context. Much focus has been devoted to
    supporting environmental models (groundwater, surface water, etc) but
    these tools are readily applicable to any computer model.
    """

    homepage = "https://pesthomepage.org"
    url      = "https://github.com/usgs/pestpp/archive/5.0.5.tar.gz"

    version('5.0.5', sha256='b9695724758f69c1199371608b01419973bd1475b1788039a2fab6313f6ed67c')

    variant('mpi', default=True, description='Enable MPI support')

    depends_on('cmake@3.9:', type='build')
    depends_on('mpi', type=('build', 'run'), when='+mpi')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
