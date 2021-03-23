# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob

from spack import *
from spack.pkg.builtin.boost import Boost


class NcbiToolkit(AutotoolsPackage):
    """NCBI C++ Toolkit"""

    homepage = "https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/"
    url      = "ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools++/CURRENT/ncbi_cxx--22_0_0.tar.gz"

    version('22_0_0', sha256='ef39429bbc7f13c44c0d327432d9cfb430f9f20d10d825e6b2c4ddd7ccce457f',
            url='ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools++/ARCHIVE/2019/Mar_28_2019/ncbi_cxx--22_0_0.tar.gz')
    version('21_0_0', sha256='48cc3ae24ca63d1ab1be148e7525e8c5b9f4eaa5eb36d172800784b640a84a4f',
            url='ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools++/ARCHIVE/2018/Apr_2_2018/ncbi_cxx--21_0_0.tar.gz')

    variant('debug', default=False,
            description='Build debug versions of libs and apps')

    depends_on('boost@1.35.0:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('bzip2')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('libxslt@1.1.14:')
    depends_on('lzo')
    depends_on('pcre')
    depends_on('giflib')
    depends_on('sqlite@3.6.6:')
    depends_on('zlib')
    depends_on('samtools')
    depends_on('bamtools')

    def configure_args(self):
        args = ['--without-sybase', '--without-fastcgi']
        if '+debug' not in self.spec:
            args += ['--without-debug']
        return args

    def patch(self):
        with working_dir(join_path('src', 'util', 'image')):
            filter_file(r'jpeg_start_compress(&cinfo, true)',
                        'jpeg_start_compress(&cinfo, TRUE)',
                        'image_io_jpeg.cpp', string=True)
        # TODO: Convert these substitutions into BOOST_VERSION preprocessor
        # patches to send upstream.
        if self.spec.satisfies('^boost@1.69:'):
            with working_dir(join_path('include', 'corelib')):
                filter_file(r'(boost::unit_test::decorator::collector)',
                            r'\1_t', 'test_boost.hpp')
        if self.spec.satisfies('^boost@1.70:'):
            with working_dir(join_path('include', 'corelib')):
                filter_file(('unit_test::ut_detail::'
                             'ignore_unused_variable_warning'),
                            'ignore_unused', 'test_boost.hpp', string=True)
            with working_dir(join_path('src', 'corelib')):
                for file_ in ['test_boost.cpp', 'teamcity_boost.cpp']:
                    filter_file(
                        r'(void log_build_info\s*\(.*ostream&[^)]*)\);',
                        r'\1, bool log_build_info = true);', file_)
                    filter_file(r'(::log_build_info\(.*ostream.*&[^)]+)\)',
                                r'\1, bool log_build_info)', file_)
                    filter_file(r'(log_build_info\(ostr)\)', r'\1, true)',
                                file_)

    def build(self, spec, prefix):
        with working_dir(join_path(glob(
                '*MT64')[0], 'build')):
            make('all_r')
