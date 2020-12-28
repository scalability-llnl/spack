# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Memsurfer(PythonPackage):
    """MemSurfer is a tool to compute and analyze membrane surfaces found in a
       wide variety of large-scale molecular simulations."""

    homepage = "https://github.com/LLNL/MemSurfer"
    git = "https://github.com/LLNL/MemSurfer.git"
    maintainers = ['bhatiaharsh']

    version('1.0',     tag='v1.0',       submodules=True)
    version('master',  branch='master',  submodules=True)
    version('develop', branch='develop', submodules=True)

    variant('osmesa', default=False,
            description='Enable OSMesa support (for VTK)')

    extends('python')
    depends_on('python@3.7:', type=('build', 'run'))

    depends_on('cmake@3.14:', type='build')
    depends_on('swig@3.0.12', type='build')

    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    depends_on('eigen@3.3.7')
    depends_on('cgal@4.13 +shared~core~demos~imageio')

    # vtk needs to know whether to build with mesa or opengl
    vtk_conf = '~ffmpeg~mpi+opengl2~qt~xdmf+python'
    depends_on('vtk@8.1.2 ' + vtk_conf + ' ~osmesa', when='~osmesa')
    depends_on('vtk@8.1.2 ' + vtk_conf + ' +osmesa', when='+osmesa')

    # needed only to resolve the conflict between the default and netcdf's spec
    depends_on('hdf5 +hl')

    # memsurfer's setup needs path to these deps to build extension modules
    def setup_build_environment(self, env):
        env.set('VTK_ROOT', self.spec['vtk'].prefix)
        env.set('CGAL_ROOT', self.spec['cgal'].prefix)
        env.set('BOOST_ROOT', self.spec['boost'].prefix)
        env.set('EIGEN_ROOT', self.spec['eigen'].prefix)
