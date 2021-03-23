# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mcutils(MakefilePackage):
    """A collection of routines for classification and manipulation of
       particle physics simulated HepMC event records."""

    homepage = "https://gitlab.com/hepcedar/mcutils"
    git      = "https://gitlab.com/hepcedar/mcutils.git"

    tags = ['hep']

    version('1.3.5', tag='mcutils-1.3.5')
    version('1.3.4', tag='mcutils-1.3.4')
    version('1.3.3', tag='mcutils-1.3.3')
    version('1.3.2', tag='mcutils-1.3.2')
    version('1.3.1', tag='mcutils-1.3.1')
    version('1.3.1', tag='mcutils-1.3.0')
    version('1.2.1', tag='mcutils-1.2.1')
    version('1.2.0', tag='mcutils-1.2.0')
    version('1.1.2', tag='mcutils-1.1.2')
    version('1.1.1', tag='mcutils-1.1.1')
    version('1.1.0', tag='mcutils-1.1.0')
    version('1.0.3', tag='mcutils-1.0.3')
    version('1.0.2', tag='mcutils-1.0.2')
    version('1.0.1', tag='mcutils-1.0.1')
    version('1.0.0', tag='mcutils-1.0.0')

    depends_on('heputils', when='@1.1.0:')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
