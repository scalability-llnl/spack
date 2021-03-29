# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os


class Hdf(AutotoolsPackage):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://portal.hdfgroup.org"
    url      = "https://support.hdfgroup.org/ftp/HDF/releases/HDF4.2.14/src/hdf-4.2.14.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 2
    maintainers = ['lrknox']

    version('4.2.15', sha256='dbeeef525af7c2d01539906c28953f0fdab7dba603d1bc1ec4a5af60d002c459')
    version('4.2.14', sha256='2d383e87c8a0ca6a5352adbd1d5546e6cc43dc21ff7d90f93efa644d85c0b14a')
    version('4.2.13', sha256='be9813c1dc3712c2df977d4960e1f13f20f447dfa8c3ce53331d610c1f470483')
    version('4.2.12', sha256='dd419c55e85d1a0e13f3ea5ed35d00710033ccb16c85df088eb7925d486e040c')
    version('4.2.11', sha256='c3f7753b2fb9b27d09eced4d2164605f111f270c9a60b37a578f7de02de86d24')

    variant('szip', default=False, description="Enable szip support")
    variant('external-xdr', default=sys.platform != 'darwin',
            description="Use an external XDR backend")
    variant('netcdf', default=False,
            description='Build NetCDF API (version 2.3.2)')
    variant('fortran', default=False,
            description='Enable Fortran interface')
    variant('java', default=False,
            description='Enable Java JNI interface')
    variant('shared', default=False, description='Enable shared library')
    variant('pic', default=True,
            description='Produce position-independent code')

    depends_on('zlib@1.1.4:')
    depends_on('jpeg')
    depends_on('szip', when='+szip')
    depends_on('rpc', when='+external-xdr')

    depends_on('bison', type='build')
    depends_on('flex',  type='build')
    depends_on('java@7:', when='+java', type=('build', 'run'))

    # https://forum.hdfgroup.org/t/cant-build-hdf-4-2-14-with-jdk-11-and-enable-java/5702
    patch('disable_doclint.patch', when='@:4.2.14^java@9:')

    patch('for_aarch64.patch', when='target=aarch64:')

    conflicts('^libjpeg@:6a')

    # configure: error: Cannot build shared fortran libraries.
    # Please configure with --disable-fortran flag.
    conflicts('+fortran', when='+shared')

    # configure: error: Java requires shared libraries to be built
    conflicts('+java', when='~shared')

    # configure: WARNING: unrecognized options: --enable-java
    conflicts('+java', when='@:4.2.11')

    # The Java interface library uses netcdf-related macro definitions even
    # when netcdf is disabled and the macros are not defined, e.g.:
    # hdfsdsImp.c:158:30: error: 'MAX_NC_NAME' undeclared
    conflicts('+java', when='@4.2.12:4.2.13~netcdf')

    # TODO: '@:4.2.14 ~external-xdr' and the fact that we compile for 64 bit
    #  architecture should be in conflict

    @property
    def libs(self):
        """HDF can be queried for the following parameters:

        - "shared": shared libraries (default if '+shared')
        - "static": static libraries (default if '~shared')
        - "transitive": append transitive dependencies to the list of static
            libraries (the argument is ignored if shared libraries are
            requested)

        :return: list of matching libraries
        """
        libraries = ['libmfhdf', 'libdf']

        query_parameters = self.spec.last_query.extra_parameters

        if 'shared' in query_parameters:
            shared = True
        elif 'static' in query_parameters:
            shared = False
        else:
            shared = '+shared' in self.spec

        libs = find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

        if not libs:
            msg = 'Unable to recursively locate {0} {1} libraries in {2}'
            raise spack.error.NoLibrariesError(
                msg.format('shared' if shared else 'static',
                           self.spec.name,
                           self.spec.prefix))

        if not shared and 'transitive' in query_parameters:
            libs += self.spec['jpeg:transitive'].libs
            libs += self.spec['zlib:transitive'].libs
            if '+szip' in self.spec:
                libs += self.spec['szip:transitive'].libs
            if ('+external-xdr' in self.spec and
                    self.spec['rpc'].name != 'libc'):
                libs += self.spec['rpc:transitive'].libs

        return libs

    def flag_handler(self, name, flags):
        if '+pic' in self.spec:
            if name == 'cflags':
                flags.append(self.compiler.cc_pic_flag)
            elif name == 'fflags':
                flags.append(self.compiler.f77_pic_flag)

        return flags, None, None

    def setup_build_environment(self, env):
        env.prepend_path('CPATH', self.spec['libtirpc'].prefix.include.tirpc)

    def configure_args(self):
        config_args = ['--enable-production',
                       '--enable-static',
                       '--with-zlib=%s' % self.spec['zlib'].prefix,
                       '--with-jpeg=%s' % self.spec['jpeg'].prefix]

        config_args += self.enable_or_disable('shared')
        config_args += self.enable_or_disable('netcdf')
        config_args += self.enable_or_disable('fortran')
        config_args += self.enable_or_disable('java')

        if '+szip' in self.spec:
            config_args.append('--with-szlib=%s' % self.spec['szip'].prefix)
        else:
            config_args.append('--without-szlib')

        if '~external-xdr' in self.spec:
            config_args.append('--enable-hdf4-xdr')
        elif self.spec['rpc'].name != 'libc':
            # We should not specify '--disable-hdf4-xdr' due to a bug in the
            # configure script.
            config_args.append('LIBS=%s' % self.spec['rpc'].libs.link_flags)

        # https://github.com/Parallel-NetCDF/PnetCDF/issues/61
        if self.spec.satisfies('%gcc@10:'):
            config_args.extend([
                'FFLAGS=-fallow-argument-mismatch',
                'FCFLAGS=-fallow-argument-mismatch']
            )

        return config_args

    # Otherwise, we randomly get:
    # SDgetfilename:
    #   incorrect file being opened - expected <file755>, retrieved <file754>
    def check(self):
        with working_dir(self.build_directory):
            make('check', parallel=False)

    extra_install_tests = 'hdf/util/testfiles'

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(self.extra_install_tests)

    def _test_check_versions(self):
        """Perform version checks on selected installed package binaries."""
        spec_vers_str = 'Version {0}'.format(self.spec.version.up_to(2))

        exes = ['hdfimport', 'hrepack', 'ncdump', 'ncgen']
        for exe in exes:
            reason = 'test: ensuring version of {0} is {1}' \
                .format(exe, spec_vers_str)
            self.run_test(exe, ['-V'], spec_vers_str, installed=True,
                          purpose=reason, skip_missing=True)

    def _test_gif_converters(self):
        """This test performs an image conversion sequence and diff."""
        work_dir = '.'
        storm_fn = os.path.join(self.install_test_root,
                                self.extra_install_tests, 'storm110.hdf')
        gif_fn = 'storm110.gif'
        new_hdf_fn = 'storm110gif.hdf'

        # Convert a test HDF file to a gif
        self.run_test('hdf2gif', [storm_fn, gif_fn], '', installed=True,
                      purpose="test: hdf-to-gif", work_dir=work_dir)

        # Convert the gif to an HDF file
        self.run_test('gif2hdf', [gif_fn, new_hdf_fn], '', installed=True,
                      purpose="test: gif-to-hdf", work_dir=work_dir)

        # Compare the original and new HDF files
        self.run_test('hdiff', [new_hdf_fn, storm_fn], '', installed=True,
                      purpose="test: compare orig to new hdf",
                      work_dir=work_dir)

    def _test_list(self):
        """This test compares low-level HDF file information to expected."""
        storm_fn = os.path.join(self.install_test_root,
                                self.extra_install_tests, 'storm110.hdf')
        test_data_dir = self.test_suite.current_test_data_dir
        work_dir = '.'

        reason = 'test: checking hdfls output'
        details_file = os.path.join(test_data_dir, 'storm110.out')
        expected = get_escaped_text_output(details_file)
        self.run_test('hdfls', [storm_fn], expected, installed=True,
                      purpose=reason, skip_missing=True, work_dir=work_dir)

    def test(self):
        """Perform smoke tests on the installed package."""
        # Simple version check tests on subset of known binaries that respond
        self._test_check_versions()

        # Run gif converter sequence test
        self._test_gif_converters()

        # Run hdfls output
        self._test_list()
