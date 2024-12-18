# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Guile(AutotoolsPackage, GNUMirrorPackage):
    """Guile is the GNU Ubiquitous Intelligent Language for Extensions,
    the official extension language for the GNU operating system."""

    homepage = "https://www.gnu.org/software/guile/"
    gnu_mirror_path = "guile/guile-2.2.0.tar.gz"

    license("LGPL-3.0-or-later AND GPL-3.0-or-later")

    version("2.2.6", sha256="08c0e7487777740b61cdd97949b69e8a5e2997d8c2fe6c7e175819eb18444506")
    version("2.2.5", sha256="c3c7a2f6ae0d8321a240c7ebc532a1d47af8c63214157a73789e2b2305b4c927")
    version("2.2.4", sha256="33b904c0bf4e48e156f3fb1d0e6b0392033bd610c6c9d9a0410c6e0ea96a3e5c")
    version("2.2.3", sha256="87ee07caef33c97ddc74bf3c29ce7628cfac12061f573e4a29a3a1176754610a")
    version("2.2.2", sha256="3d9b94183b19f04dd4317da87beedafd1c947142f3d861ca1f0224e7a75127ee")
    version("2.2.1", sha256="f004b2a5e98017df80cd419773f12a77cfc7ba6069195f97d6702e3d6e487a14")
    version("2.2.0", sha256="ef1e9544631f18029b113911350bffd5064955c208a975bfe0d27a4003d6d86b")
    version("2.0.14", sha256="8aeb2f353881282fe01694cce76bb72f7ffdd296a12c7a1a39255c27b0dfe5f1")
    version("2.0.11", sha256="e6786c934346fa2e38e46d8d81a622bb1c16d130153523f6129fcd79ef1fb040")

    depends_on("c", type="build")  # generated

    variant("readline", default=True, description="Use the readline library")
    variant(
        "threads",
        default="none",
        values=("none", "posix", "dgux386"),
        multi=False,
        description="Use the thread interface",
    )

    depends_on("bdw-gc@7.0: threads=none", when="threads=none")
    depends_on("bdw-gc@7.0: threads=posix", when="threads=posix")
    depends_on("bdw-gc@7.0: threads=dgux386", when="threads=dgux386")
    depends_on("gmp@4.2:")
    depends_on("gettext")
    depends_on("libtool@1.5.6:", type="link")  # links to libltdl.so
    depends_on("libunistring@0.9.3:")
    depends_on("libffi")
    depends_on("readline", when="+readline")
    depends_on("pkgconfig", type="build")

    build_directory = "spack-build"

    conflicts("threads=posix", when="%intel")
    conflicts("threads=dgux386", when="%intel")

    def flag_handler(self, name, flags):
        # Intel oneAPI's compiler enables fast math by default, which
        # breaks Guile's build. See https://github.com/spack/spack/discussions/38689
        if name == "cflags" and "%oneapi" in self.spec:
            flags.append("-fp-model=precise")

        return (flags, None, None)

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--with-libunistring-prefix={0}".format(spec["libunistring"].prefix),
            "--with-libltdl-prefix={0}".format(spec["libtool"].prefix),
            "--with-libgmp-prefix={0}".format(spec["gmp"].prefix),
            "--with-libintl-prefix={0}".format(spec["gettext"].prefix),
        ]

        if spec.satisfies("threads=none"):
            config_args.append("--without-threads")
        else:
            config_args.append("--with-threads")

        if spec.satisfies("+readline"):
            config_args.append("--with-libreadline-prefix={0}".format(spec["readline"].prefix))
        else:
            config_args.append("--without-libreadline-prefix")

        return config_args
