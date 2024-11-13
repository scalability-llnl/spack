# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys

from spack.package import *


class Mumps(Package):
    """MUMPS: a MUltifrontal Massively Parallel sparse direct Solver"""

    homepage = "https://mumps-solver.org/index.php"
    url = "https://mumps-solver.org/MUMPS_5.5.1.tar.gz"

    maintainers("jcortial-safran")

    version("5.7.3", sha256="84a47f7c4231b9efdf4d4f631a2cae2bdd9adeaabc088261d15af040143ed112")
    version("5.7.2", sha256="1362d377ce7422fc886c55212b4a4d2c381918b5ca4478f682a22d0627a8fbf8")
    version("5.6.2", sha256="13a2c1aff2bd1aa92fe84b7b35d88f43434019963ca09ef7e8c90821a8f1d59a")
    version("5.6.1", sha256="1920426d543e34d377604070fde93b8d102aa38ebdf53300cbce9e15f92e2896")
    version("5.6.0", sha256="3e08c1bdea7aaaba303d3cf03059f3b4336fa49bef93f4260f478f067f518289")
    version("5.5.1", sha256="1abff294fa47ee4cfd50dfd5c595942b72ebfcedce08142a75a99ab35014fa15")
    version("5.5.0", sha256="e54d17c5e42a36c40607a03279e0704d239d71d38503aab68ef3bfe0a9a79c13")
    version("5.4.1", sha256="93034a1a9fe0876307136dcde7e98e9086e199de76f1c47da822e7d4de987fa8")
    version("5.4.0", sha256="c613414683e462da7c152c131cebf34f937e79b30571424060dd673368bbf627")
    version("5.3.5", sha256="e5d665fdb7043043f0799ae3dbe3b37e5b200d1ab7a6f7b2a4e463fd89507fa4")
    version("5.3.3", sha256="27e7749ac05006bf8e81a457c865402bb72a42bf3bc673da49de1020f0f32011")
    version("5.2.0", sha256="41f2c7cb20d69599fb47e2ad6f628f3798c429f49e72e757e70722680f70853f")
    version("5.1.2", sha256="eb345cda145da9aea01b851d17e54e7eef08e16bfa148100ac1f7f046cd42ae9")
    version("5.1.1", sha256="a2a1f89c470f2b66e9982953cbd047d429a002fab9975400cef7190d01084a06")
    version("5.0.2", sha256="77292b204942640256097a3da482c2abcd1e0d5a74ecd1d4bab0f5ef6e60fe45")
    # Alternate location if main server is down.
    # version('5.0.1', sha256='50355b2e67873e2239b4998a46f2bbf83f70cdad6517730ab287ae3aae9340a0',
    #         url='http://pkgs.fedoraproject.org/repo/pkgs/MUMPS/MUMPS_5.0.1.tar.gz/md5/b477573fdcc87babe861f62316833db0/MUMPS_5.0.1.tar.gz')
    version("5.0.1", sha256="50355b2e67873e2239b4998a46f2bbf83f70cdad6517730ab287ae3aae9340a0")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Compile MUMPS with MPI support")
    variant("scotch", default=False, description="Activate Scotch as a possible ordering library")
    variant(
        "ptscotch", default=False, description="Activate PT-Scotch as a possible ordering library"
    )
    variant("metis", default=False, description="Activate Metis as a possible ordering library")
    variant(
        "parmetis", default=False, description="Activate Parmetis as a possible ordering library"
    )
    variant("double", default=True, description="Activate the compilation of dmumps")
    variant("float", default=True, description="Activate the compilation of smumps")
    variant(
        "complex", default=True, description="Activate the compilation of cmumps and/or zmumps"
    )
    variant("int64", default=False, description="Use int64_t/integer*8 as default index type")
    variant("incfort", default=False, description="Use explicit types size in fortran headers")
    variant("shared", default=True, description="Build shared libraries")
    variant("openmp", default=True, description="Compile MUMPS with OpenMP support")
    variant(
        "blr_mt",
        default=False,
        description="Allow BLAS calls in OpenMP regions "
        + "(warning: might not be supported by all multithread BLAS)",
    )

    depends_on("scotch + esmumps", when="~ptscotch+scotch")
    depends_on("scotch + esmumps ~ metis + mpi", when="+ptscotch")
    depends_on("metis@5:", when="+metis")
    depends_on("parmetis", when="+parmetis")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack", when="+mpi")
    depends_on("mpi", when="+mpi")

    patch("examples.patch", when="@5.1.1%clang^spectrum-mpi")
    patch("gfortran8.patch", when="@5.1.2")
    # The following patches src/Makefile to fix some dependency
    # issues in lib[cdsz]mumps.so
    patch("mumps.src-makefile.5.2.patch", when="@5.2.0 +shared")
    patch("mumps.src-makefile.5.3.patch", when="@5.3.0:5.4.1 +shared")
    patch("mumps.src-makefile.5.5.patch", when="@5.5.0: +shared")

    conflicts("+parmetis", when="~mpi", msg="You cannot use the parmetis variant without mpi")
    conflicts("+parmetis", when="~metis", msg="You cannot use the parmetis variant without metis")
    conflicts("+ptscotch", when="~mpi", msg="You cannot use the ptscotch variant without mpi")
    conflicts("+blr_mt", when="~openmp", msg="You cannot use the blr_mt variant without openmp")

    @when("+incfort")
    def patch(self):
        """Set the effective integer type used during compilation.
        Usual usecase: building mumps with int and compiling a program that
        includes these headers with '-fdefault-integer-8'.
        """
        headers = glob.glob("include/*.h")
        intsize = 8 if "+int64" in self.spec else 4
        filter_file("INTEGER *,", "INTEGER({0}),".format(intsize), *headers)
        filter_file("INTEGER *::", "INTEGER({0}) ::".format(intsize), *headers)
        for typ in ("REAL", "COMPLEX", "LOGICAL"):
            filter_file("{0} *,".format(typ), "{0}(4),".format(typ), *headers)
            filter_file("{0} *::".format(typ), "{0}(4) ::".format(typ), *headers)

    def write_makefile_inc(self):
        # The makefile variables LIBBLAS, LSCOTCH, LMETIS, and SCALAP are only
        # used to link the examples, so if building '+shared' there is no need
        # to explicitly link with the respective libraries because we make sure
        # the mumps shared libraries are already linked with them. See also the
        # comment below about 'inject_libs'. This behaviour may cause problems
        # if building '+shared' and the used libraries were build static
        # without the PIC option.
        shared = "+shared" in self.spec

        lapack_blas = self.spec["lapack"].libs + self.spec["blas"].libs
        makefile_conf = ["LIBBLAS = %s" % lapack_blas.ld_flags if not shared else ""]

        orderings = ["-Dpord"]
        # All of the lib[cdsz]mumps.* libs depend on mumps_common
        extra_libs4mumps = ["-L$(topdir)/lib", "-lmumps_common"]
        # and mumps_common depends on pord
        extra_libs4mumps += ["-L$(topdir)/PORD/lib", "-lpord"]

        if "+ptscotch" in self.spec or "+scotch" in self.spec:
            makefile_conf.extend(
                [
                    "ISCOTCH = -I%s" % self.spec["scotch"].prefix.include,
                    "LSCOTCH = {0}".format(
                        self.spec["scotch"].libs.ld_flags if not shared else ""
                    ),
                ]
            )

            orderings.append("-Dscotch")
            if "+ptscotch" in self.spec:
                orderings.append("-Dptscotch")

        if "+parmetis" in self.spec:
            makefile_conf.extend(
                [
                    "IMETIS = -I%s" % self.spec["parmetis"].prefix.include,
                    (
                        (
                            "LMETIS = -L%s -l%s -L%s -l%s"
                            % (
                                self.spec["parmetis"].prefix.lib,
                                "parmetis",
                                self.spec["metis"].prefix.lib,
                                "metis",
                            )
                        )
                        if not shared
                        else "LMETIS ="
                    ),
                ]
            )

            orderings.append("-Dparmetis")
        elif "+metis" in self.spec:
            makefile_conf.extend(
                [
                    "IMETIS = -I%s" % self.spec["metis"].prefix.include,
                    (
                        ("LMETIS = -L%s -l%s" % (self.spec["metis"].prefix.lib, "metis"))
                        if not shared
                        else "LMETIS ="
                    ),
                ]
            )

            orderings.append("-Dmetis")

        makefile_conf.append("ORDERINGSF = %s" % (" ".join(orderings)))

        # Determine which compiler suite we are using
        using_gcc = self.compiler.name == "gcc"
        using_pgi = self.compiler.name == "pgi"
        using_nvhpc = self.compiler.name == "nvhpc"
        using_intel = self.compiler.name == "intel"
        using_oneapi = self.compiler.name == "oneapi"
        using_xl = self.compiler.name in ["xl", "xl_r"]
        using_fj = self.compiler.name == "fj"

        # The llvm compiler suite does not contain a Fortran compiler by
        # default.  Its possible that a Spack user may have configured
        # ~/.spack/<platform>/compilers.yaml for using xlf.
        using_xlf = using_xl or (spack_f77.endswith("xlf") or spack_f77.endswith("xlf_r"))

        # when building shared libs need -fPIC, otherwise
        # /usr/bin/ld: graph.o: relocation R_X86_64_32 against `.rodata.str1.1'
        # can not be used when making a shared object; recompile with -fPIC
        cpic = self.compiler.cc_pic_flag if shared else ""
        fpic = self.compiler.fc_pic_flag if shared else ""
        # TODO: test this part, it needs a full blas, scalapack and
        # partitionning environment with 64bit integers

        # The mumps.src-makefile.patch wants us to set these PIC variables
        makefile_conf.append("FC_PIC_FLAG={0}".format(fpic))
        makefile_conf.append("CC_PIC_FLAG={0}".format(cpic))

        opt_level = "3" if using_xl else "2"

        optc = ["-O{0}".format(opt_level)]
        optf = ["-O{0}".format(opt_level)]
        optl = ["-O{0}".format(opt_level)]

        if shared:
            optc.append(cpic)
            optf.append(fpic)
            optl.append(cpic)

        if not using_xlf:
            optf.append("-DALLOW_NON_INIT")

        if "+int64" in self.spec:
            if not using_xlf:
                # the fortran compilation flags most probably are
                # working only for intel and gnu compilers this is
                # perhaps something the compiler should provide
                optf.append("-fdefault-integer-8" if using_gcc else "-i8")

            optc.append("-DINTSIZE64")
        else:
            if using_xlf:
                optf.append("-qfixed")

        # With gfortran >= 10 we need to add '-fallow-argument-mismatch'. This
        # check handles mixed toolchains which are not handled by the method
        # 'flag_handler' defined below.
        # TODO: remove 'flag_handler' since this check covers that case too?
        if os.path.basename(spack_fc) == "gfortran":
            gfortran = Executable(spack_fc)
            gfort_ver = Version(gfortran("-dumpversion", output=str).strip())
            if gfort_ver >= Version("10"):
                optf.append("-fallow-argument-mismatch")

        # As of version 5.2.0, MUMPS is able to take advantage
        # of the GEMMT BLAS extension. MKL and amdblis are the only
        # known BLAS implementation supported.
        if self.spec["blas"].name in INTEL_MATH_LIBRARIES and self.spec.satisfies("@5.2.0:"):
            optf.append("-DGEMMT_AVAILABLE")

        if "@5.2.0: ^amdblis@3.0:" in self.spec:
            optf.append("-DGEMMT_AVAILABLE")

        if "+openmp" in self.spec:
            optc.append(self.compiler.openmp_flag)
            optf.append(self.compiler.openmp_flag)
            optl.append(self.compiler.openmp_flag)

        # Using BLR_MT might not be supported by all multithreaded BLAS
        # (MKL is known to work) but it is not something we can easily
        # check so we trust that the user knows what he/she is doing.
        if "+blr_mt" in self.spec:
            optf.append("-DBLR_MT")

        makefile_conf.extend(
            [
                "OPTC = {0}".format(" ".join(optc)),
                "OPTF = {0}".format(" ".join(optf)),
                "OPTL = {0}".format(" ".join(optl)),
            ]
        )

        if "+mpi" in self.spec:
            scalapack = self.spec["scalapack"].libs if not shared else LibraryList([])
            makefile_conf.extend(
                [
                    "CC = {0}".format(self.spec["mpi"].mpicc),
                    "FC = {0}".format(self.spec["mpi"].mpifc),
                    "FL = {0}".format(self.spec["mpi"].mpifc),
                    "SCALAP = %s" % scalapack.ld_flags,
                    "MUMPS_TYPE = par",
                ]
            )
        else:
            makefile_conf.extend(
                [
                    "CC = {0}".format(spack_cc),
                    "FC = {0}".format(spack_fc),
                    "FL = {0}".format(spack_fc),
                    "MUMPS_TYPE = seq",
                ]
            )
            # For sequential MUMPS, we need to link to a fake MPI lib
            extra_libs4mumps += ["-L$(topdir)/libseq", "-lmpiseq"]

        # TODO: change the value to the correct one according to the
        # compiler possible values are -DAdd_, -DAdd__ and/or -DUPPER
        if using_intel or using_oneapi or using_pgi or using_nvhpc or using_fj:
            # Intel, PGI, and Fujitsu Fortran compiler provides
            # the main() function so C examples linked with the Fortran
            # compiler require a hack defined by _DMAIN_COMP
            # (see examples/c_example.c)
            makefile_conf.append("CDEFS   = -DAdd_ -DMAIN_COMP")
        else:
            if not using_xlf:
                makefile_conf.append("CDEFS = -DAdd_")

        if "+shared" in self.spec:
            # All Mumps libraries will be linked with 'inject_libs'.
            inject_libs = []
            if "+mpi" in self.spec:
                inject_libs += [self.spec["scalapack"].libs.ld_flags]
            if "+ptscotch" in self.spec or "+scotch" in self.spec:
                inject_libs += [self.spec["scotch"].libs.ld_flags]
            if "+parmetis" in self.spec and "+metis" in self.spec:
                inject_libs += [
                    "-L%s -l%s -L%s -l%s"
                    % (
                        self.spec["parmetis"].prefix.lib,
                        "parmetis",
                        self.spec["metis"].prefix.lib,
                        "metis",
                    )
                ]
            elif "+metis" in self.spec:
                inject_libs += ["-L%s -l%s" % (self.spec["metis"].prefix.lib, "metis")]
            inject_libs += [lapack_blas.ld_flags]
            inject_libs = " ".join(inject_libs)

            if sys.platform == "darwin":
                # Building dylibs with mpif90 causes segfaults on 10.8 and
                # 10.10. Use gfortran. (Homebrew)
                makefile_conf.extend(
                    [
                        "LIBEXT=.dylib",
                        "AR=%s -dynamiclib -Wl,-install_name -Wl,%s/$(notdir $@)"
                        " -undefined dynamic_lookup %s -o "
                        % (os.environ["FC"], prefix.lib, inject_libs),
                        "RANLIB=echo",
                    ]
                )
            else:
                if using_xlf:
                    build_shared_flag = "qmkshrobj"
                else:
                    build_shared_flag = "shared"

                makefile_conf.extend(
                    [
                        "LIBEXT=.so",
                        "AR=link_cmd() { $(FL) -%s -Wl,-soname "
                        '-Wl,$(notdir $@) -o "$$@" %s; }; link_cmd '
                        % (build_shared_flag, inject_libs),
                        "RANLIB=ls",
                    ]
                )
                # When building libpord, read AR from Makefile.inc instead of
                # going through the make command line - this prevents various
                # problems with the substring "$$@".
                filter_file(r' AR="\$\(AR\)"', "", "Makefile")
                filter_file(
                    r"^(INCLUDES = -I../include)",
                    "\\1\ninclude ../../Makefile.inc",
                    join_path("PORD", "lib", "Makefile"),
                )

        else:
            makefile_conf.extend(["LIBEXT  = .a", "AR = ar vr ", "RANLIB = ranlib"])

        # The mumps.src-makefile.patch wants EXTRA_LIBS4MUMPS defined
        makefile_conf.extend(["EXTRA_LIBS4MUMPS = {0}".format(" ".join(extra_libs4mumps))])
        makefile_inc_template = join_path(os.path.dirname(self.module.__file__), "Makefile.inc")
        with open(makefile_inc_template, "r") as fh:
            makefile_conf.extend(fh.read().split("\n"))

        with working_dir("."):
            with open("Makefile.inc", "w") as fh:
                makefile_inc = "\n".join(makefile_conf)
                fh.write(makefile_inc)

    def flag_handler(self, name, flags):
        if name == "fflags":
            if self.spec.satisfies("%gcc@10:"):
                if flags is None:
                    flags = []
                flags.append("-fallow-argument-mismatch")

        return (flags, None, None)

    def install(self, spec, prefix):
        self.write_makefile_inc()

        # Build fails in parallel
        # That is why we split the builds of 's', 'c', 'd', and/or 'z' which
        # can be build one after the other, each using a parallel build.
        letters_variants = [
            ["s", "+float"],
            ["c", "+complex+float"],
            ["d", "+double"],
            ["z", "+complex+double"],
        ]
        for ltr, v in letters_variants:
            if v in spec:
                if self.spec.satisfies("@5.4:"):
                    make(ltr)
                else:
                    make(ltr + "examples")

        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)

        if "~mpi" in spec:
            lib_dsuffix = ".dylib" if sys.platform == "darwin" else ".so"
            lib_suffix = lib_dsuffix if "+shared" in spec else ".a"
            install("libseq/libmpiseq%s" % lib_suffix, prefix.lib)
            install(join_path("libseq", "*.h"), prefix.include)

        # FIXME: extend the tests to mpirun -np 2 when build with MPI
        # FIXME: use something like numdiff to compare output files
        # Note: In some cases, when 'mpi' is enabled, the examples below cannot
        # be run without 'mpirun', so we enabled the tests only if explicitly
        # requested with the Spack '--test' option.
        if self.run_tests:
            with working_dir("examples"):
                if "+float" in spec:
                    ssimpletest = Executable("./ssimpletest")
                    ssimpletest(input="input_simpletest_real")
                    if "+complex" in spec:
                        csimpletest = Executable("./csimpletest")
                        csimpletest(input="input_simpletest_cmplx")
                if "+double" in spec:
                    dsimpletest = Executable("./dsimpletest")
                    dsimpletest(input="input_simpletest_real")
                    if "+complex" in spec:
                        zsimpletest = Executable("./zsimpletest")
                        zsimpletest(input="input_simpletest_cmplx")

    @property
    def libs(self):
        component_libs = ["*mumps", "mumps_common", "pord"]
        return (
            find_libraries(
                ["lib" + comp for comp in component_libs],
                root=self.prefix.lib,
                shared=("+shared" in self.spec),
                recursive=False,
            )
            or None
        )
