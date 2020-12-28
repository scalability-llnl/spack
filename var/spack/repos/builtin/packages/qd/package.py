# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qd(AutotoolsPackage):
    """C++/Fortran-90 double-double and quad-double package.
       With modifications for easier integration with NJet.
       see http://crd-legacy.lbl.gov/~dhbailey/mpdist/ for authors page"""

    homepage = "https://bitbucket.org/njet/qd-library/src/master/"
    git      = "https://bitbucket.org/njet/qd-library.git"

    tags = ['hep']

    version('2.3.13', commit='a57dde9')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def setup_build_environment(self, env):
        if self.spec.satisfies('%nvhpc'):
            env.append_flags('FCFLAGS', "-fPIC")

    def configure_args(self):
        args = ['--enable-shared']
        return args
