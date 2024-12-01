# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Octa(AutotoolsPackage):
    """OCTA is an integrated simulation system for soft materials."""

    homepage = "https://octa.jp"
    url = (
        "http://49.212.191.63/phpBB/download/file.php?id=3454&sid=3dfae182c664d1f5960d9ca63c40798a"
    )

    version(
        "8.4",
        sha256="b76d25f333fef76601bfe8262e9a748154280d5408ea823fa6530a6f3f86b51b",
        extension="tar.gz",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("libjpeg", type="link")
    depends_on("libpng", type="link")
    depends_on("zlib-api", type="link")
    depends_on("jogl")
    depends_on("python")
    depends_on("gnuplot", type="run")
    depends_on("py-numpy")
    depends_on("py-scipy")
    depends_on("py-numba")

    # specify for linux_aarch64
    patch("aarch64.patch", when="target=aarch64:")
    # For jogl 2.3.2 or later
    patch("jogl.patch")
    # patch for non-constant-expression cannot be narrowed error.
    patch("narrowed-initialize.patch")

    configure_directory = join_path("GOURMET", "src")

    def patch(self):
        with working_dir(self.configure_directory):
            copy("jogltest.java_v232", "jogltest.java")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-python={0}".format(spec["python"].command),
            "--with-java-home={0}".format(spec["java"].prefix),
            "--with-jogl-jar={0}".format(spec["jogl"].prefix.lib),
            "--with-jogl-lib={0}".format(spec["jogl"].prefix.lib),
        ]
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path("GOURMET", "bin", "*.sh"), prefix.bin)
        with working_dir(self.configure_directory):
            make("install", parallel=False)
