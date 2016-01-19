from spack import *

class Boost(Package):
    """Boost provides free peer-reviewed portable C++ source
       libraries, emphasizing libraries that work well with the C++
       Standard Library.

       Boost libraries are intended to be widely useful, and usable
       across a broad spectrum of applications. The Boost license
       encourages both commercial and non-commercial use.
    """
    homepage = "http://www.boost.org"
    url      = "http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2"
    list_url = "http://sourceforge.net/projects/boost/files/boost/"
    list_depth = 2

    version('1.60.0', '65a840e1a0b13a558ff19eeb2c4f0cbe')
    version('1.59.0', '6aa9a5c6a4ca1016edd0ed1178e3cb87')
    version('1.58.0', 'b8839650e61e9c1c0a89f371dd475546')
    version('1.57.0', '1be49befbdd9a5ce9def2983ba3e7b76')
    version('1.56.0', 'a744cf167b05d72335f27c88115f211d')
    version('1.55.0', 'd6eef4b4cacb2183f2bf265a5a03a354')
    version('1.54.0', '15cb8c0803064faef0c4ddf5bc5ca279')
    version('1.53.0', 'a00d22605d5dbcfb4c9936a9b35bc4c2')
    version('1.52.0', '3a855e0f919107e0ca4de4d84ad3f750')
    version('1.51.0', '4b6bd483b692fd138aef84ed2c8eb679')
    version('1.50.0', '52dd00be775e689f55a987baebccc462')
    version('1.49.0', '0d202cb811f934282dea64856a175698')
    version('1.48.0', 'd1e9a7a7f532bb031a3c175d86688d95')
    version('1.47.0', 'a2dc343f7bc7f83f8941e47ed4a18200')
    version('1.46.1', '7375679575f4c8db605d426fc721d506')
    version('1.46.0', '37b12f1702319b73876b0097982087e0')
    version('1.45.0', 'd405c606354789d0426bc07bea617e58')
    version('1.44.0', 'f02578f5218f217a9f20e9c30e119c6a')
    version('1.43.0', 'dd49767bfb726b0c774f7db0cef91ed1')
    version('1.42.0', '7bf3b4eb841b62ffb0ade2b82218ebe6')
    version('1.41.0', '8bb65e133907db727a2a825c5400d0a6')
    version('1.40.0', 'ec3875caeac8c52c7c129802a8483bd7')
    version('1.39.0', 'a17281fd88c48e0d866e1a12deecbcc0')
    version('1.38.0', '5eca2116d39d61382b8f8235915cb267')
    version('1.37.0', '8d9f990bfb7e83769fa5f1d6f065bc92')
    version('1.36.0', '328bfec66c312150e4c2a78dcecb504b')
    version('1.35.0', 'dce952a7214e72d6597516bcac84048b')
    version('1.34.1', '2d938467e8a448a2c9763e0a9f8ca7e5')
    version('1.34.0', 'ed5b9291ffad776f8757a916e1726ad0')

    variant('debug', default=False, description='Switch to the debug version of Boost')
    variant('python', default=False, description='Activate the component Boost.Python')
    variant('mpi', default=False, description='Activate the component Boost.MPI')
    variant('compression', default=True, description='Activate the compression Boost.iostreams')

    depends_on('python', when='+python')
    depends_on('mpi', when='+mpi')
    depends_on('bzip2', when='+compression')
    depends_on('zlib', when='+compression')

    def url_for_version(self, version):
        """Handle Boost's weird URLs, which write the version two different ways."""
        parts = [str(p) for p in Version(version)]
        dots = ".".join(parts)
        underscores = "_".join(parts)
        return "http://downloads.sourceforge.net/project/boost/boost/%s/boost_%s.tar.bz2" % (
            dots, underscores)

    def determine_toolset(self, spec):
        if spec.satisfies("=darwin-x86_64"):
            return 'darwin'

        toolsets = {'g++': 'gcc',
                    'icpc': 'intel',
                    'clang++': 'clang'}

        for cc, toolset in toolsets.iteritems():
            if cc in self.compiler.cxx_names:
                return toolset

        # fallback to gcc if no toolset found
        return 'gcc'

    def determine_bootstrap_options(self, spec, options):
        options.append('--with-toolset=%s' % self.determine_toolset(spec))

        without_libs = []
        if '~mpi' in spec:
            without_libs.append('mpi')
        if '~python' in spec:
            without_libs.append('python')
        else:
            options.append('--with-python=%s' %
                join_path(spec['python'].prefix.bin, 'python'))

        if without_libs:
            options.append('--without-libraries=%s' % ','.join(without_libs))

        with open('user-config.jam', 'w') as f:
            if '+mpi' in spec:
                f.write('using mpi : %s ;\n' %
                    join_path(spec['mpi'].prefix.bin, 'mpicxx'))
            if '+python' in spec:
                f.write('using python : %s : %s ;\n' %
                    (spec['python'].version,
                    join_path(spec['python'].prefix.bin, 'python')))

    def determine_b2_options(self, spec, options):
        if '+debug' in spec:
            options.append('variant=debug')
        else:
            options.append('variant=release')

        if '~compression' in spec:
            options.extend([
                '-s', 'NO_BZIP2=1',
                '-s', 'NO_ZLIB=1'])

        if '+compression' in spec:
            options.extend([
                '-s', 'BZIP2_INCLUDE=%s' % spec['bzip2'].prefix.include,
                '-s', 'BZIP2_LIBPATH=%s' % spec['bzip2'].prefix.lib,
                '-s', 'ZLIB_INCLUDE=%s' % spec['zlib'].prefix.include,
                '-s', 'ZLIB_LIBPATH=%s' % spec['zlib'].prefix.lib,
                ])

        options.extend([
            'toolset=%s' % self.determine_toolset(spec),
            'link=static,shared',
            'threading=single,multi',
            '--layout=tagged'])

    def install(self, spec, prefix):
        # to make Boost find the user-config.jam
        env['BOOST_BUILD_PATH'] = './'

        bootstrap = Executable('./bootstrap.sh')

        bootstrap_options = ['--prefix=%s' % prefix]
        self.determine_bootstrap_options(spec, bootstrap_options)

        bootstrap(*bootstrap_options)

        # b2 used to be called bjam, before 1.47 (sigh)
        b2name = './b2' if spec.satisfies('@1.47:') else './bjam'

        b2 = Executable(b2name)
        b2_options = ['-j', '%s' % make_jobs]

        self.determine_b2_options(spec, b2_options)

        b2('install', *b2_options)
