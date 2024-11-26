# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pgplot(MakefilePackage):
    """PGPLOT Graphics Subroutine Library.

    The PGPLOT Graphics Subroutine Library is a Fortran- or
    C-callable, device-independent graphics package for making
    simple scientific graphs. It is intended for making
    graphical images of publication quality with minimum effort
    on the part of the user. For most applications, the program
    can be device-independent, and the output can be directed to
    the appropriate device at run time."""

    homepage = "https://sites.astro.caltech.edu/~tjp/pgplot/"
    url = "ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz"

    maintainers("eschnett")

    version(
        "5.2.2",
        url="ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz",
        sha256="a5799ff719a510d84d26df4ae7409ae61fe66477e3f1e8820422a9a4727a5be4",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Replace hard-coded compilers and options by tokens, so that Spack can
    # edit the file more easily
    patch("g77_gcc.conf.patch")

    # https://research.iac.es/sieinvens/siepedia/pmwiki.php?n=HOWTOs.PGPLOTMacOSX
    patch("pndriv.c.patch")

    # Read font from spack generated directory
    patch("grsy00.f.patch")

    parallel = False

    # enable drivers
    variant("X", default=False, description="Build with X11 support.")
    variant("png", default=True, description="Enable driver for Portable Network Graphics file.")
    variant("ps", default=True, description="Enable driver for PostScript files.")

    depends_on("libx11", when="+X")
    depends_on("libpng", when="+png")

    def edit(self, spec, prefix):
        libs = ""
        if "+X" in spec:
            libs += " " + self.spec["libx11"].libs.ld_flags
        if "+png" in spec:
            libs += " " + self.spec["libpng"].libs.ld_flags

        sub = {}
        if spec.satisfies("%gcc"):
            fib = " -fallow-invalid-boz" if spec.satisfies("%gcc@10:") else ""

            sub = {
                "@CCOMPL@": spack_cc,
                "@CFLAGC@": "-Wall -fPIC -DPG_PPU -O -std=c89 "
                + "-Wno-error=implicit-function-declaration",
                "@CFLAGD@": "-O2 -fPIC",
                "@FCOMPL@": spack_fc,
                "@FFLAGC@": "-Wall -fPIC -O -ffixed-line-length-none" + fib,
                "@FFLAGD@": "-fPIC " + libs + " -fno-backslash",
                "@LIBS@": libs + " -lgfortran",
                "@SHARED_LD@": spack_cc + " -shared -o $SHARED_LIB",
                "@SHARED_LIB_LIBS@": libs + " -lgfortran",
            }
        elif spec.satisfies("%intel"):
            sub = {
                "@CCOMPL@": spack_cc,
                "@CFLAGC@": "-O2 -fPIC -DPG_PPU",
                "@CFLAGD@": "-O2 -lifcore -lifport",
                "@FCOMPL@": spack_fc,
                "@FFLAGC@": "-fPIC",
                "@FFLAGD@": libs + " -nofor-main",
                "@LIBS@": libs + " -nofor-main -lifcore -lifport",
                "@SHARED_LD@": spack_cc + " -shared -o $SHARED_LIB",
                "@SHARED_LIB_LIBS@": libs + " -nofor-main -lifcore -lifport",
            }

        conf = join_path(self.stage.source_path, "sys_linux/g77_gcc.conf")

        drivers_list = join_path(self.stage.source_path, "drivers.list")

        # eg. change contents of drivers_list file like:
        # '! XWDRIV 1 /XWINDOW' ->  'XWDRIV 1 /XWINDOW'
        enable_driver = lambda s: filter_file(s, s[2:], drivers_list)

        if "+X" in spec:
            enable_driver("! XWDRIV 1 /XWINDOW")
            enable_driver("! XWDRIV 2 /XSERVE")

        if "+png" in spec:
            enable_driver("! PNDRIV 1 /PNG")

            filter_file(
                "pndriv.o : ./png.h ./pngconf.h ./zlib.h ./zconf.h", "pndriv.o :", "makemake"
            )

        # Alwasy enable PS and LATEX since they are not depending on other libraries.
        enable_driver("! PSDRIV 1 /PS")
        enable_driver("! PSDRIV 2 /VPS")
        enable_driver("! PSDRIV 3 /CPS")
        enable_driver("! PSDRIV 4 /VCPS")
        enable_driver("! LXDRIV 0 /LATEX")

        # GIF is not working. Maybe it is a bug in the gidriv.f.
        # enable_driver('! GIDRIV 1 /GIF')
        # enable_driver('! GIDRIV 2 /VGIF')

        for key, value in sub.items():
            filter_file(key, value, conf)

    def setup_build_environment(self, env):
        if "+X" in self.spec:
            env.append_flags("LIBS", self.spec["libx11"].libs.ld_flags)
        if "+png" in self.spec:
            env.append_flags("LIBS", self.spec["libpng"].libs.ld_flags)

    def build(self, spec, prefix):
        makemake = which("./makemake")
        makemake(self.build_directory, "linux", "g77_gcc")
        make()
        make("clean")
        make("cpg")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("cpgdemo", prefix.bin)
        install("pgbind", prefix.bin)
        install("pgdemo1", prefix.bin)
        install("pgdemo2", prefix.bin)
        install("pgdemo3", prefix.bin)
        install("pgdemo4", prefix.bin)
        install("pgdemo5", prefix.bin)
        install("pgdemo6", prefix.bin)
        install("pgdemo7", prefix.bin)
        install("pgdemo8", prefix.bin)
        install("pgdemo9", prefix.bin)
        install("pgdemo10", prefix.bin)
        install("pgdemo11", prefix.bin)
        install("pgdemo12", prefix.bin)
        install("pgdemo13", prefix.bin)
        install("pgdemo14", prefix.bin)
        install("pgdemo15", prefix.bin)
        install("pgdemo16", prefix.bin)
        install("pgdemo17", prefix.bin)
        if "+X" in spec:
            install("pgxwin_server", prefix.bin)
        mkdirp(prefix.include)
        install("cpgplot.h", prefix.include)
        mkdirp(prefix.lib)
        install("libcpgplot.a", prefix.lib)
        install("libpgplot.a", prefix.lib)
        install("libpgplot.so", prefix.lib)
        install("grfont.dat", prefix.include)
        mkdirp(prefix.lib + "/pgplot5")
        install("rgb.txt", prefix.lib + "/pgplot5")

    @property
    def libs(self):
        shared = "+shared" in self.spec
        if shared:
            libnames = ["libpgplot"]
        else:
            libnames = ["libcpgplot", "libpgplot"]
        return find_libraries(libnames, root=self.prefix, shared=shared, recursive=True)

    def setup_run_environment(self, env):
        env.set("PGPLOT_FONT", self.prefix.include + "/grfont.dat")
        env.set("PGPLOT_DIR", self.prefix.lib + "/pgplot5")

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("PGPLOT_FONT", self.prefix.include + "/grfont.dat")
        env.set("PGPLOT_DIR", self.prefix.lib + "/pgplot5")
