# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Kentutils(MakefilePackage):
    """
    Jim Kent command line bioinformatic utilities and libraries

    This bundles a custom version of htslib, but can be overridden with ~htslib.
    Consider adding the ^mysql+client_only dependency to avoid building all mysql/mariadb.
    """

    homepage = "https://genome.cse.ucsc.edu/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v453.src.tgz"

    maintainers("teaguesterling")

    version("465", sha256="eef17b1f3182d1d9dc99b5c73a6b0468d5d3bd80470f25d3f7706cc1372e04b0")
    version("464", sha256="24e20fe68e2a2894d802c87662f69a62f71b3c15fafb2e4d6c3c425c63638bb2")
    version("460", sha256="b955e56ee880074521ef1ab1371491f47e66dc6fdd93b05328386dd675a635fa")
    version("455", sha256="e458cadad7c4a5c1b8385edafffa1b29380ac725a0c20535bf5a3bab99fe80db")
    # This version isn't present in the archive any more
    # Might be worth changing url to: https://github.com/ucscGenomeBrowser/kent-core/tags/...
    version(
        "459",
        sha256="0b6e89a183e6385c713cf010a7aeead9da6626d8d2f78c363a4f1bc56ccccebb",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # The bundled version of kentlib has some custom changes that are used by parts of
    # kentlib. See https://github.com/spack/spack/pull/44501#issuecomment-2162789410
    # for some additional details. A built-in version SHOULD work for most things though.
    variant(
        "builtin_htslib",
        default=False,
        description="Build with bundled htslib (using an external htslib may lead to errors)",
        sticky=True,
    )

    with default_args(type=("build", "link", "run")):
        depends_on("libpng")
        depends_on("openssl")
        depends_on("uuid")
        depends_on("mysql-client")
        depends_on("zlib-api")
        depends_on("freetype")
        depends_on("libiconv")
        depends_on("htslib+pic", when="~builtin_htslib")

    # The bgzip.c bug present in other packages is present in kent/src/htslib/bgzf.c
    # Conflicting line: assert(compressBound(BGZF_BLOCK_SIZE) < BGZF_MAX_BLOCK_SIZE);
    # We can patch this by removing the assertion, but there are still performance issues
    # See: https://github.com/samtools/htslib/issues/1257
    conflicts("zlib-ng")

    # Does not add a link to mysql_config, which is required for compilation
    conflicts("mariadb-c-client")

    # MySQL pointer/integer conversion issue (https://github.com/ucscGenomeBrowser/kent/pull/87)
    patch("fix-mysql-options-gcc13.patch", when="%gcc@13: ^mysql")
    # MySQL build flags from `mysql_config` are not compatible with Spack's method of building
    # and includes zlib when it's not needed/available, leading to a linking failure.
    patch("mysql-zlib-workaround.patch", when="%gcc ^mysql")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.cc_pic_flag)
        elif name == "ldflags":
            flags.append(f'{self.spec["libiconv"].libs.ld_flags}')
        return (flags, None, None)

    @property
    def machtype(self):
        # This is hard-coded in the Makefile and included here for reference
        # and to make it adjustable if we need to adjust this in the future
        return "local"

    @property
    def headers(self):
        headers = []
        headers.extend(find_headers("*", self.prefix.inc, recursive=True))
        if self.spec.satisfies("+builtin_htslib"):
            headers.extend(find_headers("*", self.prefix.htslib, recursive=True))
        return HeaderList(headers)

    @property
    def libs(self):
        return LibraryList([join_path(self.prefix, lib) for lib in self.local_libs])

    @property
    def local_libs(self):
        libs = [
            f"lib/{self.machtype}/jkweb.a",
            f"lib/{self.machtype}/jkOwnLib.a",
            f"lib/{self.machtype}/jkhgap.a",
            f"lib/{self.machtype}/jkhgapcgi.a",
            f"hg/altSplice/lib/{self.machtype}/libSpliceGraph.a",
        ]
        if self.spec.satisfies("+builtin_htslib"):
            libs.append("htslib/libhts.a")
        return LibraryList(libs)

    @property
    def lib_dir(self):
        return join_path(self.prefix.lib, self.machtype)

    @property
    def htslib_include_dir(self):
        if self.spec.satisfies("~builtin_htslib"):
            # If we're not using the bundled version, just defer to htslib
            return self.spec["htslib"].prefix.include
        else:
            # In the event we're using the bundled htslib, the htslib
            # headers live in a different part of the installed tree
            return self.prefix.htslib

    # Packages that link to kentlib (and potential, htslib) often have
    # idiosyncratic ways of setting up their includes and linker paths.
    # Having these paths available will make things cleaner downstream.
    def setup_dependent_package(self, module, dep_spec):
        setattr(module, "kentutils_include_dir", self.prefix.inc)
        setattr(module, "kentutils_lib_dir", self.lib_dir)
        setattr(module, "kentutils_htslib_include_dir", self.htslib_include_dir)

    def install_libs_from_stage(self, spec, prefix):
        # Dependent packages expect things in the source tree, but we don't
        # want to copy all of the compilation artifacts in so we'll do them
        # manually instead of leaving the build directory around

        src_prefix = "kent/src"

        def install_kent(path, tree):
            src = join_path(src_prefix, path)
            dest = join_path(prefix, path)
            mkdirp(os.path.dirname(dest))
            if tree:
                install_tree(src, dest)
            else:
                install(src, dest)

        install_kent("inc", tree=True)
        if spec.satisfies("+builtin_htslib"):
            install_kent("htslib/htslib", tree=True)

        for lib in self.local_libs:
            install_kent(lib, tree=False)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        self.install_libs_from_stage(spec, prefix)
