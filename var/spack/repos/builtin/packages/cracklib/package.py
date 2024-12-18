# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cracklib(AutotoolsPackage):
    """CrackLib tests passwords to determine whether they match certain
    security-oriented characteristics, with the purpose of stopping users
    from choosing passwords that are easy to guess."""

    homepage = "https://github.com/cracklib/cracklib"
    url = "https://github.com/cracklib/cracklib/archive/v2.9.7.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.9.11", sha256="23837f80d65bf67e2679cd246d810c8851630860f27620205b957b3b5f88ee88")
    version("2.9.9", sha256="0a3fd72163512088c6f2add0f6cd6e34954ca0fa3f333ff9cced478b04e73ce1")
    version("2.9.7", sha256="ff4e6c3f86494c93719f5e4186e2c3ea9e265f41972ec21f7b87852aced704e6")
    version("2.9.6", sha256="7cd2c01365f199c466b490ad2585beccbe0108ccd606c1bcc6c1e52800e627fe")
    version("2.9.5", sha256="b3fcf3fba2f4566f8eb2b79502d1a66198a71c557d2ab1011c78001489f0fe26")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "run"))
    depends_on("gettext")
    depends_on("fmt")
    depends_on("zlib-api")

    configure_directory = "src"

    def autoreconf(self, spec, prefix):
        with working_dir("src"):
            sh = which("sh")
            sh("./autogen.sh")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
