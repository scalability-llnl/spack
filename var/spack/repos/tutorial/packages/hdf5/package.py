# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil
import sys

from spack import *


class Hdf5(AutotoolsPackage):
    """HDF5 is a data model, library, and file format for storing and managing
    data. It supports an unlimited variety of datatypes, and is designed for
    flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "https://support.hdfgroup.org/HDF5/"
    url      = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.1/src/hdf5-1.10.1.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3

    version('1.10.4', '8f60dc4dd6ab5fcd23c750d1dc5bca3d0453bdce5c8cdaf0a4a61a9d1122adb2')
    version('1.10.3', 'b600d7c914cfa80ae127cd1a1539981213fee9994ac22ebec9e3845e951d9b39')
    version('1.10.2', '8d4eae84e533efa57496638fd0dca8c3')
    version('1.10.1', '43a2f9466702fb1db31df98ae6677f15')
    version('1.10.0-patch1', '9180ff0ef8dc2ef3f61bd37a7404f295')
    version('1.10.0', 'bdc935337ee8282579cd6bc4270ad199')
    version('1.8.19', '7f568e2464d4ab0a74d16b23956d900b')
    version('1.8.18', 'dd2148b740713ca0295442ec683d7b1c')
    version('1.8.17', '7d572f8f3b798a628b8245af0391a0ca')
    version('1.8.16', 'b8ed9a36ae142317f88b0c7ef4b9c618')
    version('1.8.15', '03cccb5b33dbe975fdcd8ae9dc021f24')
    version('1.8.14', 'a482686e733514a51cde12d6fe5c5d95')
    version('1.8.13', 'c03426e9e77d7766944654280b467289')
    version('1.8.12', 'd804802feb99b87fc668a90e6fa34411')
    version('1.8.10', '710aa9fb61a51d61a7e2c09bf0052157')

    variant('debug', default=False,
            description='Builds a debug version of the library')
    variant('shared', default=True,
            description='Builds a shared version of the library')

    variant('hl', default=False, description='Enable the high-level library')
    variant('cxx', default=False, description='Enable C++ support')
    variant('fortran', default=False, description='Enable Fortran support')
    variant('threadsafe', default=False,
            description='Enable thread-safe capabilities')

    variant('mpi', default=True, description='Enable MPI support')
    variant('szip', default=False, description='Enable szip support')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    depends_on('mpi', when='+mpi')
    # numactl does not currently build on darwin
    if sys.platform != 'darwin':
        depends_on('numactl', when='+mpi+fortran')
    depends_on('szip', when='+szip')
    depends_on('zlib@1.1.2:')

    # There are several officially unsupported combinations of the features:
    # 1. Thread safety is not guaranteed via high-level C-API but in some cases
    #    it works.
    # conflicts('+threadsafe+hl')

    # 2. Thread safety is not guaranteed via Fortran (CXX) API, but it's
    #    possible for a dependency tree to contain a package that uses Fortran
    #    (CXX) API in a single thread and another one that uses low-level C-API
    #    in multiple threads. To allow for such scenarios, we don't specify the
    #    following conflicts.
    # conflicts('+threadsafe+cxx')
    # conflicts('+threadsafe+fortran')

    # 3. Parallel features are not supported via CXX API, but for the reasons
    #    described in #2 we allow for such combination.
    # conflicts('+mpi+cxx')

    # There are known build failures with intel@18.0.1. This issue is
    # discussed and patch is provided at
    # https://software.intel.com/en-us/forums/intel-fortran-compiler-for-linux-and-mac-os-x/topic/747951.
    patch('h5f90global-mult-obj-same-equivalence-same-common-block.patch',
          when='@1.10.1%intel@18')

    # Turn line comments into block comments to conform with pre-C99 language
    # standards. Versions of hdf5 after 1.8.10 don't require this patch,
    # either because they conform to pre-C99 or neglect to ask for pre-C99
    # language standards from their compiler. The hdf5 build system adds
    # the -ansi cflag (run 'man gcc' for info on -ansi) for some versions
    # of some compilers (see hdf5-1.8.10/config/gnu-flags). The hdf5 build
    # system does not provide an option to disable -ansi, but since the
    # pre-C99 code is restricted to just five lines of line comments in
    # three src files, this patch accomplishes the simple task of patching the
    # three src files and leaves the hdf5 build system alone.
    patch('pre-c99-comments.patch', when='@1.8.10')

    # There are build errors with GCC 8, see
    # https://forum.hdfgroup.org/t/1-10-2-h5detect-compile-error-gcc-8-1-0-on-centos-7-2-solved/4441
    patch('https://salsa.debian.org/debian-gis-team/hdf5/raw/bf94804af5f80f662cad80a5527535b3c6537df6/debian/patches/gcc-8.patch', sha256='57cee5ff1992b4098eda079815c36fc2da9b10e00a9056df054f2384c4fc7523', when='@1.10.2%gcc@8:')

    filter_compiler_wrappers('h5cc', 'h5c++', 'h5fc', relative_root='bin')

    def url_for_version(self, version):
        url = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{0}/hdf5-{1}/src/hdf5-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    @property
    def libs(self):
        """HDF5 can be queried for the following parameters:

        - "hl": high-level interface
        - "cxx": C++ APIs
        - "fortran": Fortran APIs

        :return: list of matching libraries
        """
        # This map contains a translation from query_parameters
        # to the libraries needed
        query2libraries = {  # noqa: F841
            tuple(): ['libhdf5'],
            ('cxx', 'fortran', 'hl'): [
                'libhdf5hl_fortran',
                'libhdf5_hl_cpp',
                'libhdf5_hl',
                'libhdf5_fortran',
                'libhdf5',
            ],
            ('cxx', 'hl'): [
                'libhdf5_hl_cpp',
                'libhdf5_hl',
                'libhdf5',
            ],
            ('fortran', 'hl'): [
                'libhdf5hl_fortran',
                'libhdf5_hl',
                'libhdf5_fortran',
                'libhdf5',
            ],
            ('hl',): [
                'libhdf5_hl',
                'libhdf5',
            ],
            ('cxx', 'fortran'): [
                'libhdf5_fortran',
                'libhdf5_cpp',
                'libhdf5',
            ],
            ('cxx',): [
                'libhdf5_cpp',
                'libhdf5',
            ],
            ('fortran',): [
                'libhdf5_fortran',
                'libhdf5',
            ]
        }

        # TUTORIAL: you need to fix the implementation below, and
        # return the correct list of libraries according to the
        # query parameters your dependency has used.
        #
        # You can retrieve the query parameters by doing
        #
        # query_parameters = self.spec.last_query.extra_parameters
        #
        # and use the map above to query the list of libraries you need
        # to search.
        #
        # Finally uncomment the lines below to return a LibraryList
        #
        # shared = '+shared' in self.spec
        # return find_libraries(
        #     libraries, root=self.prefix, shared=shared, recursive=True
        # )
        return []

    @run_before('configure')
    def fortran_check(self):
        if '+fortran' in self.spec and not self.compiler.fc:
            msg = 'cannot build a Fortran variant without a Fortran compiler'
            raise RuntimeError(msg)

    def configure_args(self):
        # Always enable this option. This does not actually enable any
        # features: it only *allows* the user to specify certain
        # combinations of other arguments. Enabling it just skips a
        # sanity check in configure, so this doesn't merit a variant.
        extra_args = ['--enable-unsupported']
        extra_args += self.enable_or_disable('threadsafe')
        extra_args += self.enable_or_disable('cxx')
        extra_args += self.enable_or_disable('hl')
        extra_args += self.enable_or_disable('fortran')

        if '+szip' in self.spec:
            extra_args.append('--with-szlib=%s' % self.spec['szip'].prefix)
        else:
            extra_args.append('--without-szlib')

        if self.spec.satisfies('@1.10:'):
            if '+debug' in self.spec:
                extra_args.append('--enable-build-mode=debug')
            else:
                extra_args.append('--enable-build-mode=production')
        else:
            if '+debug' in self.spec:
                extra_args.append('--enable-debug=all')
            else:
                extra_args.append('--enable-production')

            # '--enable-fortran2003' no longer exists as of version 1.10.0
            if '+fortran' in self.spec:
                extra_args.append('--enable-fortran2003')
            else:
                extra_args.append('--disable-fortran2003')

        if '+shared' in self.spec:
            extra_args.append('--enable-shared')
        else:
            extra_args.append('--disable-shared')
            extra_args.append('--enable-static-exec')

        if '+pic' in self.spec:
            extra_args.extend([
                'CFLAGS=%s' % self.compiler.cc_pic_flag,
                'CXXFLAGS=%s' % self.compiler.cxx_pic_flag,
                'FCFLAGS=%s' % self.compiler.fc_pic_flag,
            ])

        if '+mpi' in self.spec:
            # The HDF5 configure script warns if cxx and mpi are enabled
            # together. There doesn't seem to be a real reason for this, except
            # that parts of the MPI interface are not accessible via the C++
            # interface. Since they are still accessible via the C interface,
            # this is not actually a problem.
            extra_args += ['--enable-parallel',
                           'CC=%s' % self.spec['mpi'].mpicc]

            if '+cxx' in self.spec:
                extra_args.append('CXX=%s' % self.spec['mpi'].mpicxx)

            if '+fortran' in self.spec:
                extra_args.append('FC=%s' % self.spec['mpi'].mpifc)

        extra_args.append('--with-zlib=%s' % self.spec['zlib'].prefix)

        return extra_args

    @run_after('configure')
    def patch_postdeps(self):
        if '@:1.8.14' in self.spec:
            # On Ubuntu14, HDF5 1.8.12 (and maybe other versions)
            # mysteriously end up with "-l -l" in the postdeps in the
            # libtool script.  Patch this by removing the spurious -l's.
            filter_file(
                r'postdeps="([^"]*)"',
                lambda m: 'postdeps="%s"' % ' '.join(
                    arg for arg in m.group(1).split(' ') if arg != '-l'),
                'libtool')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # Build and run a small program to test the installed HDF5 library
        spec = self.spec
        print("Checking HDF5 installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <hdf5.h>
#include <assert.h>
#include <stdio.h>
int main(int argc, char **argv) {
  unsigned majnum, minnum, relnum;
  herr_t herr = H5get_libversion(&majnum, &minnum, &relnum);
  assert(!herr);
  printf("HDF5 version %d.%d.%d %u.%u.%u\n", H5_VERS_MAJOR, H5_VERS_MINOR,
         H5_VERS_RELEASE, majnum, minnum, relnum);
  return 0;
}
"""
            expected = """\
HDF5 version {version} {version}
""".format(version=str(spec.version.up_to(3)))
            with open("check.c", 'w') as f:
                f.write(source)
            if '+mpi' in spec:
                cc = Executable(spec['mpi'].mpicc)
            else:
                cc = Executable(self.compiler.cc)
            cc(*(['-c', "check.c"] + spec['hdf5'].headers.cpp_flags.split()))
            cc(*(['-o', "check",
                  "check.o"] + spec['hdf5'].libs.ld_flags.split()))
            try:
                check = Executable('./check')
                output = check(output=str)
            except ProcessError:
                output = ""
            success = output == expected
            if not success:
                print("Produced output does not match expected output.")
                print("Expected output:")
                print('-' * 80)
                print(expected)
                print('-' * 80)
                print("Produced output:")
                print('-' * 80)
                print(output)
                print('-' * 80)
                raise RuntimeError("HDF5 install check failed")
        shutil.rmtree(checkdir)
