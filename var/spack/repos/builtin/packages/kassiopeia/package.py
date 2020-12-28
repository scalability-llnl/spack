# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kassiopeia(CMakePackage):
    """Simulation of electric and magnetic fields and particle tracking."""

    homepage = "https://katrin-experiment.github.io/Kassiopeia/"
    url      = "https://github.com/KATRIN-Experiment/Kassiopeia/archive/v3.6.1.tar.gz"
    git      = "https://github.com/KATRIN-Experiment/Kassiopeia.git"

    tags = ['hep']

    maintainers = ['wdconinc']

    version('3.7.5', sha256='8f28d08c7ef51e64221e0a4705f3cee3a5d738b8cdde5ce9fa58a3a0dd14ae05')
    version('3.7.4', sha256='c1514163a084530930be10dbe487fb1950ccbc9662a4a190bdecffbd84a71fd4')
    version('3.7.3', sha256='a8753585b9fa0903e1f5f821c4ced3cddd72792ad7e6075a7e25318f81ad9eaa')
    version('3.7.2', sha256='bdfdf8c26fa5ad19e8b9c6eb600dfbd3c8218cd695ce067f10633b63bd192f92')
    version('3.7.1', sha256='b22ae2fe5c2271bdf6aaf65d9ecf57ff0d6a88d28ad26d176e1129f0e58faea4')
    version('3.7.0', sha256='32a3e98c77d1b97fe9862cf1d8c6ba8e6c82fb9295a6a217c7ce77cbec751046')
    version('3.6.1', sha256='30193d5384ad81b8570fdcd1bb35b15cc365ab84712819ac0d989c6f5cf6f790')
    version('3.5.0', sha256='b704d77bd182b2806dc8323f642d3197ce21dba3d456430f594b19a7596bda22')
    version('3.4.0', sha256='4e2bca61011e670186d49048aea080a06c3c95dacf4b79e7549c36960b4557f4')

    variant("root", default=False,
            description="Include support for writing ROOT files")
    variant("vtk", default=False,
            description="Include visualization support through VTK")
    variant("mpi", default=False,
            description="Include MPI support for field calculations")
    variant("tbb", default=False,
            description="Include Intel TBB support for field calculations")
    variant("opencl", default=False,
            description="Include OpenCL support for field calculations")

    depends_on('cmake@3.13:', type='build')
    depends_on('zlib')
    depends_on('root@6.0.0:', when='+root')
    depends_on('vtk@6.1:', when='+vtk')
    depends_on('mpi', when='+mpi')
    depends_on('tbb', when='+tbb')
    depends_on('opencl', when='+opencl')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+vtk'):
            args.append('-DKASPER_USE_VTK=ON')
        else:
            args.append('-DKASPER_USE_VTK=OFF')
        if self.spec.satisfies('+tbb'):
            args.append('-DKASPER_USE_TBB=ON')
        else:
            args.append('-DKASPER_USE_TBB=OFF')
        if self.spec.satisfies('+mpi'):
            args.append('-DKEMField_USE_MPI=ON')
        else:
            args.append('-DKEMField_USE_MPI=OFF')
        if self.spec.satisfies('+opencl'):
            args.append('-DKEMField_USE_OPENCL=ON')
        else:
            args.append('-DKEMField_USE_OPENCL=OFF')
        return args
