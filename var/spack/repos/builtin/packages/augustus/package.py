# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Augustus(MakefilePackage):
    """AUGUSTUS is a program that predicts genes in eukaryotic
       genomic sequences"""

    homepage = "http://bioinf.uni-greifswald.de/augustus/"
    url      = "https://github.com/Gaius-Augustus/Augustus/archive/v3.3.4.tar.gz"

    # Releases have moved to github
    version('3.4.0', sha256='2c06cf5953da5afdce1478fa10fcd3c280a3b050f1b2367bf3e731d7374d9bb8')
    version('3.3.2', sha256='d09f972cfd88deb34b19b69878eb8af3bbbe4f1cde1434b69cedc2aa6247a0f2')
    version('3.3.1-tag1', sha256='011379606f381ee21b9716f83e8a1a57b2aaa01aefeebd2748104efa08c47cab',
            url='https://github.com/Gaius-Augustus/Augustus/archive/v3.3.1-tag1.tar.gz')
    version('3.3',   sha256='b5eb811a4c33a2cc3bbd16355e19d530eeac6d1ac923e59f48d7a79f396234ee',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/augustus-3.3.tar.gz')
    version('3.2.3', sha256='a1af128aefd228dea0c46d6f5234910fdf068a2b9133175ca8da3af639cb4514',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/augustus-3.2.3.tar.gz')

    depends_on('perl', type=('build', 'run'))
    depends_on('python', when='@3.3.1:', type=('build', 'run'))
    depends_on('bamtools')
    depends_on('gsl')
    depends_on('boost')
    depends_on('zlib')
    depends_on('htslib')
    depends_on('bcftools')
    depends_on('samtools')
    depends_on('curl', when='@3.3.1:')
    depends_on('sqlite', when='@3.4.0:')
    depends_on('mysql-client', when='@3.4.0:')
    depends_on('mysqlpp', when='@3.4.0:')
    depends_on('lp-solve', when='@3.4.0:')
    depends_on('suite-sparse', when='@3.4.0:')

    # Trying to use filter_file here got too complicated so use a patch with a
    # corresponding environment variable
    patch('bam2wig_Makefile.patch', when='@3.4.0:')

    def edit(self, spec, prefix):
        # Set compile commands for each compiler and
        # Fix for using 'boost' on Spack. (only after ver.3.3.1-tag1)
        if self.version >= Version('3.3.1-tag1'):
            with working_dir(join_path('auxprogs', 'utrrnaseq', 'Debug')):
                filter_file('g++', spack_cxx, 'makefile', string=True)
                filter_file('g++ -I/usr/include/boost', '{0} -I{1}'
                            .format(spack_cxx,
                                    self.spec['boost'].prefix.include),
                            'src/subdir.mk', string=True)

        # Makefiles to set spack compiler over gcc/g++
        makefiles = [
            'auxprogs/aln2wig/Makefile',
            'auxprogs/bam2hints/Makefile',
            'auxprogs/bam2wig/Makefile',
            'auxprogs/compileSpliceCands/Makefile',
            'auxprogs/homGeneMapping/src/Makefile',
            'auxprogs/joingenes/Makefile',
            'src/Makefile',
        ]
        if self.version < Version('3.4.0'):
            makefiles.append('auxprogs/checkTargetSortedness/Makefile')

        if self.version >= Version('3.4.0'):
            makefiles.extend([
                'auxprogs/filterBam/src/Makefile',
                'src/unittests/Makefile',
            ])

        for makefile in makefiles:
            filter_file('gcc', spack_cc, makefile, string=True)
            filter_file('g++', spack_cxx, makefile, string=True)

        bamtools = self.spec['bamtools'].prefix
        bcftools = self.spec['bcftools'].prefix
        htslib = self.spec['htslib'].prefix
        samtools = self.spec['samtools'].prefix

        with working_dir(join_path('auxprogs', 'filterBam', 'src')):
            makefile = FileFilter('Makefile')
            makefile.filter('BAMTOOLS = .*', 'BAMTOOLS = {0}'.format(bamtools))
            makefile.filter('INCLUDES = *',
                            'INCLUDES = -I$(BAMTOOLS)/include/bamtools ')
            if 'bamtools@2.5:' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib64'
                                '/libbamtools.a -lz')
            if 'bamtools@:2.4' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib/bamtools'
                                '/libbamtools.a -lz')
        with working_dir(join_path('auxprogs', 'bam2hints')):
            makefile = FileFilter('Makefile')
            makefile.filter('/usr/include/bamtools',
                            '{0}/include/bamtools'.format(bamtools))
            if 'bamtools@2.5:' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = {0}/lib64'
                                '/libbamtools.a -lz'.format(bamtools))
            if 'bamtools@:2.4' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = {0}/lib/bamtools'
                                '/libbamtools.a -lz'.format(bamtools))

        if self.version < Version('3.4.0'):
            with working_dir(join_path('auxprogs', 'bam2wig')):
                makefile = FileFilter('Makefile')
                # point tools to spack installations
                makefile.filter('BCFTOOLS=.*$',
                                'BCFTOOLS={0}/include'.format(bcftools))
                makefile.filter('SAMTOOLS=.*$',
                                'SAMTOOLS={0}/include'.format(samtools))
                makefile.filter('HTSLIB=.*$',
                                'HTSLIB={0}/include'.format(htslib))

                # fix bad linking dirs
                makefile.filter('$(SAMTOOLS)/libbam.a',
                                '$(SAMTOOLS)/../lib/libbam.a', string=True)
                makefile.filter('$(HTSLIB)/libhts.a',
                                '$(HTSLIB)/../lib/libhts.a', string=True)
            with working_dir(join_path('auxprogs', 'checkTargetSortedness')):
                makefile = FileFilter('Makefile')
                makefile.filter('SAMTOOLS.*=.*$',
                                'SAMTOOLS={0}/include'.format(samtools))
                makefile.filter('LIBS=-lbam',
                                'LIBS=$(SAMTOOLS)/../lib/libbam.a',
                                string=True)
        else:
            mysql = self.spec['mysql-client'].prefix
            mysqlpp = self.spec['mysqlpp'].prefix
            lpsolve = self.spec['lp-solve'].prefix

            with working_dir('src'):
                makefile = FileFilter('Makefile')
                makefile.filter(r'/usr/include/mysql\+\+',
                                '{0}/include/mysql++'.format(mysqlpp))
                if '^mariadb-c-client' in spec:
                    makefile.filter('/usr/include/mysql',
                                    '{0}/include/mariadb'.format(mysql))
                else:
                    makefile.filter('/usr/include/mysql',
                                    '{0}/include/mysql'.format(mysql))
                makefile.filter('/usr/include/lpsolve',
                                '{0}/include/lpsolve'.format(lpsolve))

    def install(self, spec, prefix):
        install_tree('bin', join_path(self.spec.prefix, 'bin'))
        install_tree('config', join_path(self.spec.prefix, 'config'))
        install_tree('scripts', join_path(self.spec.prefix, 'scripts'))

    @run_after('install')
    def filter_sbang(self):
        with working_dir(self.prefix.scripts):
            pattern = '^#!.*'
            repl = '#!{0}'.format(self.spec['perl'].command.path)
            files = glob.glob("*.pl")
            for file in files:
                filter_file(pattern, repl, *files, backup=False)

            repl = '#!{0}'.format(self.spec['python'].command.path)
            files = glob.glob("*.py")
            for file in files:
                filter_file(pattern, repl, *files, backup=False)

    def setup_build_environment(self, env):
        if self.version >= Version('3.4.0'):
            htslib = self.spec['htslib'].prefix
            env.set('HTSLIBDIR', htslib)

    def setup_run_environment(self, env):
        env.set('AUGUSTUS_CONFIG_PATH', join_path(
            self.prefix, 'config'))
        env.prepend_path('PATH', join_path(self.prefix, 'scripts'))
