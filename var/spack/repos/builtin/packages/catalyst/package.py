# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import subprocess
import sys
import llnl.util.tty as tty


class Catalyst(CMakePackage):
    """Catalyst is an in situ use case library, with an adaptable application
    programming interface (API), that orchestrates the alliance between
    simulation and analysis and/or visualization tasks."""

    homepage = 'http://www.paraview.org'
    url      = "http://www.paraview.org/files/v5.5/ParaView-v5.5.2.tar.gz"
    _urlfmt_gz = 'http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.gz'
    _urlfmt_xz = 'http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.xz'

    maintainers = ['chuckatkins', 'danlipsa']

    version('5.6.0', sha256='5b49cb96ab78eee0427e25200530ac892f9a3da7725109ce1790f8010cb5b377')
    version('5.5.2', sha256='64561f34c4402b88f3cb20a956842394dde5838efd7ebb301157a837114a0e2d')
    version('5.5.1', sha256='a6e67a95a7a5711a2b5f95f38ccbff4912262b3e1b1af7d6b9afe8185aa85c0d')
    version('5.5.0', sha256='1b619e326ff574de808732ca9a7447e4cd14e94ae6568f55b6581896cd569dff')
    version('5.4.1', sha256='390d0f5dc66bf432e202a39b1f34193af4bf8aad2355338fa5e2778ea07a80e4')
    version('5.4.0', sha256='f488d84a53b1286d2ee1967e386626c8ad05a6fe4e6cbdaa8d5e042f519f94a9')
    version('5.3.0', sha256='046631bbf00775edc927314a3db207509666c9c6aadc7079e5159440fd2f88a0')
    version('5.2.0', sha256='894e42ef8475bb49e4e7e64f4ee2c37c714facd18bfbb1d6de7f69676b062c96')
    version('5.1.2', sha256='ff02b7307a256b7c6e8ad900dee5796297494df7f9a0804fe801eb2f66e6a187')
    version('5.0.1', sha256='caddec83ec284162a2cbc46877b0e5a9d2cca59fb4ab0ea35b0948d2492950bb')
    version('4.4.0', sha256='c2dc334a89df24ce5233b81b74740fc9f10bc181cd604109fd13f6ad2381fc73')

    variant('python', default=False, description='Enable Python support')
    variant('python3', default=False, description='Enable Python3 support')
    variant('essentials', default=False, description='Enable Essentials support')
    variant('extras', default=False, description='Enable Extras support. Implies Essentials.')
    variant('rendering', default=True, description='Enable Rendering support. Implies Extras and Essentials.')
    variant('osmesa', default=True, description='Use offscreen rendering')
    conflicts('+osmesa', when='~rendering')

    conflicts('+python', when='+python3')
    conflicts('+python', when='@5.6:')
    conflicts('+python3', when='@:5.5')

    # Workaround for
    # adding the following to your packages.yaml
    # packages:
    #   python:
    #     version: [3, 2]
    # without this you'll get:
    # paraview requires python version 3:, but spec asked for 2.7.16
    # for `spack spec paraview+python`
    # see spack pull request #11539
    # extends('python', when='+python')
    extends('python', when='+python')
    extends('python', when='+python3')

    depends_on('git', type='build')
    depends_on('mpi')
    depends_on('python@2.7:2.8', when='+python', type=('build', 'link', 'run'))
    depends_on('python@3:', when='+python3', type=('build', 'link', 'run'))

    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python3', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python+mpi', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python3+mpi', type=('build', 'run'))

    depends_on('gl@3.2:', when='+rendering')
    depends_on('osmesa', when='+rendering+osmesa')
    depends_on('glx', when='+rendering~osmesa')
    depends_on('cmake@3.3:', type='build')

    @when('@5.5.0:5.5.2')
    def patch(self):
        """Apply the patch (it should be fixed in Paraview 5.6)
        at the package dir to the source code in
        root_cmakelists_dir."""
        patch_name = 'vtkm-catalyst-pv551.patch'
        patch = which("patch", required=True)
        with working_dir(self.root_cmakelists_dir):
            patch('-s', '-p', '1', '-i',
                  join_path(self.package_dir, patch_name),
                  "-d", '.')

    def url_for_version(self, version):
        """Handle ParaView version-based custom URLs."""
        if version < Version('5.1.0'):
            return self._urlfmt_gz.format(version.up_to(2), version, '-source')
        elif version < Version('5.6.0'):
            return self._urlfmt_gz.format(version.up_to(2), version, '')
        else:
            return self._urlfmt_xz.format(version.up_to(2), version, '')

    @property
    def paraview_subdir(self):
        """The paraview subdirectory name as paraview-major.minor"""
        return 'paraview-{0}'.format(self.spec.version.up_to(2))

    @property
    def editions(self):
        """Transcribe spack variants into names of Catalyst Editions"""
        selected = ['Base']  # Always required

        if '+python' in self.spec or '+python3' in self.spec:
            selected.append('Enable-Python')

        if '+essentials' in self.spec:
            selected.append('Essentials')

        if '+extras' in self.spec:
            selected.append('Essentials')
            selected.append('Extras')

        if '+rendering' in self.spec:
            selected.append('Essentials')
            selected.append('Extras')
            selected.append('Rendering-Base')

        return selected

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball.
        Then, generate the catalyst source files."""
        super(Catalyst, self).do_stage(mirror_only)

        # extract the catalyst part
        catalyst_script = os.path.join(self.stage.source_path, 'Catalyst',
                                       'catalyze.py')
        editions_dir = os.path.join(self.stage.source_path, 'Catalyst',
                                    'Editions')
        catalyst_source_dir = os.path.abspath(self.root_cmakelists_dir)

        python_path = (os.path.realpath(
            spec['python3'].command.path if '+python3' in self.spec else
            spec['python'].command.path if '+python' in self.spec else
            sys.executable))

        command = [python_path, catalyst_script,
                   '-r', self.stage.source_path,
                   '-o', catalyst_source_dir]

        for edition in self.editions:
            command.extend(['-i', os.path.join(editions_dir, edition)])

        if not os.path.isdir(catalyst_source_dir):
            os.mkdir(catalyst_source_dir)
            subprocess.check_call(command)
            tty.msg("Generated catalyst source in %s" % self.stage.source_path)
        else:
            tty.msg("Already generated %s in %s" % (self.name,
                                                    self.stage.source_path))

    def setup_run_environment(self, env):
        # paraview 5.5 and later
        # - cmake under lib/cmake/paraview-5.5
        # - libs  under lib
        # - python bits under lib/python2.8/site-packages
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        if self.spec.version <= Version('5.4.1'):
            lib_dir = join_path(lib_dir, paraview_subdir)
        env.set('ParaView_DIR', self.prefix)
        env.prepend_path('LIBRARY_PATH', lib_dir)
        env.prepend_path('LD_LIBRARY_PATH', lib_dir)

        if '+python' in self.spec or '+python3' in self.spec:
            python_version = self.spec['python'].version.up_to(2)
            env.prepend_path('PYTHONPATH', join_path(lib_dir,
                             'python{0}'.format(python_version),
                             'site-packages'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('ParaView_DIR', self.prefix)

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return os.path.join(self.stage.source_path,
                            'Catalyst-v' + str(self.version))

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return join_path(os.path.abspath(self.root_cmakelists_dir),
                         'spack-build')

    def cmake_args(self):
        """Populate cmake arguments for Catalyst."""
        spec = self.spec

        def variant_bool(feature, on='ON', off='OFF'):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        def nvariant_bool(feature):
            """Negated ternary for spec variant to OFF/ON string"""
            return variant_bool(feature, on='OFF', off='ON')

        cmake_args = [
            '-DPARAVIEW_GIT_DESCRIBE=v%s' % str(self.version),
            '-DVTK_USE_SYSTEM_EXPAT:BOOL=ON',
            '-DVTK_USE_X:BOOL=%s' % nvariant_bool('+osmesa'),
            '-DVTK_USE_OFFSCREEN:BOOL=%s' % variant_bool('+osmesa'),
            '-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' % variant_bool('+osmesa'),
        ]
        if '+python' in spec or '+python3' in spec:
            cmake_args.extend([
                '-DPARAVIEW_ENABLE_PYTHON:BOOL=ON',
                '-DPYTHON_EXECUTABLE:FILEPATH=%s' %
                spec['python'].command.path,
                '-DVTK_USE_SYSTEM_MPI4PY:BOOL=%s' % variant_bool('+mpi')
            ])
        else:
            cmake_args.append('-DPARAVIEW_ENABLE_PYTHON:BOOL=OFF')

        if spec.platform == 'linux' and spec.target == 'aarch64':
            cmake_args.append('-DCMAKE_CXX_FLAGS=-DPNG_ARM_NEON_OPT=0')
            cmake_args.append('-DCMAKE_C_FLAGS=-DPNG_ARM_NEON_OPT=0')

        return cmake_args

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory through the cmake.sh script"""
        cmake_script_path = os.path.join(
            os.path.abspath(self.root_cmakelists_dir),
            'cmake.sh')
        with working_dir(self.build_directory, create=True):
            subprocess.check_call([cmake_script_path,
                                   os.path.abspath(self.root_cmakelists_dir)] +
                                  self.cmake_args() + self.std_cmake_args)
