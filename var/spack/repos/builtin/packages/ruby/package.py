# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re


class Ruby(AutotoolsPackage):
    """A dynamic, open source programming language with a focus on
    simplicity and productivity."""

    homepage = "https://www.ruby-lang.org/"
    url      = "http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz"
    list_url = "http://cache.ruby-lang.org/pub/ruby/"
    list_depth = 1

    version('3.0.0', sha256='a13ed141a1c18eb967aac1e33f4d6ad5f21be1ac543c344e0d6feeee54af8e28')
    version('2.7.2', sha256='6e5706d0d4ee4e1e2f883db9d768586b4d06567debea353c796ec45e8321c3d4')
    version('2.7.1', sha256='d418483bdd0000576c1370571121a6eb24582116db0b7bb2005e90e250eae418')
    version('2.6.2', sha256='a0405d2bf2c2d2f332033b70dff354d224a864ab0edd462b7a413420453b49ab')
    version('2.5.3', sha256='9828d03852c37c20fa333a0264f2490f07338576734d910ee3fd538c9520846c')
    version('2.2.0', sha256='7671e394abfb5d262fbcd3b27a71bf78737c7e9347fa21c39e58b0bb9c4840fc')

    variant('openssl', default=True, description="Enable OpenSSL support")
    variant('readline', default=False, description="Enable Readline support")

    extendable = True

    depends_on('pkgconfig', type=('build'))
    depends_on('libffi')
    depends_on('zlib')
    depends_on('libx11', when='@:2.3')
    depends_on('tcl', when='@:2.3')
    depends_on('tk', when='@:2.3')
    depends_on('openssl@:1.0', when='@:2.3+openssl')
    depends_on('openssl', when='+openssl')
    depends_on('readline', when='+readline')

    # Known build issues when Avira antivirus software is running:
    # https://github.com/rvm/rvm/issues/4313#issuecomment-374020379
    # TODO: add check for this and warn user

    # gcc-7-based build requires patches (cf. https://bugs.ruby-lang.org/issues/13150)
    patch('ruby_23_gcc7.patch', level=0, when='@2.2.0:2.2.999 %gcc@7:')
    patch('ruby_23_gcc7.patch', level=0, when='@2.3.0:2.3.4 %gcc@7:')
    patch('ruby_24_gcc7.patch', level=1, when='@2.4.0 %gcc@7:')

    resource(
        name='rubygems-updated-ssl-cert',
        url='https://raw.githubusercontent.com/rubygems/rubygems/master/lib/rubygems/ssl_certs/index.rubygems.org/GlobalSignRootCA.pem',
        sha256='df68841998b7fd098a9517fe971e97890be0fc93bbe1b2a1ef63ebdea3111c80',
        when='+openssl',
        destination='',
        placement='rubygems-updated-ssl-cert',
        expand=False
    )

    executables = ['^ruby$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'ruby ([\d.]+)', output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        url = "http://cache.ruby-lang.org/pub/ruby/{0}/ruby-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        args = []
        if '+openssl' in self.spec:
            args.append("--with-openssl-dir=%s" % self.spec['openssl'].prefix)
        if '+readline' in self.spec:
            args.append("--with-readline-dir=%s"
                        % self.spec['readline'].prefix)
        if '^tk' in self.spec:
            args.append('--with-tk=%s' % self.spec['tk'].prefix)
        if self.spec.satisfies("%fj"):
            args.append('--disable-dtrace')
        return args

    def setup_dependent_build_environment(self, env, dependent_spec):
        # TODO: do this only for actual extensions.
        # Set GEM_PATH to include dependent gem directories
        ruby_paths = []
        for d in dependent_spec.traverse():
            if d.package.extends(self.spec):
                ruby_paths.append(d.prefix)

        env.set_path('GEM_PATH', ruby_paths)

        # The actual installation path for this gem
        env.set('GEM_HOME', dependent_spec.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before ruby modules' install() methods.  Sets GEM_HOME
        and GEM_PATH to values appropriate for the package being built.

        In most cases, extensions will only need to have one line::

            gem('install', '<gem-name>.gem')
        """
        # Ruby extension builds have global ruby and gem functions
        module.ruby = Executable(self.prefix.bin.ruby)
        module.gem  = Executable(self.prefix.bin.gem)
        module.rake = Executable(self.prefix.bin.rake)

    @run_after('install')
    def post_install(self):
        """ RubyGems updated their SSL certificates at some point, so
        new certificates must be installed after Ruby is installed
        in order to download gems; see
        http://guides.rubygems.org/ssl-certificate-update/
        for details.
        """
        if self.spec.satisfies("+openssl"):
            rubygems_updated_cert_path = join_path(self.stage.source_path,
                                                   'rubygems-updated-ssl-cert',
                                                   'GlobalSignRootCA.pem')
            rubygems_certs_path = join_path(self.spec.prefix.lib,
                                            'ruby',
                                            '{0}.0'.format(self.spec.version.
                                                           up_to(2)),
                                            'rubygems',
                                            'ssl_certs')
            install(rubygems_updated_cert_path, rubygems_certs_path)

        rbconfig = find(self.prefix, 'rbconfig.rb')[0]
        filter_file(r'^(\s*CONFIG\["CXX"\]\s*=\s*).*',
                    r'\1"{0}"'.format(self.compiler.cxx),
                    rbconfig)
        filter_file(r'^(\s*CONFIG\["CC"\]\s*=\s*).*',
                    r'\1"{0}"'.format(self.compiler.cc),
                    rbconfig)
        filter_file(r'^(\s*CONFIG\["MJIT_CC"\]\s*=\s*).*',
                    r'\1"{0}"'.format(self.compiler.cc),
                    rbconfig)
