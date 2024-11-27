# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cryptsetup(AutotoolsPackage):
    """Cryptsetup and LUKS - open-source disk encryption."""

    homepage = "https://gitlab.com/cryptsetup/cryptsetup"
    url = "https://www.kernel.org/pub/linux/utils/cryptsetup/v2.2/cryptsetup-2.2.1.tar.xz"
    list_url = "https://www.kernel.org/pub/linux/utils/cryptsetup/"
    list_depth = 1

    # If you're adding newer versions, check whether the patch below
    # still needs to be applied.
    version("2.3.5", sha256="ced9946f444d132536daf92fc8aca4277638a3c2d96e20540b2bae4d36fd70c1")
    version("2.3.4", sha256="9d16eebb96b53b514778e813019b8dd15fea9fec5aafde9fae5febf59df83773")
    version("2.3.1", sha256="92aba4d559a2cf7043faed92e0f22c5addea36bd63f8c039ba5a8f3a159fe7d2")
    version("2.2.3", sha256="2af0ec9551ab9c870074cae9d3f68d82cab004f4095fa89db0e4413713424a46")
    version("2.2.2", sha256="2af0ec9551ab9c870074cae9d3f68d82cab004f4095fa89db0e4413713424a46")
    version("2.2.1", sha256="94e79a31ed38bdb0acd9af7ccca1605a2ac62ca850ed640202876b1ee11c1c61")

    depends_on("c", type="build")  # generated

    depends_on("uuid", type=("build", "link"))
    depends_on("lvm2", type=("build", "link"))
    depends_on("popt", type=("build", "link"))
    depends_on("json-c", type=("build", "link"))
    depends_on("util-linux", type=("build", "link"))
    depends_on("gettext", type=("build", "link"))

    depends_on("pkgconfig", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("automake@:1.16.1", when="@2.2.1", type="build")
    depends_on("openssl")

    # Upstream includes support for discovering the location of the libintl
    # library but is missing the bit in the Makefile.ac that includes it in
    # the LDFLAGS. See https://gitlab.com/cryptsetup/cryptsetup/issues/479
    # This *should* be unnecessary starting with release 2.2.2, see
    # https://gitlab.com/cryptsetup/cryptsetup/issues/479#note_227617031
    patch("autotools-libintl.patch", when="@:2.2.1")

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/cryptsetup/v{0}/cryptsetup-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        args = [
            "systemd_tmpfilesdir={0}/tmpfiles.d".format(self.prefix),
            "--with-crypto_backend=openssl",
        ]
        return args

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Prepend the sbin directory to PATH."""
        env.prepend_path("PATH", self.prefix.sbin)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Prepend the sbin directory to PATH."""
        env.prepend_path("PATH", self.prefix.sbin)
