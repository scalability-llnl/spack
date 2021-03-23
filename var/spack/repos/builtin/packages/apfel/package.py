# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apfel(AutotoolsPackage):
    """APFEL is a library able to perform DGLAP evolution up to NNLO in QCD and
       to NLO in QED, both with pole and MSbar masses. The coupled DGLAP
       QCD+QED evolution equations are solved in x-space by means of higher
       order interpolations and Runge-Kutta techniques."""

    homepage = "https://github.com/scarrazza/apfel"
    url      = "https://github.com/scarrazza/apfel/archive/3.0.4.tar.gz"

    tags = ['hep']

    version('3.0.4', sha256='c7bfae7fe2dc0185981850f2fe6ae4842749339d064c25bf525b4ef412bbb224')

    depends_on('swig', when='+python')
    depends_on('python', when='+python', type=('build', 'run'))
    depends_on('lhapdf', when='+lhapdf', type=('build', 'run'))

    variant('python', description='Build python wrapper', default=False)
    variant('lhapdf', description='Link to LHAPDF', default=False)

    def configure_args(self):
        args = []
        if self.spec.satisfies('~python'):
            args.append('--disable-pywrap')
        else:
            args.append('--enable-pywrap')

        args += self.enable_or_disable('lhapdf')
        return args
