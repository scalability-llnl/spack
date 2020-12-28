# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
from shutil import copyfile, Error

from spack.package import *


class NetcdfFortran(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the Fortran
    distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.5.3.tar.gz"

    maintainers = ['skosukhin', 'WardF']

    version('4.5.3', sha256='123a5c6184336891e62cf2936b9f2d1c54e8dee299cfd9d2c1a1eb05dd668a74')
    version('4.5.2', sha256='b959937d7d9045184e9d2040a915d94a7f4d0185f4a9dceb8f08c94b0c3304aa')
    version('4.4.5', sha256='2467536ce29daea348c736476aa8e684c075d2f6cab12f3361885cb6905717b8')
    version('4.4.4', sha256='b2d395175f8d283e68c8be516e231a96b191ade67ad0caafaf7fa01b1e6b5d75')
    version('4.4.3', sha256='330373aa163d5931e475b5e83da5c1ad041e855185f24e6a8b85d73b48d6cda9')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True, description='Enable shared library')
    variant('doc', default=False, description='Enable building docs')

    depends_on('netcdf-c')
    depends_on('doxygen', when='+doc', type='build')

    # The default libtool.m4 is too old to handle NAG compiler properly:
    # https://github.com/Unidata/netcdf-fortran/issues/94
    # Moreover, Libtool can't handle '-pthread' flag coming from libcurl,
    # doesn't inject convenience libraries into the shared ones, and is unable
    # to detect NAG when it is called with an MPI wrapper.
    patch('nag_libtool_2.4.2.patch', when='@:4.4.4%nag')
    patch('nag_libtool_2.4.6.patch', when='@4.4.5:%nag')

    # Enable 'make check' for NAG, which is too strict.
    patch('nag_testing.patch', when='@4.4.5%nag')

    # File fortran/nf_logging.F90 is compiled without -DLOGGING, which leads
    # to missing symbols in the library. Additionally, the patch enables
    # building with NAG, which refuses to compile empty source files (see also
    # comments in the patch):
    patch('logging.patch', when='@:4.4.5')

    # Prevent excessive linking to system libraries. Without this patch the
    # library might get linked to the system installation of libcurl. See
    # https://github.com/Unidata/netcdf-fortran/commit/0a11f580faebbc1c4dce68bf5135709d1c7c7cc1#diff-67e997bcfdac55191033d57a16d1408a
    patch('excessive_linking.patch', when='@4.4.5')

    # Parallel builds do not work in the fortran directory. This patch is
    # derived from https://github.com/Unidata/netcdf-fortran/pull/211
    patch('no_parallel_build.patch', when='@4.5.2')

    def flag_handler(self, name, flags):
        config_flags = None

        if name == 'cflags':
            if '+pic' in self.spec:
                flags.append(self.compiler.cc_pic_flag)
        elif name == 'fflags':
            if '+pic' in self.spec:
                flags.append(self.compiler.f77_pic_flag)
            if self.spec.satisfies('%gcc@10:'):
                # https://github.com/Unidata/netcdf-fortran/issues/212
                flags.append('-fallow-argument-mismatch')
            elif self.compiler.name == 'cce':
                # Cray compiler generates module files with uppercase names by
                # default, which is not handled by the makefiles of
                # NetCDF-Fortran:
                # https://github.com/Unidata/netcdf-fortran/pull/221.
                # The following flag forces the compiler to produce module
                # files with lowercase names.
                flags.append('-ef')
        elif name == 'ldflags':
            # We need to specify LDFLAGS to get correct dependency_libs
            # in libnetcdff.la, so packages that use libtool for linking
            # could correctly link to all the dependencies even when the
            # building takes place outside of Spack environment, i.e.
            # without Spack's compiler wrappers.
            config_flags = [self.spec['netcdf-c'].libs.search_flags]

        return flags, None, config_flags

    @property
    def libs(self):
        libraries = ['libnetcdff']

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

        if libs:
            return libs

        msg = 'Unable to recursively locate {0} {1} libraries in {2}'
        raise spack.error.NoLibrariesError(
            msg.format('shared' if shared else 'static',
                       self.spec.name,
                       self.spec.prefix))

    def configure_args(self):
        config_args = self.enable_or_disable('shared')
        config_args.append('--enable-static')

        # We need to build with MPI wrappers if either of the parallel I/O
        # features is enabled in netcdf-c:
        # https://www.unidata.ucar.edu/software/netcdf/docs/building_netcdf_fortran.html
        netcdf_c_spec = self.spec['netcdf-c']
        if '+mpi' in netcdf_c_spec or '+parallel-netcdf' in netcdf_c_spec:
            config_args.append('CC=%s' % self.spec['mpi'].mpicc)
            config_args.append('FC=%s' % self.spec['mpi'].mpifc)
            config_args.append('F77=%s' % self.spec['mpi'].mpif77)

        if '+doc' in self.spec:
            config_args.append('--enable-doxygen')
        else:
            config_args.append('--disable-doxygen')

        return config_args

    @when('@:4.4.5')
    def check(self):
        with working_dir(self.build_directory):
            make('check', parallel=False)

    @run_after('install')
    def cray_module_filenames(self):
        # Cray compiler searches for module files with uppercase names by
        # default and with lowercase names when the '-ef' flag is specified.
        # To avoid warning messages when compiler user applications in both
        # cases, we create copies of all '*.mod' files in the prefix/include
        # with names in upper- and lowercase.
        if self.spec.compiler.name != 'cce':
            return

        with working_dir(self.spec.prefix.include):
            for f in glob.glob('*.mod'):
                name, ext = os.path.splitext(f)
                try:
                    # Create a copy with uppercase name:
                    copyfile(f, name.upper() + ext)
                except Error:
                    # Assume that the exception tells us that the file with
                    # uppercase name already exists. Try to create a file with
                    # lowercase name then:
                    try:
                        copyfile(f, name.lower() + ext)
                    except Error:
                        pass
