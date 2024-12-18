# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from shutil import copyfile

from spack.package import *


class Netpbm(MakefilePackage):
    """Netpbm - graphics tools and converters.

    A whole bunch of utilities for primitive manipulation of
    graphic images. Wide array of converters
    from one graphics format to another. E.g.
    from g3 fax format to jpeg. Many basic graphics
    editing tools such as magnifying and cropping.
    """

    homepage = "https://netpbm.sourceforge.net"
    url = "https://sourceforge.net/projects/netpbm/files/super_stable/10.73.35/netpbm-10.73.35.tgz"

    maintainers("cessenat")

    license("IJG AND BSD-3-Clause AND GPL-2.0-only")

    version("10.73.43", sha256="f9fd9a7f932258224d1925bfce61396a15e0fad93e3853d6324ac308d1adebf8")
    version("10.73.40", sha256="8542ae62aa744dfd52c8e425208f895f082955a0629ac1749f80278d6afc0344")
    version("10.73.35", sha256="628dbe8490bc43557813d1fedb2720dfdca0b80dd3f2364cb2a45c6ff04b0f18")

    depends_on("c", type="build")  # generated

    # As a default we wish to commpile absolutely everything at once.
    # Variants are there in case compilation was a problem.
    variant("all", default=True, description="Enable all 3rd party libs")
    variant("X", default=True, description="Enable X libs for pamx")
    variant("fiasco", default=True, description="Enable fiasco")
    variant(
        "ghostscript", default=True, description="Ghostscript is called by pstopnm and pbmtextps"
    )
    # netpbm can provide it's own jasper and jbig : better use the ones
    # from their respective spack package.
    variant("builtin", default=False, description="Use builtin libs instead of 3rd party")

    depends_on("perl", type=("build", "run"))
    depends_on("gmake", type="build")
    depends_on("pkgconfig", type="build")

    # These are general pre-requisites indicated at
    # http://netpbm.sourceforge.net/prereq.html
    depends_on("zlib-api")
    depends_on("jpeg")
    depends_on("libtiff")
    depends_on("libpng")
    # Ghostscript is called as "gs" by pstopnm and pbmtextps
    depends_on("ghostscript", type="run", when="+ghostscript")

    # These are the optional libs:
    # svgtopam : http://netpbm.sourceforge.net/prereq.html
    # homebrew also sets a dependancy to libxml2
    # https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/netpbm.rb
    depends_on("libxml2", when="+all")
    # thinkjettopbm : http://netpbm.sourceforge.net/prereq.html
    depends_on("flex", type=("build", "run"), when="+all")
    # https://formulae.brew.sh/formula/netpbm
    depends_on("jasper", when="+all~builtin")
    # Only Mac Ports sets a dependency to jbig
    # https://ports.macports.org/port/netpbm/summary
    depends_on("jbigkit", when="+all~builtin")

    # pamx depends on X11 libraries:
    depends_on("libx11", when="+X")

    def edit(self, spec, prefix):
        # We better not run the interactive perl script buildtools/configure.pl
        # as explained by Todd in
        # https://groups.google.com/g/spack/c/8sEqDkZ68DA/m/wpbB0wHaAgAJ
        # so we will mimic the perl script bahavior
        copyfile("config.mk.in", "config.mk")
        config = []
        config.append("####Lines above were copied from config.mk.in")
        # This is already the default but we make sure it is set
        # even for a dev release for instance:
        config.append("DEFAULT_TARGET = nonmerge")
        config.append("NETPBMLIBSUFFIX={0}".format(dso_suffix))
        if "platform=darwin" in spec:
            config.append("NETPBMLIBTYPE=dylib")
            args = ["-dynamiclib", "-Wl,-install_name"]
            args.append("-Wl,@rpath/libnetpbm.dylib")
            config.append("LDSHLIB = {0}".format(" ".join(args)))
        elif "platform=cygwin" in spec:
            config.append("NETPBMLIBTYPE=dll")
            config.append("NETPBMLIBSUFFIX=dll")
            config.append("SHLIBPREFIXLIST=cyg lib")
            config.append("EXE = .exe")
            config.append("SYMLINK = cp")
            config.append("LINKERISCOMPILER = Y")
            config.append("WINICON_OBJECT = $(BUILDDIR)/icon/netpbm.o")
            config.append("DLLVER=$(NETPBM_MAJOR_RELEASE)")
            args = ["-shared", "-Wl,--image-base=0x10000000"]
            args.append("-Wl,--enable-auto-import")
            config.append("LDSHLIB = {0}".format(" ".join(args)))
        else:
            config.append("NETPBMLIBTYPE=unixshared")

        if "~fiasco" in spec:
            config.append("BUILD_FIASCO = N")

        config.append("STATICLIB_TOO=Y")
        config.append("OMIT_NETWORK = Y")
        config.append("CC = {0}".format(spack_cc))
        config.append("LD = {0}".format(spack_cc))
        config.append("CC_FOR_BUILD = {0}".format(spack_cc))
        config.append("LD_FOR_BUILD = {0}".format(spack_cc))
        config.append("CFLAGS_SHLIB += {0}".format(self.compiler.cc_pic_flag))
        if "%gcc" in spec or "platform=darwin" in spec:
            cflags = ["-O3", "-ffast-math", "-pedantic", "-Wall", "-Wimplicit"]
            cflags.extend(["-Wno-uninitialized", "-Wmissing-declarations"])
            cflags.extend(["-Wwrite-strings", "-Wmissing-prototypes"])
            cflags.extend(["-Wundef", "-Wno-unknown-pragmas"])
            if "platform=darwin" in spec:
                # https://github.com/macports/macports-ports/blob/master/graphics/netpbm/Portfile
                cflags.append("-D_DARWIN_C_SOURCE")
                # https://www.linuxquestions.org/questions/linux-from-scratch-13/can't-compile-luit-xorg-applications-4175476308/
                # cflags.append('-U_XOPEN_SOURCE')
                # https://www.mistys-internet.website/blog/blog/2013/10/19/no-cpp-precomp-the-compiler-flag-that-time-forgot/
                # cflags.append('-no-cpp-precomp')
            config.append("CFLAGS = {0}".format(" ".join(cflags)))
            config.append("CFLAGS_SHLIB += -fno-common")

        if "+all" in spec:
            flex = join_path(spec["flex"].prefix.bin, "flex")
            if os.path.exists(flex):
                config.append("LEX = {0}".format(flex))

        config.append("TIFFLIB={0}".format(spec["libtiff"].libs.ld_flags))
        config.append("TIFFHDR_DIR={0}".format(spec["libtiff"].headers.directories[0]))
        config.append("PNGLIB={0}".format(spec["libpng"].libs.ld_flags))
        config.append("PNGHDR_DIR={0}".format(spec["libpng"].headers.directories[0]))
        config.append("JPEGLIB={0}".format(spec["jpeg"].libs.ld_flags))
        config.append("JPEGHDR_DIR={0}".format(spec["jpeg"].headers.directories[0]))
        if "+all" in spec and "+builtin" not in spec:
            config.append("JASPERLIB={0}".format(spec["jasper"].libs.ld_flags))
            config.append("JASPERHDR_DIR={0}".format(spec["jasper"].headers.directories[0]))
            config.append("JBIGLIB={0}".format(spec["jbigkit"].libs.ld_flags))
            config.append("JBIGHDR_DIR={0}".format(spec["jbigkit"].headers.directories[0]))
        if "+X" in spec:
            pkg_config = which("pkg-config")
            if not pkg_config("x11", "--exists"):
                config.append("X11LIB={0}".format(spec["libx11"].libs.ld_flags))
                config.append("X11HDR_DIR={0}".format(spec["libx11"].headers.directories[0]))
                config.append("ZLIB={0}".format(spec["zlib-api"].libs.ld_flags))
        config.append("NETPBM_DOCURL = http://netpbm.sourceforge.net/doc/")
        if spec.target.family == "x86_64":
            config.append("WANT_SSE = Y")

        with open("config.mk", "a") as mk:
            mk.write("\n".join(config))

    def build(self, spec, prefix):
        make()
        if self.run_tests:
            # Don't run the default command 'make check' for test
            self.build_time_test_callbacks = []

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def make_check_tree(self):
        # Run custom test command 'make check-tree'
        make("check-tree")

    def install(self, spec, prefix):
        bdir = join_path(self.build_directory, "build")
        make("package", "pkgdir={0}".format(bdir), parallel=False)
        # Same as before build, mimic the interactive
        # perl script buildtools/installnetpbm.pl
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        mkdirp(prefix.man)
        with working_dir("build"):
            install_tree("bin", prefix.bin)
            install_tree("lib", prefix.lib)
            install_tree("misc", prefix.lib)
            install_tree("include", prefix.include)
            install_tree(join_path("include", "netpbm"), prefix.include)
            if os.path.exists("man"):
                install_tree("man", prefix.man)
            # As a default a static lib is also created.
            # We could put that as an option
            staticlib = join_path("staticlink", "libnetpbm.a")
            if os.path.exists(staticlib):
                install(staticlib, prefix.lib)
            else:
                staticlib = join_path("link", "libnetpbm.a")
                if os.path.exists(staticlib):
                    install(staticlib, prefix.lib)
        # Make the .pc as done by installnetpbm.pl
        src = join_path("buildtools", "pkgconfig_template")
        pdir = join_path(prefix.lib, "pkgconfig")
        mkdirp(pdir)
        copyfile(src, join_path(pdir, "netpbm.pc"))
        pfic = FileFilter(join_path(pdir, "netpbm.pc"))
        pfic.filter("@VERSION@", "Netpbm {0}".format(str(spec.version)))
        pfic.filter("@LINKDIR@", "{0}".format(prefix.lib))
        pfic.filter("@INCLUDEDIR@", "{0}".format(prefix.include))
