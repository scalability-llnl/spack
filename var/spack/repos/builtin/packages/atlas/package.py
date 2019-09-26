# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.package_test import compile_c_and_execute, compare_output_file


class Atlas(Package):
    """Automatically Tuned Linear Algebra Software, generic shared ATLAS is an
    approach for the automatic generation and optimization of numerical
    software. Currently ATLAS supplies optimized versions for the complete set
    of linear algebra kernels known as the Basic Linear Algebra Subroutines
    (BLAS), and a subset of the linear algebra routines in the LAPACK library.
    """
    homepage = "http://math-atlas.sourceforge.net/"

    # Developer (unstable)
    version('3.11.41', sha256='477d567a8d683e891d786e9e8bb6ad6659daa9ba18e8dd0e2f70b7a54095f8de')
    version('3.11.39', '5f3252fa980f5f060f93edd4669321e2')
    version('3.11.34', '0b6c5389c095c4c8785fd0f724ec6825')

    # Stable
    version('3.10.3', 'd6ce4f16c2ad301837cfb3dade2f7cef', preferred=True)
    version('3.10.2', 'a4e21f343dec8f22e7415e339f09f6da')

    # not all packages (e.g. Trilinos@12.6.3) stopped using deprecated in 3.6.0
    # Lapack routines. Stick with 3.5.0 until this is fixed.
    resource(name='lapack',
             url='http://www.netlib.org/lapack/lapack-3.5.0.tgz',
             md5='b1d3e3e425b2e44a06760ff173104bdf',
             destination='spack-resource-lapack',
             when='@3:')

    variant('shared', default=True, description='Builds shared library')

    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'none'),
        multi=False
    )

    variant('tune_cpu', default=-1, multi=False,
            description="Number of threads to tune to, "
            "-1 for autodetect, 0 for no threading")

    provides('blas')
    provides('lapack')

    parallel = False

    def url_for_version(self, version):
        url = 'https://sourceforge.net/projects/math-atlas/files/'

        if version >= Version('3.11'):
            url += 'Developer%20%28unstable%29/{0}/atlas{0}.tar.bz2'
        else:
            url += 'Stable/{0}/atlas{0}.tar.bz2'

        return url.format(version)

    def patch(self):
        # Disable thread check.  LLNL's environment does not allow
        # disabling of CPU throttling in a way that ATLAS actually
        # understands.
        filter_file(r'^\s+if \(thrchk\) exit\(1\);', 'if (0) exit(1);',
                    'CONFIG/src/config.c')
        # TODO: investigate a better way to add the check back in
        # TODO: using, say, MSRs.  Or move this to a variant.

    def install(self, spec, prefix):
        # reference to other package managers
        # https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/a/atlas.py
        # https://github.com/macports/macports-ports/blob/master/math/atlas/Portfile
        # https://github.com/Homebrew/homebrew-science/pull/3571
        options = []
        if '+shared' in spec:
            options.extend([
                '--shared'
            ])
            # TODO: for non GNU add '-Fa', 'alg', '-fPIC' ?

        # configure for 64-bit build
        options.extend([
            '-b', '64'
        ])

        # set number of cpu's to tune to
        options.extend([
            '-t', spec.variants['tune_cpu'].value
        ])

        # set compilers:
        options.extend([
            '-C', 'ic', spack_cc,
            '-C', 'if', spack_f77
        ])

        # Workaround for macOS Clang:
        # http://math-atlas.sourceforge.net/atlas_install/node66.html
        if spec.satisfies('@3.10.3: %clang platform=darwin'):
            options.append('--force-clang=' + spack_cc)

        # Lapack resource to provide full lapack build. Note that
        # ATLAS only provides a few LAPACK routines natively.
        options.append('--with-netlib-lapack-tarfile=%s' %
                       self.stage[1].archive_file)

        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('check')
            make('ptcheck')
            make('time')
            if '+shared' in spec:
                with working_dir('lib'):
                    make('shared_all')

            make("install")
            if self.run_tests:
                self.install_test()

    @property
    def libs(self):
        # libsatlas.[so,dylib,dll ] contains all serial APIs (serial lapack,
        # serial BLAS), and all ATLAS symbols needed to support them. Whereas
        # libtatlas.[so,dylib,dll ] is parallel (multithreaded) version.
        is_threaded = self.spec.satisfies('threads=pthreads')
        if '+shared' in self.spec:
            to_find = ['libtatlas'] if is_threaded else ['libsatlas']
            shared = True
        else:
            interfaces = [
                'libptcblas',
                'libptf77blas'
            ] if is_threaded else [
                'libcblas',
                'libf77blas'
            ]
            to_find = ['liblapack'] + interfaces + ['libatlas']
            shared = False
        return find_libraries(
            to_find, root=self.prefix, shared=shared, recursive=True
        )

    def install_test(self):
        source_file = join_path(os.path.dirname(self.module.__file__),
                                'test_cblas_dgemm.c')
        blessed_file = join_path(os.path.dirname(self.module.__file__),
                                 'test_cblas_dgemm.output')

        include_flags = ["-I%s" % self.spec.prefix.include]
        link_flags = self.libs.ld_flags.split()

        output = compile_c_and_execute(source_file, include_flags, link_flags)
        compare_output_file(output, blessed_file)
