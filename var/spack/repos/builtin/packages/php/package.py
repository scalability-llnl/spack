# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.hooks.sbang as sbang
from spack.package import *


class Php(AutotoolsPackage):
    """
    PHP is a popular general-purpose scripting language that is especially
    suited to web development. Fast, flexible and pragmatic, PHP powers
    everything from your blog to the most popular websites in the world.
    """

    homepage = "https://php.net/"
    url = "https://github.com/php/php-src/archive/php-7.3.13.tar.gz"

    license("PHP-3.01")

    version("8.3.12", sha256="d5d4e6ffc6d6b2f02a87c45741623e08045ec6509ade44a1033e0f8bbb374119")
    version("7.4.33", sha256="dfbb2111160589054768a37086bda650a0041c89878449d078684d70d6a0e411")
    with default_args(deprecated=True):
        version("7.4.1", sha256="4d9d7c5681bec3af38a935d033657dce09a9913498f8022d7ca163a7f2f493a7")
        version("7.4.0", sha256="91d34b48025ab9789216df89e247b6904912eeeaeff38c300ef314bdda8920b0")
        version(
            "7.3.13", sha256="e68b8d9e659f2993eee912f05860e546fdc18e459f31cd2771f404df21285f0b"
        )
        version(
            "7.3.12", sha256="d0672ea84c0ab184f636acff3230d376d89a2067d59a87a2f1842361ee1f97d6"
        )
        version(
            "7.3.11", sha256="4d861b2f3bc640ded8b591ce87250161392a6244a3c84042da0c06fd8c500eb2"
        )
        version(
            "7.2.26", sha256="da132a836cec8021c00f22952e6044d91628ee3d2ef92a95d65cf91bad810600"
        )
        version(
            "7.2.25", sha256="049b2d291c45cb889d15fcd2bac6da7d15ca5d535d272d2f8879fb834bbf276e"
        )
        version(
            "7.2.24", sha256="334c9915733f6a29e1462f64038b1b4b1b21cb18f4f5f980add86792b5550ab3"
        )
        version(
            "7.1.33", sha256="f80a795a09328a9441bae4a8a60fa0d6d43ec5adc98f5aa5f51d06f4522c07fe"
        )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("bison", type="build")
    depends_on("re2c", type="build")
    depends_on("bash", type="build")
    depends_on("libiconv", when="@8:")
    depends_on("libxml2")
    depends_on("sqlite")

    patch("sbang-7.patch", when="@7")
    patch("sbang-8.patch", when="@8")

    def patch(self):
        """
        phar sbang is added before build phase.
        Because phar is php script with binary data
        (Not UTF-8 text file) And phar is embeded own sha1 checksum.
        """
        shebang_limit = 127

        if len(self.prefix.bin.php) + 2 <= shebang_limit:
            return

        new_sbang_line = "#!/bin/bash %s" % sbang.sbang_install_path()
        original_bang = '-b "$(PHP_PHARCMD_BANG)"'
        makefile = join_path("ext", "phar", "Makefile.frag")
        filter_file(
            original_bang,
            original_bang + ' -z "{0}"'.format(new_sbang_line),
            makefile,
            string=True,
        )

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./buildconf", "--force")

    @when("@8:")
    def configure_args(self):
        args = [f"--with-iconv={self.spec['libiconv'].prefix}"]
        return args
