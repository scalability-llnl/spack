# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sensei(CMakePackage):
    """SENSEI is a platform for scalable in-situ analysis and visualization.
    Its design motto is 'Write once, run everywhere', this means that once
    the application is instrumented with SENSEI it can use existing and
    future analysis backends. Existing backends include: Paraview/Catalyst,
    Visit/Libsim, ADIOS, Python scripts, and so on."""

    homepage = "https://sensei-insitu.org"
    url      = "https://gitlab.kitware.com/sensei/sensei/-/archive/v3.1.0/sensei-v3.1.0.tar.gz"
    git      = "https://gitlab.kitware.com/sensei/sensei.git"
    maintainers = ['sshudler']

    version('develop', branch='develop')
    version('3.2.1', sha256='8cde9ac5313e6c03fd793d24a6f285b60cca14cacfc83931f11d878163ee9d5b')
    version('3.2.0', sha256='fe4fe294c17e469bfd1824130648a7d25b1fa771904b5c5edc37b820d090e224')
    version('3.1.0', sha256='9a3e6d0d5bb6170ee666586435434da1708b3876fd448b9d41142571ed9da939')
    version('3.0.0', sha256='0aabbea03ade9947c88fc0aa6d3cbaf3c8267e8504e384a041445678a95e58eb')
    version('2.1.1', sha256='8a27ebf133fef00a59e4b29433762e6560bf20214072de7808836eb668bb5687')
    version('2.1.0', sha256='b7af21a25523cf6cd8934d797471b75ca32881166625d71f24b5c8b6d727ca99')
    version('2.0.0', sha256='df48eab035e1acdd8edf5159955c05306f9ca48117effacc4a6b77c3fb24f62b')
    version('1.1.0', sha256='e5a4ba691573ff6c7b0d4793665e218ee5868ebcc0198915d1f16a4b7b92a368')
    version('1.0.0', sha256='bdcb03c56b51f2795ec5a7e85a5abb01d473d192fac50f2a8bf2608cc3564ff8')

    variant('shared', default=True, description='Enables shared libraries')
    variant('sencore', default=True, description='Enables the SENSEI core library')
    variant('ascent', default=False, description='Build with ParaView-Catalyst support')
    variant('catalyst', default=False, description='Build with ParaView-Catalyst support')
    variant('libsim', default=False, description='Build with VisIt-Libsim support')
    variant('vtkio', default=False, description='Enable adaptors to write to VTK XML format')
    variant('adios2', default=False, description='Enable ADIOS2 adaptors and endpoints')
    variant('hdf5', default=False, description='Enables HDF5 adaptors and endpoints')
    variant('vtkm', default=False, description='Enable VTKm adaptors and endpoints')
    variant('python', default=False, description='Enable Python bindings')
    variant('miniapps', default=True, description='Enable the parallel 3D and oscillators miniapps')
    variant('cxxstd', default='11', values=('11', '14', '17'), multi=False, description='Use the specified C++ standard when building.')

    # All SENSEI versions up to 2.1.1 support only Python 2, so in this case
    # Paraview 6 cannot be used since it requires Python 3. Starting from
    # version 3, SENSEI supports Python 3.
    depends_on("paraview@5.5.0:5.5.2+mpi+hdf5", when="@:2.1.1 +catalyst")
    depends_on("paraview@5.5.0:5.5.2+python+mpi+hdf5", when="@:2.1.1 +catalyst+python")
    depends_on("paraview@5.6:5.7+mpi+hdf5", when="@3:3.2.1 +catalyst")
    depends_on("paraview@5.6:5.7+python3+mpi+hdf5", when="@3:3.2.1 +catalyst+python")
    depends_on("paraview+mpi+hdf5", when="+catalyst")
    depends_on("paraview+python3+mpi+hdf5", when="+catalyst+python")
    depends_on("visit~gui~python", when="+libsim")
    depends_on("vtk@8.1.0:8.1.2", when="+libsim")
    depends_on("vtk", when="~libsim ~catalyst")
    depends_on("vtk+python", when="~libsim ~catalyst+python")
    depends_on("adios2", when="+adios2")
    depends_on("ascent", when="+ascent")

    # VTK needs +hl and currently spack cannot resolve +hl and ~hl
    depends_on("hdf5+hl", when="+hdf5")
    # SENSEI 3 supports Python 3, earlier versions upport only Python 2
    depends_on("python@:2.7.16", when="@:2.1.1 +python", type=('build', 'run'))
    depends_on("python@3:", when="@3: +python", type=('build', 'run'))
    extends('python', when='+python')
    depends_on("py-numpy", when="+python", type=('build', 'run'))
    depends_on("py-mpi4py", when="+python", type=('build', 'run'))
    depends_on("swig", when="+python", type='build')
    depends_on('cmake@3.6:', when="@3:", type='build')
    depends_on('pugixml')

    # Since sensei always has a VTK dependency, either directly or indirectly,
    # VTKm will also always be available via VTK so there's no scenario to
    # have a directl dependency on VTK,

    # Can have either LibSim or Catalyst, but not both
    conflicts('+libsim', when='+catalyst')
    # hdf5 variant is available only for SENSEI 3
    conflicts('+hdf5', when='@:2.1.1')

    def cmake_args(self):
        spec = self.spec

        # -Ox flags are set by default in CMake based on the build type
        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            self.define('CMAKE_C_STANDARD', 11),
            self.define('SENSEI_USE_EXTERNAL_pugixml', True),
            self.define('CMAKE_POSITION_INDEPENDENT_CODE', True),
            self.define_from_variant('ENABLE_SENSEI', 'sencore'),
            self.define_from_variant('ENABLE_ASCENT', 'ascent'),
            self.define_from_variant('ENABLE_VTKM', 'vtkm'),
            self.define_from_variant('ENABLE_CATALYST', 'catalyst'),
            self.define_from_variant('ENABLE_LIBSIM', 'libsim'),
            self.define_from_variant('ENABLE_VTK_IO', 'vtkio'),
            self.define_from_variant('ENABLE_PYTHON', 'python'),
            self.define_from_variant('ENABLE_ADIOS2', 'adios2'),
            self.define_from_variant('ENABLE_HDF5', 'hdf5'),
            self.define_from_variant('ENABLE_PARALLEL3D', 'miniapps'),
            self.define_from_variant('ENABLE_OSCILLATORS', 'miniapps')
        ]

        if '+libsim' in spec:
            args.append(
                '-DVISIT_DIR:PATH={0}/current/{1}-{2}'.format(
                    spec['visit'].prefix, spec.platform, spec.target.family)
            )

        if '+python' in spec:
            args.append(self.define('PYTHON_EXECUTABLE', spec['python'].command.path))
            if spec.satisfies('@3:'):
                args.append(self.define('SENSEI_PYTHON_VERSION', 3))
            args.append(self.define_from_variant('ENABLE_CATALYST_PYTHON', 'catalyst'))

        return args
