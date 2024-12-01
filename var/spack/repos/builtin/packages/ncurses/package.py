# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Ncurses(AutotoolsPackage, GNUMirrorPackage):
    """The ncurses (new curses) library is a free software emulation of
    curses in System V Release 4.0, and more. It uses terminfo format,
    supports pads and color and multiple highlights and forms
    characters and function-key mapping, and has all the other
    SYSV-curses enhancements over BSD curses."""

    homepage = "https://invisible-island.net/ncurses/ncurses.html"
    # URL must remain http:// so Spack can bootstrap curl
    gnu_mirror_path = "ncurses/ncurses-6.1.tar.gz"

    executables = [r"^ncursesw?(?:\d+(?:\.\d+)*)?-config$"]

    license("X11")

    version("6.5", sha256="136d91bc269a9a5785e5f9e980bc76ab57428f604ce3e5a5a90cebc767971cc6")
    version("6.4", sha256="6931283d9ac87c5073f30b6290c4c75f21632bb4fc3603ac8100812bed248159")
    version("6.3", sha256="97fc51ac2b085d4cde31ef4d2c3122c21abc217e9090a43a30fc5ec21684e059")
    version("6.2", sha256="30306e0c76e0f9f1f0de987cf1c82a5c21e1ce6568b9227f7da5b71cbea86c9d")
    version("6.1", sha256="aa057eeeb4a14d470101eff4597d5833dcef5965331be3528c08d99cebaa0d17")
    version("6.0", sha256="f551c24b30ce8bfb6e96d9f59b42fbea30fa3a6123384172f9e7284bcf647260")
    version("5.9", sha256="9046298fb440324c9d4135ecea7879ffed8546dd1b58e59430ea07a4633f563b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("symlinks", default=False, description="Enables symlinks. Needed on AFS filesystem.")
    variant(
        "termlib",
        default=True,
        description="Enables termlib features. This is an extra "
        "lib and optional internal dependency.",
    )
    # Build ncurses with ABI compaitibility.
    variant(
        "abi",
        default="none",
        description="choose abi compatibility",
        values=("none", "5", "6"),
        multi=False,
    )

    conflicts("abi=6", when="@:5.9", msg="6 is not compatible with this release")

    depends_on("pkgconfig", type="build")

    # avoid disallowed const_cast from T* to void* and use reinterpret_cast
    # Ref: https://lists.gnu.org/archive/html/bug-ncurses/2014-08/msg00008.html
    patch("0001-Fix-errors-in-type-conversion.patch", when="@:5")
    patch("sed_pgi.patch", when="@:6.0")
    patch("nvhpc_fix_preprocessor_flag.patch", when="@6.0:6.2%nvhpc")
    patch("rxvt_unicode_6_4.patch", when="@6.1:")

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)("--version", output=str, error=str).rstrip()

    @classmethod
    def determine_variants(cls, exes, version):
        results = []
        for exe in exes:
            variants = ""
            output = Executable(exe)("--libs", output=str, error=str)

            if "-ltinfo" in output:
                variants += "+termlib"

            output = Executable(exe)("--terminfo-dirs", output=str, error=str)
            usingSymlinks = False
            for termDir in output.split(":"):
                for top, dirs, files in os.walk(termDir):
                    for filename in files:
                        if os.path.islink(os.path.join(top, filename)):
                            usingSymlinks = True
                            break
                    if usingSymlinks:
                        break
                if usingSymlinks:
                    break
            if usingSymlinks:
                variants += "+symlinks"

            abiVersion = "none"
            output = Executable(exe)("--abi-version", output=str, error=str)
            if "6" in output:
                abiVersion = "6"
            elif "5" in output:
                abiVersion = "5"
            variants += " abi=" + abiVersion

            results.append(variants)
        return results

    def setup_build_environment(self, env):
        env.unset("TERMINFO")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.cc_pic_flag)
        elif name == "cxxflags":
            flags.append(self.compiler.cxx_pic_flag)

        # ncurses@:6.0 fails in definition of macro 'mouse_trafo' without -P
        if self.spec.satisfies("@:6.0 %gcc@5.0:"):
            if name == "cppflags":
                flags.append("-P")

        # ncurses@:6.0 uses dynamic exception specifications not allowed in c++17
        if self.spec.satisfies("@:5"):
            if name == "cxxflags":
                flags.append(self.compiler.cxx14_flag)

        return (flags, None, None)

    def configure(self, spec, prefix):
        opts = [
            "--disable-stripping",
            "--with-shared",
            "--with-cxx-shared",
            "--enable-overwrite",
            "--without-ada",
            "--enable-pc-files",
            "--disable-overwrite",
        ]

        if spec.satisfies("@:6.2"):
            opts.append("--with-pkg-config-libdir={0}/pkgconfig".format(prefix.lib))
        else:
            pcstage = "{0}/lib/pkgconfig".format(self.stage.source_path)
            mkdirp(pcstage)
            opts.append("--with-pkg-config-libdir={0}".format(pcstage))

        nwide_opts = ["--disable-widec", "--without-manpages", "--without-tests"]

        wide_opts = ["--enable-widec", "--without-manpages", "--without-tests"]

        if "+symlinks" in self.spec:
            opts.append("--enable-symlinks")

        if "+termlib" in self.spec:
            opts.extend(
                (
                    "--with-termlib",
                    "--enable-termcap",
                    "--enable-getcap",
                    "--enable-tcap-names",
                    "--with-versioned-syms",
                )
            )

        abi = self.spec.variants["abi"].value
        if abi != "none":
            opts.append("--with-abi-version=" + abi)

        prefix = "--prefix={0}".format(prefix)

        configure = Executable("../configure")

        with working_dir("build_ncurses", create=True):
            configure(prefix, *(opts + nwide_opts))

        with working_dir("build_ncursesw", create=True):
            configure(prefix, *(opts + wide_opts))

    def build(self, spec, prefix):
        with working_dir("build_ncurses"):
            make()
        with working_dir("build_ncursesw"):
            make()

    def install(self, spec, prefix):
        with working_dir("build_ncurses"):
            make("install")
        with working_dir("build_ncursesw"):
            make("install")

        # fix for packages that use "#include <ncurses.h>" (use wide by default)
        headers = glob.glob(os.path.join(prefix.include, "ncursesw", "*.h"))
        for header in headers:
            h = os.path.basename(header)
            os.symlink(os.path.join("ncursesw", h), os.path.join(prefix.include, h))

        if spec.satisfies("@6.3:"):
            pc_stage = "{0}/lib/pkgconfig".format(self.stage.source_path)
            pc_install = "{0}/pkgconfig".format(prefix.lib)
            mkdirp(pc_install)
            install_tree(pc_stage, pc_install)

    @run_after("install")
    def symlink_curses(self):
        soext = "so" if not self.spec.satisfies("platform=darwin") else "dylib"
        libncurses = "{0}/libncurses.{1}".format(self.prefix.lib, soext)
        libcurses = "{0}/libcurses.{1}".format(self.prefix.lib, soext)
        if not os.path.exists(libcurses) and os.path.exists(libncurses):
            os.symlink(libncurses, libcurses)

    def query_parameter_options(self):
        """Use query parameters passed to spec (e.g., "spec[ncurses:wide]")
        to select wide, non-wide, or default/both."""
        query_parameters = self.spec.last_query.extra_parameters
        return "nowide" in query_parameters, "wide" in query_parameters

    @property
    def headers(self):
        nowide, wide = self.query_parameter_options()
        include = self.prefix.include
        hdirs = []
        if not (nowide or wide):
            # default (top-level, wide)
            hdirs.append(include)
        if nowide:
            hdirs.append(include.ncurses)
        if wide:
            hdirs.append(include.ncursesw)

        headers = HeaderList([])
        for hdir in hdirs:
            headers = headers + find_headers("*", root=hdir, recursive=False).headers
        headers.directories = hdirs
        return headers

    @property
    def libs(self):
        nowide, wide = self.query_parameter_options()
        if not (nowide or wide):
            # default (both)
            nowide = True
            wide = True

        libs = ["libncurses"]
        if "+termlib" in self.spec:
            libs.append("libtinfo")
        wlibs = [lib + "w" for lib in libs]

        libraries = []
        if nowide:
            libraries.extend(libs)
        if wide:
            libraries.extend(wlibs)
        return find_libraries(libraries, root=self.prefix, recursive=True)
