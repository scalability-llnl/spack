# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tempfile

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Mysql(CMakePackage):
    """MySQL is an open source relational database management system."""

    homepage = "https://www.mysql.com/"
    url = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.15.tar.gz"

    version("8.0.35", sha256="917c5ed38704e99211185ce4be24e33a8c19c91241ed73af4181a6f38d1574c2")
    version("8.0.29", sha256="512170fa6f78a694d6f18d197e999d2716ee68dc541d7644dd922a3663407266")
    version("8.0.19", sha256="a62786d67b5e267eef928003967b4ccfe362d604b80f4523578e0688f5b9f834")
    version("8.0.18", sha256="4cb39a315298eb243c25c53c184b3682b49c2a907a1d8432ba0620534806ade8")
    version("8.0.17", sha256="c6e3f38199a77bfd8a4925ca00b252d3b6159b90e4980c7232f1c58d6ca759d6")
    version("8.0.16", sha256="8d9fe89920dc8bbbde2857b7b877ad2fa5ec2f231c68e941d484f3b72735eaea")
    version("8.0.15", sha256="bb1bca2dc2f23ee9dd395cc4db93b64561d4ac20b53be5d1dae563f7be64825e")
    version("8.0.14", sha256="bc53f4c914fb39650289700d144529121d71f38399d2d24a0f5c76e5a8abd204")
    version("8.0.13", sha256="d85eb7f98b6aa3e2c6fe38263bf40b22acb444a4ce1f4668473e9e59fb98d62e")
    version("8.0.12", sha256="69f16e20834dbc60cb28d6df7351deda323330b9de685d22415f135bcedd1b20")
    version("8.0.11", sha256="3bde3e30d5d4afcedfc6db9eed5c984237ac7db9480a9cc3bddc026d50700bf9")
    version("5.7.27", sha256="f8b65872a358d6f5957de86715c0a3ef733b60451dad8d64a8fd1a92bf091bba")
    version("5.7.26", sha256="5f01d579a20199e06fcbc28f0801c3cb545a54a2863ed8634f17fe526480b9f1")
    version("5.7.25", sha256="53751c6243806103114567c1a8b6a3ec27f23c0e132f377a13ce1eb56c63723f")
    version("5.7.24", sha256="05bf0c92c6a97cf85b67fff1ac83ca7b3467aea2bf306374d727fa4f18431f87")
    version("5.7.23", sha256="0730f2d5520bfac359e9272da6c989d0006682eacfdc086a139886c0741f6c65")
    version("5.7.22", sha256="4eb8405b0a9acb0381eae94c1741b2850dfc6467742b24b676e62b566409cff2")
    version("5.7.21", sha256="fa205079c27a39c24f3485e7498dd0906a6e0b379b4f99ebc0ec38a9ec5b09b7")
    version("5.7.20", sha256="5397549bb7c238f396c123db2df4cad2191b11adf8986de7fe63bff8e2786487")
    version("5.7.19", sha256="3e51e76f93179ca7b165a7008a6cc14d56195b3aef35d26d3ac194333d291eb1")
    version("5.7.18", sha256="0b5d71ed608656cd8181d3bb0434d3e36bac192899038dbdddf5a7594aaea1a2")
    version("5.7.17", sha256="cebf23e858aee11e354c57d30de7a079754bdc2ef85eb684782458332a4b9651")
    version("5.7.16", sha256="4935b59974edb275629f6724a0fcf72265a5845faf1e30eeb50ed4b6528318a5")
    version("5.7.15", sha256="9085353143bfda59c90aa959e79a35622a22aa592e710993416e193b37eb9956")
    version("5.7.14", sha256="f7415bdac2ca8bbccd77d4f22d8a0bdd7280b065bd646a71a506b77c7a8bd169")
    version("5.7.13", sha256="50bf1a1635a61235fc43fd4876df2f77163de109372679e29c1ff8dbc38a0b87")
    version("5.7.12", sha256="32843cb6d22ab22cd2340262b53c0d6009b5bd41b1fa4102beda19635a5c1c87")
    version("5.7.11", sha256="54f8c7af87d3d8084419bde2b9f0d8970b3dada0757b015981b02f35a3681f0e")
    version("5.7.10", sha256="1ea1644884d086a23eafd8ccb04d517fbd43da3a6a06036f23c5c3a111e25c74")
    version("5.7.9", sha256="315342f5bee1179548cecad2d776cd7758092fd2854024e60a3a5007feba34e0")
    version("5.6.44", sha256="c031c92c3f226856b09bf929d8a26b0cd8600036cb9db4e0fdf6b6f032ced336")
    version("5.6.43", sha256="1c95800bf0e1b7a19a37d37fbc5023af85c6bc0b41532433b3a886263a1673ef")
    version("5.5.62", sha256="b1e7853bc1f04aabf6771e0ad947f35ac8d237f4b35d0706d1095c9526ff99d7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("client_only", default=False, description="Build and install client only.")
    variant(
        "cxxstd",
        default="17",
        values=("98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # 5.7.X cannot be compiled client-only.
    conflicts("+client_only", when="@5.7.0:5.7")
    # Server code has a macro 'byte', which conflicts with C++17's
    # std::byte.
    conflicts("cxxstd=17", when="@8.0.0:~client_only")

    provides("mysql-client")

    # https://dev.mysql.com/doc/refman/8.0/en/source-installation.html
    # https://dev.mysql.com/doc/refman/8.0/en/source-configuration-options.html

    # See CMAKE_MINIMUM_REQUIRED in CMakeLists.txt
    depends_on("cmake@3.1.0:", type="build", when="@5.7.0:5.7 platform=win32")
    depends_on("cmake@3.8.0:", type="build", when="@8.0.0: platform=win32")
    depends_on("cmake@3.9.2:", type="build", when="@8.0.0: platform=darwin")
    depends_on("cmake@3.4.0:", type="build", when="@8.0.0: platform=solaris")
    depends_on("cmake@2.6:", type="build", when="@:5.6")
    depends_on("cmake@2.8.9:", type="build", when="@5.7.0:5.7")
    depends_on("cmake@2.8.12:", type="build", when="@8.0.0:")

    depends_on("gmake@3.75:", type="build")
    depends_on("pkgconfig", type="build", when="@5.7.0:")
    depends_on("doxygen", type="build", when="@8.0.0:")

    # Each version of MySQL requires a specific version of boost
    # See BOOST_PACKAGE_NAME in cmake/boost.cmake
    # 8.0.35
    depends_on("boost@1.77.0 cxxstd=17", type="build", when="@8.0.35 cxxstd=17")
    # 8.0.29
    depends_on("boost@1.77.0 cxxstd=98", type="build", when="@8.0.29 cxxstd=98")
    depends_on("boost@1.77.0 cxxstd=11", type="build", when="@8.0.29 cxxstd=11")
    depends_on("boost@1.77.0 cxxstd=14", type="build", when="@8.0.29 cxxstd=14")
    depends_on("boost@1.77.0 cxxstd=17", type="build", when="@8.0.29 cxxstd=17")
    # 8.0.19
    depends_on("boost@1.70.0 cxxstd=98", type="build", when="@8.0.19 cxxstd=98")
    depends_on("boost@1.70.0 cxxstd=11", type="build", when="@8.0.19 cxxstd=11")
    depends_on("boost@1.70.0 cxxstd=14", type="build", when="@8.0.19 cxxstd=14")
    depends_on("boost@1.70.0 cxxstd=17", type="build", when="@8.0.19 cxxstd=17")
    # 8.0.16--8.0.18
    depends_on("boost@1.69.0 cxxstd=98", type="build", when="@8.0.16:8.0.18 cxxstd=98")
    depends_on("boost@1.69.0 cxxstd=11", type="build", when="@8.0.16:8.0.18 cxxstd=11")
    depends_on("boost@1.69.0 cxxstd=14", type="build", when="@8.0.16:8.0.18 cxxstd=14")
    depends_on("boost@1.69.0 cxxstd=17", type="build", when="@8.0.16:8.0.18 cxxstd=17")
    # 8.0.14--8.0.15
    depends_on("boost@1.68.0 cxxstd=98", type="build", when="@8.0.14:8.0.15 cxxstd=98")
    depends_on("boost@1.68.0 cxxstd=11", type="build", when="@8.0.14:8.0.15 cxxstd=11")
    depends_on("boost@1.68.0 cxxstd=14", type="build", when="@8.0.14:8.0.15 cxxstd=14")
    depends_on("boost@1.68.0 cxxstd=17", type="build", when="@8.0.14:8.0.15 cxxstd=17")
    # 8.0.12--8.0.13
    depends_on("boost@1.67.0 cxxstd=98", type="build", when="@8.0.12:8.0.13 cxxstd=98")
    depends_on("boost@1.67.0 cxxstd=11", type="build", when="@8.0.12:8.0.13 cxxstd=11")
    depends_on("boost@1.67.0 cxxstd=14", type="build", when="@8.0.12:8.0.13 cxxstd=14")
    depends_on("boost@1.67.0 cxxstd=17", type="build", when="@8.0.12:8.0.13 cxxstd=17")
    # 8.0.11
    depends_on("boost@1.66.0 cxxstd=98", type="build", when="@8.0.11 cxxstd=98")
    depends_on("boost@1.66.0 cxxstd=11", type="build", when="@8.0.11 cxxstd=11")
    depends_on("boost@1.66.0 cxxstd=14", type="build", when="@8.0.11 cxxstd=14")
    depends_on("boost@1.66.0 cxxstd=17", type="build", when="@8.0.11 cxxstd=17")
    # 5.7.X
    depends_on("boost@1.59.0 cxxstd=98", when="@5.7.0:5.7 cxxstd=98")
    depends_on("boost@1.59.0 cxxstd=11", when="@5.7.0:5.7 cxxstd=11")
    depends_on("boost@1.59.0 cxxstd=14", when="@5.7.0:5.7 cxxstd=14")
    depends_on("boost@1.59.0 cxxstd=17", when="@5.7.0:5.7 cxxstd=17")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@5.7:")

    with when("@8.0.35:"):
        depends_on("openssl@3:")
        requires("cxxstd=17")

    depends_on("zstd", when="@8.0.18:")

    depends_on("patchelf", type="build")
    depends_on("curl")
    depends_on("zlib-api")
    depends_on("libevent")
    depends_on("lz4")

    depends_on("rpcsvc-proto")
    depends_on("ncurses")
    depends_on("openssl@:2", when="@:8.0.29")
    depends_on("libtirpc", when="@5.7.0: platform=linux")
    depends_on("libedit", type=["build", "run"])
    depends_on("perl", type=["build", "test"], when="@:7")
    depends_on("bison@2.1:", type="build")
    depends_on("m4", type="build", when="@develop platform=solaris")
    depends_on("cyrus-sasl", when="@:5.7")

    patch("fix-no-server-5.5.patch", level=1, when="@5.5.0:5.5")

    @property
    def command(self):
        return Executable(self.prefix.bin.mysql_config)

    @property
    def libs(self):
        return find_libraries("libmysqlclient", root=self.prefix, recursive=True)

    def url_for_version(self, version):
        url = "https://dev.mysql.com/get/Downloads/MySQL-{0}/mysql-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def cmake_args(self):
        spec = self.spec
        options = [
            self.define("REPRODUCIBLE_BUILD", True),
            self.define("WITH_CURL", spec["curl"].prefix),
            self.define("WITH_EDITLINE", "system"),
            self.define("WITH_LIBEVENT", "system"),
            self.define("WITH_LZ4", "system"),
            self.define("WITH_SSL", spec["openssl"].prefix),
            self.define("WITH_ZLIB", "system"),
            self.define_from_variant("WITHOUT_SERVER", "client_only"),
        ]

        if spec.satisfies("@5.7:"):
            options.extend(
                [
                    self.define("WITH_BOOST", spec["boost"].prefix),
                    self.define("LOCAL_BOOST_DIR", spec["boost"].prefix),
                ]
            )

        if spec.satisfies("@8.0.18:"):
            options.extend([self.define("WITH_ZSTD", "system")])

        return options

    def _fix_dtrace_shebang(self, env):
        # dtrace may cause build to fail because it uses
        # '/usr/bin/python' in the shebang. To work around that we copy
        # the original script into a temporary folder, and change the
        # shebang to '/usr/bin/env python'. Treatment adapted from that
        # used in glib recipe per M. Culpo @b2822b258.
        dtrace = which("dtrace").path
        dtrace_copy_path = os.path.join(tempfile.mkdtemp(), "dtrace-copy")
        dtrace_copy = os.path.join(dtrace_copy_path, "dtrace")
        mkdirp(dtrace_copy_path)
        copy(dtrace, dtrace_copy)
        filter_file(
            "^#!/usr/bin/python",
            "#!/usr/bin/env {0}".format(os.path.basename(str(self.spec["python"].command))),
            dtrace_copy,
        )
        # To have our own copy of dtrace in PATH, we need to
        # prepend to PATH the temporary folder where it resides.
        env.prepend_path("PATH", dtrace_copy_path)

    def setup_build_environment(self, env):
        cxxstd = self.spec.variants["cxxstd"].value
        flag = getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        if flag:
            env.append_flags("CXXFLAGS", flag)
        if cxxstd != "98":
            if int(cxxstd) > 11:
                env.append_flags("CXXFLAGS", "-Wno-deprecated-declarations")
            if int(cxxstd) > 14:
                env.append_flags("CXXFLAGS", "-Wno-error=register")

        if "python" in self.spec and self.spec.satisfies("@:7"):
            self._fix_dtrace_shebang(env)

    @run_before("install")
    def fixup_mysqlconfig(self):
        if not self.spec.satisfies("platform=windows"):
            # mysql uses spack libz but exports -lzlib to its dependencies. Fix that:
            with working_dir(self.build_directory):
                for config in ("scripts/mysql_config", "scripts/mysqlclient.pc"):
                    if os.path.exists(config):
                        filter_file(" -lzlib ", " -lz ", config)
