##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Vtk(CMakePackage):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """

    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/7.1/VTK-7.1.0.tar.gz"
    list_url = "http://www.vtk.org/download/"

    version('7.1.0', 'a7e814c1db503d896af72458c2d0228f')
    version('7.0.0', '5fe35312db5fb2341139b8e4955c367d')
    version('6.3.0', '0231ca4840408e9dd60af48b314c5b6d')
    version('6.1.0', '25e4dfb3bad778722dcaec80cd5dab7d')

    # VTK7 defaults to OpenGL2 rendering backend
    variant('opengl2', default=True, description='Build with OpenGL2 instead of OpenGL as rendering backend')
    variant('python', default=False, description='Build the python modules')

    patch('gcc.patch', when='@6.1.0')

    depends_on('qt')
    depends_on('hdf5')
    depends_on('netcdf')
    depends_on('netcdf-cxx')

    extends('python', when='+python')

    def url_for_version(self, version):
        url = "http://www.vtk.org/files/release/{0}/VTK-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def cmake_args(self):
        spec = self.spec

        opengl_ver = 'OpenGL{0}'.format('2' if '+opengl2' in spec else '')
        qt_ver = spec['qt'].version.up_to(1)
        qt_bin = spec['qt'].prefix.bin

        cmake_args = [
            '-DBUILD_SHARED_LIBS=ON',
            '-DVTK_RENDERING_BACKEND:STRING={0}'.format(opengl_ver),
            '-DVTK_USE_SYSTEM_HDF5=ON',
            '-DVTK_USE_SYSTEM_NETCDF=ON',
            '-DNETCDF_DIR={0}'.format(spec['netcdf'].prefix),
            '-DNETCDF_C_ROOT={0}'.format(spec['netcdf'].prefix),
            '-DNETCDF_CXX_ROOT={0}'.format(spec['netcdf-cxx'].prefix),

            # Enable/Disable wrappers for Python.
            '-DVTK_WRAP_PYTHON={0}'.format(
                'ON' if '+python' in spec else 'OFF'),

            # Disable wrappers for other languages.
            '-DVTK_WRAP_JAVA=OFF',
            '-DVTK_WRAP_TCL=OFF',

            # Enable Qt support here.
            '-DVTK_QT_VERSION:STRING={0}'.format(qt_ver),
            '-DQT_QMAKE_EXECUTABLE:PATH={0}/qmake'.format(qt_bin),
            '-DVTK_Group_Qt:BOOL=ON',
        ]

        # NOTE: The following definitions are required in order to allow
        # VTK to build with qt~webkit versions (see the documentation for
        # more info: http://www.vtk.org/Wiki/VTK/Tutorials/QtSetup).
        if '~webkit' in spec['qt']:
            cmake_args.extend([
                '-DVTK_Group_Qt:BOOL=OFF',
                '-DModule_vtkGUISupportQt:BOOL=ON',
                '-DModule_vtkGUISupportQtOpenGL:BOOL=ON',
            ])

        if spec.satisfies('@:6.1.0'):
            cmake_args.extend([
                '-DCMAKE_C_FLAGS=-DGLX_GLXEXT_LEGACY',
                '-DCMAKE_CXX_FLAGS=-DGLX_GLXEXT_LEGACY'
            ])

            # VTK 6.1.0 (and possibly earlier) does not use
            # NETCDF_CXX_ROOT to detect NetCDF C++ bindings, so
            # NETCDF_CXX_INCLUDE_DIR and NETCDF_CXX_LIBRARY must be
            # used instead to detect these bindings
            netcdf_cxx_lib = spec['netcdf-cxx'].libs.joined()
            cmake_args.extend([
                '-DNETCDF_CXX_INCLUDE_DIR={0}'.format(
                    spec['netcdf-cxx'].prefix.include),
                '-DNETCDF_CXX_LIBRARY={0}'.format(netcdf_cxx_lib),
            ])

            # Garbage collection is unsupported in Xcode starting with
            # version 5.1; if the Apple clang version of the compiler
            # is 5.1.0 or later, unset the required Objective-C flags
            # to remove the garbage collection flags.  Versions of VTK
            # after 6.1.0 set VTK_REQUIRED_OBJCXX_FLAGS to the empty
            # string. This fix was recommended on the VTK mailing list
            # in March 2014 (see
            # https://public.kitware.com/pipermail/vtkusers/2014-March/083368.html)
            if (self.compiler.is_apple and
                self.compiler.version >= Version('5.1.0')):
                cmake_args.extend(['-DVTK_REQUIRED_OBJCXX_FLAGS=""'])

        return cmake_args
