# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Gettext(AutotoolsPackage, GNUMirrorPackage):
    """GNU internationalization (i18n) and localization (l10n) library."""

    homepage = "https://www.gnu.org/software/gettext/"
    gnu_mirror_path = "gettext/gettext-0.20.1.tar.xz"

    maintainers("michaelkuhn")

    executables = [r"^gettext$"]
    tags = ["build-tools"]

    license("GPL-3.0-or-later AND LGPL-2.1-or-later AND MIT")

    version("0.22.5", sha256="fe10c37353213d78a5b83d48af231e005c4da84db5ce88037d88355938259640")
    version("0.22.4", sha256="29217f1816ee2e777fa9a01f9956a14139c0c23cc1b20368f06b2888e8a34116")
    version("0.22.3", sha256="b838228b3f8823a6c1eddf07297197c4db13f7e1b173b9ef93f3f945a63080b6")
    version("0.21.1", sha256="50dbc8f39797950aa2c98e939947c527e5ac9ebd2c1b99dd7b06ba33a6767ae6")
    version("0.21", sha256="d20fcbb537e02dcf1383197ba05bd0734ef7bf5db06bdb241eb69b7d16b73192")
    version("0.20.2", sha256="b22b818e644c37f6e3d1643a1943c32c3a9bff726d601e53047d2682019ceaba")
    version("0.20.1", sha256="53f02fbbec9e798b0faaf7c73272f83608e835c6288dd58be6c9bb54624a3800")
    version("0.19.8.1", sha256="105556dbc5c3fbbc2aa0edb46d22d055748b6f5c7cd7a8d99f8e7eb84e938be4")
    version("0.19.7", sha256="378fa86a091cec3acdece3c961bb8d8c0689906287809a8daa79dc0c6398d934")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Recommended variants
    variant("curses", default=True, description="Use libncurses")
    variant("libxml2", default=True, description="Use libxml2")
    variant("git", default=True, description="Enable git support")
    variant("tar", default=True, description="Enable tar support")
    variant("bzip2", default=True, description="Enable bzip2 support")
    variant("xz", default=True, description="Enable xz support")
    variant("shared", default=True, description="Build shared libraries")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    # Optional variants
    variant("libunistring", default=False, description="Use libunistring")

    depends_on("iconv")
    # Recommended dependencies
    depends_on("ncurses", when="+curses")
    depends_on("libxml2", when="+libxml2")
    # Java runtime and compiler (e.g. GNU gcj or kaffe)
    # C# runtime and compiler (e.g. pnet or mono)
    depends_on("tar", when="+tar", type="run")
    # depends_on('gzip',     when='+gzip')
    depends_on("bzip2", when="+bzip2")
    depends_on("xz", when="+xz", type=("build", "link", "run"))

    # Optional dependencies
    # depends_on('glib')  # circular dependency?
    # depends_on('libcroco@0.6.1:')
    depends_on("libunistring", when="+libunistring")
    # depends_on('cvs')

    conflicts("+shared~pic")
    # https://savannah.gnu.org/bugs/?65811
    conflicts("%gcc@:5", when="@0.22:")

    patch("test-verify-parallel-make-check.patch", when="@:0.19.8.1")
    patch("nvhpc-builtin.patch", when="@:0.21.0 %nvhpc")
    patch("nvhpc-export-symbols.patch", when="%nvhpc")
    patch("nvhpc-long-width.patch", when="%nvhpc")

    def patch(self):
        # Apply this only where we know that the system libc is glibc, be very careful:
        if self.spec.satisfies("@:0.21.0 target=ppc64le"):
            for fn in ("gettext-tools/gnulib-lib/cdefs.h", "gettext-tools/libgrep/cdefs.h"):
                with open(fn, "w") as f:
                    f.write("#include <sys/cdefs.h>\n")

        # From the configure script: "we don't want to use an external libxml, because its
        # dependencies and their dynamic relocations have an impact on the startup time", well,
        # *we* do.
        if self.spec.satisfies("@0.20:+libxml2"):  # libtextstyle/configure not present prior
            filter_file(
                "gl_cv_libxml_force_included=yes",
                "gl_cv_libxml_force_included=no",
                "libtextstyle/configure",
                string=True,
            )

    def flag_handler(self, name, flags):
        # this goes together with gl_cv_libxml_force_included=no
        if name == "ldflags" and self.spec.satisfies("+libxml2"):
            flags.append("-lxml2")
        return (flags, None, None)

    @classmethod
    def determine_version(cls, exe):
        gettext = Executable(exe)
        output = gettext("--version", output=str, error=str)
        match = re.match(r"gettext(?: \(.+\)) ([\d.]+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--disable-java",
            "--disable-csharp",
            "--with-included-glib",
            "--with-included-gettext",
            "--with-included-libcroco",
            "--without-emacs",
            "--with-lispdir=%s/emacs/site-lisp/gettext" % self.prefix.share,
            "--without-cvs",
        ]

        config_args.extend(self.enable_or_disable("shared"))

        if self.spec["iconv"].name == "libiconv":
            config_args.append(f"--with-libiconv-prefix={self.spec['iconv'].prefix}")
        else:
            config_args.append("--without-libiconv-prefix")

        if spec.satisfies("+curses"):
            config_args.append("--with-ncurses-prefix={0}".format(spec["ncurses"].prefix))
        else:
            config_args.append("--disable-curses")

        if spec.satisfies("+libxml2"):
            config_args.append("--with-libxml2-prefix={0}".format(spec["libxml2"].prefix))
        else:
            config_args.append("--with-included-libxml")

        if "+bzip2" not in spec:
            config_args.append("--without-bzip2")

        if "+xz" not in spec:
            config_args.append("--without-xz")

        if spec.satisfies("+libunistring"):
            config_args.append(
                "--with-libunistring-prefix={0}".format(spec["libunistring"].prefix)
            )
        else:
            config_args.append("--with-included-libunistring")

        config_args.extend(self.with_or_without("pic"))

        return config_args

    @property
    def libs(self):
        # Do not fail if the installed gettext did not yet have the shared variant:
        shared_variant = self.spec.variants.get("shared")
        libs = find_libraries(
            ["libasprintf", "libgettextlib", "libgettextpo", "libgettextsrc", "libintl"],
            root=self.prefix,
            recursive=True,
            shared=True if not shared_variant else shared_variant.value,
        )
        return libs
