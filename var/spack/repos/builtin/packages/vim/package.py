# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vim(AutotoolsPackage):
    """Vim is a highly configurable text editor built to enable efficient text
    editing. It is an improved version of the vi editor distributed with most
    UNIX systems.  Vim is often called a "programmer's editor," and so useful
    for programming that many consider it an entire IDE. It's not just for
    programmers, though. Vim is perfect for all kinds of text editing, from
    composing email to editing configuration files.
    """

    homepage = "http://www.vim.org"
    url      = "https://github.com/vim/vim/archive/v8.1.0338.tar.gz"

    version('8.2.1201', sha256='39032fe866f44724b104468038dc9ac4ff2c00a4b18c9a1e2c27064ab1f1143d')
    version('8.1.2141', sha256='7be3c3d88a6c871121230ffb9b7371b1d2ab462118dedb967c7265473af1144b')
    version('8.1.0338', sha256='3febcc4e49eaca458be1a1e8055a3a52887aa2054b03e24d5f38d192c3de51a0')
    version('8.1.0001', sha256='c342acaa26589f371fa34a5ca213b95811f26185c12443f8f48ad2868dee2935')
    version('8.0.1376', sha256='1ad8b5a0b9b63df5abc3f8050e31e1cb49379ffcfd2662a56daeff8bd3d780b9')
    version('8.0.0503', sha256='f2a316a7ae83eccfecf4a700e631094fce9df873358e3d5f112134faa74082ac')
    version('8.0.0454', sha256='e1f683c4a0e3fa56fa02769bbca576e4960850b0ca8640514a7b114b88c27b89')
    version('8.0.0134', sha256='1b3e3e7d187eed55cbdb0a1dae6b8f3b885005fbae84222420877d7afa3b2310')
    version('7.4.2367', sha256='a9ae4031ccd73cc60e771e8bf9b3c8b7f10f63a67efce7f61cd694cd8d7cda5c')

    feature_sets = ('huge', 'big', 'normal', 'small', 'tiny')
    for fs in feature_sets:
        variant(fs, default=False, description="Use '%s' feature set" % fs)

    variant('python', default=False, description="build with Python")
    depends_on('python', when='+python')

    variant('ruby', default=False, description="build with Ruby")
    depends_on('ruby', when='+ruby')

    variant('lua', default=False, description="build with Lua")
    depends_on('lua', when='+lua')

    variant('perl', default=False, description="build with Perl")
    depends_on('perl', when='+perl')

    variant('cscope', default=False, description="build with cscope support")
    depends_on('cscope', when='+cscope', type='run')

    # TODO: Once better support for multi-valued variants is added, add
    # support for auto/no/gtk2/gnome2/gtk3/motif/athena/neXtaw/photon/carbon
    variant('gui', default=False, description="build with gui (gvim)")
    variant('x', default=False, description="use the X Window System")
    depends_on('libx11', when="+x")
    depends_on('libsm', when="+x")
    depends_on('libxpm', when="+x")
    depends_on('libxt', when="+x")
    depends_on('libxtst', when="+x")

    depends_on('ncurses', when="@7.4:")
    depends_on('findutils', type='build')
    depends_on('fontconfig', when="+gui")

    def configure_args(self):
        spec = self.spec
        feature_set = None
        for fs in self.feature_sets:
            if "+" + fs in spec:
                if feature_set is not None:
                    raise InstallError(
                        "Only one feature set allowed, specified %s and %s"
                        % (feature_set, fs))
                feature_set = fs
        if '+gui' in spec:
            if feature_set is not None:
                if feature_set != 'huge':
                    raise InstallError(
                        "+gui variant requires 'huge' feature set, "
                        "%s was specified" % feature_set)
            feature_set = 'huge'
        if feature_set is None:
            feature_set = 'normal'

        configure_args = ["--enable-fail-if-missing"]

        if '+termlib' in spec['ncurses']:
            configure_args.append("--with-tlib=tinfow")
        else:
            configure_args.append("--with-tlib=ncursesw")

        configure_args.append("--with-features=" + feature_set)

        if '+python' in spec:
            if 'python@3:' in self.spec:
                configure_args.append("--enable-python3interp=dynamic")
                configure_args.append("--enable-pythoninterp=no")
            else:
                configure_args.append("--enable-python3interp=no")
                configure_args.append("--enable-pythoninterp=dynamic")
        else:
            configure_args.append("--enable-python3interp=no")

        if '+ruby' in spec:
            configure_args.append("--enable-rubyinterp=yes")
        else:
            configure_args.append("--enable-rubyinterp=no")

        if '+lua' in spec:
            configure_args.append("--enable-luainterp=yes")
            configure_args.append("--with-lua-prefix=%s" % spec['lua'].prefix)
        else:
            configure_args.append("--enable-luainterp=no")

        if '+perl' in spec:
            configure_args.append("--enable-perlinterp=yes")
        else:
            configure_args.append("--enable-perlinterp=no")

        if '+gui' in spec:
            configure_args.append("--enable-gui=auto")
        else:
            configure_args.append("--enable-gui=no")

        if '+x' in spec:
            configure_args.append("--with-x")
        else:
            configure_args.append("--without-x")

        if '+cscope' in spec:
            configure_args.append("--enable-cscope")

        return configure_args

    # Tests must be run in serial
    def check(self):
        make('test', parallel=False)

    # Run the install phase with -j 1.  There seems to be a problem with
    # parallel builds that results in the creation of the links (e.g. view)
    # to the vim binary silently failing.
    def install(self, spec, prefix):
        make('install', parallel=False)
