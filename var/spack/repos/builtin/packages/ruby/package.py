# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import spack.build_systems.autotools
import spack.build_systems.nmake
from spack.package import *


class Ruby(AutotoolsPackage, NMakePackage):
    """A dynamic, open source programming language with a focus on
    simplicity and productivity.
    """

    maintainers("Kerilk")

    homepage = "https://www.ruby-lang.org/"
    url = "https://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz"
    list_url = "https://cache.ruby-lang.org/pub/ruby/"
    list_depth = 1
    tags = ["windows"]

    license("Ruby AND BSD-2-Clause AND MIT", checked_by="tgamblin")

    version("3.3.5", sha256="3781a3504222c2f26cb4b9eb9c1a12dbf4944d366ce24a9ff8cf99ecbce75196")
    version("3.3.4", sha256="fe6a30f97d54e029768f2ddf4923699c416cdbc3a6e96db3e2d5716c7db96a34")
    version("3.3.2", sha256="3be1d100ebf2a0ce60c2cd8d22cd9db4d64b3e04a1943be2c4ff7b520f2bcb5b")
    version("3.3.0", sha256="96518814d9832bece92a85415a819d4893b307db5921ae1f0f751a9a89a56b7d")
    version("3.1.0", sha256="50a0504c6edcb4d61ce6b8cfdbddaa95707195fab0ecd7b5e92654b2a9412854")
    version("3.0.2", sha256="5085dee0ad9f06996a8acec7ebea4a8735e6fac22f22e2d98c3f2bc3bef7e6f1")
    version("3.0.1", sha256="369825db2199f6aeef16b408df6a04ebaddb664fb9af0ec8c686b0ce7ab77727")
    version("3.0.0", sha256="a13ed141a1c18eb967aac1e33f4d6ad5f21be1ac543c344e0d6feeee54af8e28")
    version("2.7.2", sha256="6e5706d0d4ee4e1e2f883db9d768586b4d06567debea353c796ec45e8321c3d4")
    version("2.7.1", sha256="d418483bdd0000576c1370571121a6eb24582116db0b7bb2005e90e250eae418")
    version("2.6.2", sha256="a0405d2bf2c2d2f332033b70dff354d224a864ab0edd462b7a413420453b49ab")
    version("2.5.3", sha256="9828d03852c37c20fa333a0264f2490f07338576734d910ee3fd538c9520846c")
    version("2.2.0", sha256="7671e394abfb5d262fbcd3b27a71bf78737c7e9347fa21c39e58b0bb9c4840fc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system("autotools", "nmake", default="autotools")

    for _platform_condition in ("platform=linux", "platform=darwin"):
        with when(_platform_condition):
            variant("openssl", default=True, description="Enable OpenSSL support")
            variant("readline", default=False, description="Enable Readline support")
            variant("yjit", default=False, description="Enable Rust JIT", when="@3.2:")
            depends_on("pkgconfig", type="build")
            depends_on("libffi")
            depends_on("libx11", when="@:2.3")
            depends_on("tcl", when="@:2.3")
            depends_on("tk", when="@:2.3")
            depends_on("readline", when="+readline")
            depends_on("zlib-api")
            depends_on("libyaml", when="@3:")
            with when("+openssl"):
                depends_on("openssl@:1")
                depends_on("openssl@:1.0", when="@:2.3")
            with when("+yjit"):
                depends_on("rust@1.58:")

    extendable = True

    # Known build issues when Avira antivirus software is running:
    # https://github.com/rvm/rvm/issues/4313#issuecomment-374020379
    # TODO: add check for this and warn user

    # gcc-7-based build requires patches (cf. https://bugs.ruby-lang.org/issues/13150)
    patch("ruby_23_gcc7.patch", level=0, when="@2.2.0:2.2 %gcc@7:")
    patch("ruby_23_gcc7.patch", level=0, when="@2.3.0:2.3.4 %gcc@7:")
    patch("ruby_24_gcc7.patch", level=1, when="@2.4.0 %gcc@7:")

    resource(
        name="rubygems-updated-ssl-cert",
        url="https://raw.githubusercontent.com/rubygems/rubygems/master/lib/rubygems/ssl_certs/index.rubygems.org/GlobalSignRootCA.pem",
        sha256="df68841998b7fd098a9517fe971e97890be0fc93bbe1b2a1ef63ebdea3111c80",
        when="+openssl",
        destination="",
        placement="rubygems-updated-ssl-cert",
        expand=False,
    )

    executables = ["^ruby$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"ruby ([\d.]+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        url = "https://cache.ruby-lang.org/pub/ruby/{0}/ruby-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def setup_dependent_run_environment(self, env, dependent_spec):
        if dependent_spec.package.extends(self.spec):
            env.prepend_path("GEM_PATH", dependent_spec.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before ruby modules' install() methods.  Sets GEM_HOME
        and GEM_PATH to values appropriate for the package being built.

        In most cases, extensions will only need to have one line::

            gem('install', '<gem-name>.gem')
        """
        # Ruby extension builds have global ruby and gem functions
        module.ruby = Executable(self.prefix.bin.ruby)
        module.gem = Executable(self.prefix.bin.gem)
        module.rake = Executable(self.prefix.bin.rake)


class SetupEnvironment:
    def setup_dependent_build_environment(self, env, dependent_spec):
        # TODO: do this only for actual extensions.
        # Set GEM_PATH to include dependent gem directories
        for d in dependent_spec.traverse(deptype=("build", "run", "test"), root=True):
            if d.package.extends(self.spec):
                env.prepend_path("GEM_PATH", d.prefix)

        # The actual installation path for this gem
        env.set("GEM_HOME", dependent_spec.prefix)


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder, SetupEnvironment):
    def configure_args(self):
        args = []
        if "+openssl" in self.spec:
            args.append("--with-openssl-dir=%s" % self.spec["openssl"].prefix)
        if "+readline" in self.spec:
            args.append("--with-readline-dir=%s" % self.spec["readline"].prefix)
        if "^tk" in self.spec:
            args.append("--with-tk=%s" % self.spec["tk"].prefix)
        if self.spec.satisfies("%fj"):
            args.append("--disable-dtrace")
        args.extend(self.enable_or_disable("yjit"))
        return args

    @run_after("install")
    def post_install(self):
        """RubyGems updated their SSL certificates at some point, so
        new certificates must be installed after Ruby is installed
        in order to download gems; see
        https://guides.rubygems.org/ssl-certificate-update/
        for details.
        """
        if self.spec.satisfies("+openssl"):
            rubygems_updated_cert_path = join_path(
                self.pkg.stage.source_path, "rubygems-updated-ssl-cert", "GlobalSignRootCA.pem"
            )
            rubygems_certs_path = join_path(
                self.spec.prefix.lib,
                "ruby",
                "{0}.0".format(self.spec.version.up_to(2)),
                "rubygems",
                "ssl_certs",
            )
            install(rubygems_updated_cert_path, rubygems_certs_path)

        rbconfig = find(self.prefix, "rbconfig.rb")[0]
        filter_file(
            r'^(\s*CONFIG\["CXX"\]\s*=\s*).*', r'\1"{0}"'.format(self.pkg.compiler.cxx), rbconfig
        )
        filter_file(
            r'^(\s*CONFIG\["CC"\]\s*=\s*).*', r'\1"{0}"'.format(self.pkg.compiler.cc), rbconfig
        )
        filter_file(
            r'^(\s*CONFIG\["MJIT_CC"\]\s*=\s*).*',
            r'\1"{0}"'.format(self.pkg.compiler.cc),
            rbconfig,
        )


class NMakeBuilder(spack.build_systems.nmake.NMakeBuilder, SetupEnvironment):
    def edit(self, pkg, spec, prefix):
        with working_dir(self.pkg.stage.source_path, create=True):
            Executable("win32\\configure.bat")("--prefix=%s" % self.prefix)
