# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


class Scotch(CMakePackage, MakefilePackage):
    """Scotch is a software package for graph and mesh/hypergraph
    partitioning, graph clustering, and sparse matrix ordering.
    """

    homepage = "https://gitlab.inria.fr/scotch/scotch"
    git = "https://gitlab.inria.fr/scotch/scotch.git"
    url = "https://gitlab.inria.fr/scotch/scotch/-/archive/v7.0.1/scotch-v7.0.1.tar.gz"
    list_url = "https://gforge.inria.fr/frs/?group_id=248"

    maintainers("pghysels")

    version("7.0.4", sha256="8ef4719d6a3356e9c4ca7fefd7e2ac40deb69779a5c116f44da75d13b3d2c2c3")
    version("7.0.3", sha256="5b5351f0ffd6fcae9ae7eafeccaa5a25602845b9ffd1afb104db932dd4d4f3c5")
    version("7.0.1", sha256="0618e9bc33c02172ea7351600fce4fccd32fe00b3359c4aabb5e415f17c06fed")
    version("6.1.3", sha256="4e54f056199e6c23d46581d448fcfe2285987e5554a0aa527f7931684ef2809e")
    version("6.1.2", sha256="9c2c75c75f716914a2bd1c15dffac0e29a2f8069b2df1ad2b6207c984b699450")
    version("6.1.1", sha256="14daf151399fc67f83fd3ff2933854f5e8d2207c7d35dd66a05660bf0bbd583c")
    version("6.1.0", sha256="4fe537f608f0fe39ec78807f90203f9cca1181deb16bfa93b7d4cd440e01bbd1")
    version("6.0.10", sha256="e5542b6102b5616f0f5c6619e3e9d52f9d0e48cb991e9b30670f598deeac0553")
    version("6.0.9", sha256="b9bc86c50b65781eb416663e938d57555373c2517ea8b9acf680fd3acde0cb0c")
    version("6.0.8", sha256="9457c1e7c30f073686cc217345b5a96af4166d6abbf148af84cdbab4e144b299")
    version("6.0.6", sha256="e932b4c04636fcf5d21b9a76376868de052c9b000bdaf96f8967dcec61bdaa10")
    version("6.0.5a", sha256="5b21b95e33acd5409d682fa7253cefbdffa8db82875549476c006d8cbe7c556f")
    version("6.0.4", sha256="f53f4d71a8345ba15e2dd4e102a35fd83915abf50ea73e1bf6efe1bc2b4220c7")
    version("6.0.3", sha256="6461cc9f28319a9dbe6cc10e28c0cbe90b4b25e205723c3edcde9a3ff974d6d8")
    version("6.0.0", sha256="8206127d038bda868dda5c5a7f60ef8224f2e368298fbb01bf13fa250e378dd4")
    version("5.1.10b", sha256="54c9e7fafefd49d8b2017d179d4f11a655abe10365961583baaddc4eeb6a9add")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    build_system(conditional("cmake", when="@7:"), "makefile", default="cmake")
    variant("threads", default=True, description="use POSIX Pthreads within Scotch and PT-Scotch")
    variant(
        "mpi_thread",
        default=False,
        description="use multi-threaded algorithms in conjunction with MPI",
    )
    variant("mpi", default=True, description="Compile parallel libraries")
    variant("compression", default=True, description="May use compressed files")
    variant("esmumps", default=False, description="Compile esmumps (needed by mumps)")
    variant("shared", default=True, description="Build a shared version of the library")
    variant(
        "metis", default=False, description="Expose vendored METIS/ParMETIS libraries and wrappers"
    )
    variant("int64", default=False, description="Use int64_t for SCOTCH_Num typedef")
    variant("noarch", default=False, description="Unset SPACK_TARGET_ARGS")
    variant(
        "link_error_lib",
        default=False,
        when="@7.0.1",
        description="Link error handling library to libscotch/libptscotch",
    )

    # Does not build with flex 2.6.[23]
    depends_on("flex@:2.6.1,2.6.4:", type="build")
    depends_on("bison@3.4:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("zlib-api", when="+compression")

    # Version-specific patches
    patch("nonthreaded-6.0.4.patch", when="@6.0.4")
    patch("esmumps-ldflags-6.0.4.patch", when="@6.0.4")
    patch("metis-headers-6.0.4.patch", when="@6.0.4")

    patch("libscotchmetis-return-6.0.5a.patch", when="@6.0.5a")
    patch("libscotch-scotcherr-link-7.0.1.patch", when="@7.0.1 +link_error_lib")

    # Avoid OpenMPI segfaults by using MPI_Comm_F2C for parmetis communicator
    patch("parmetis-mpi.patch", when="@6.1.1:7.0.3 +metis ^openmpi")

    # Vendored dependency of METIS/ParMETIS conflicts with standard
    # installations
    conflicts("metis", when="+metis")
    conflicts("parmetis", when="+metis")

    parallel = False

    # NOTE: Versions of Scotch up to version 6.0.0 don't include support for
    # building with 'esmumps' in their default packages.  In order to enable
    # support for this feature, we must grab the 'esmumps' enabled archives
    # from the Scotch hosting site.  These alternative archives include a
    # superset of the behavior in their default counterparts, so we choose to
    # always grab these versions for older Scotch versions for simplicity.
    @when("@:6.0.0")
    def url_for_version(self, version):
        url = "https://gforge.inria.fr/frs/download.php/latestfile/298/scotch_{0}_esmumps.tar.gz"
        return url.format(version)

    @property
    def libs(self):
        shared = "+shared" in self.spec
        libraries = ["libscotch", "libscotcherr"]
        zlibs = []

        if "+mpi" in self.spec:
            libraries = ["libptscotch", "libptscotcherr"] + libraries

        if "+esmumps" in self.spec:
            if "~mpi" in self.spec or self.spec.version >= Version("7.0.0"):
                libraries = ["libesmumps"] + libraries
            else:
                libraries = ["libptesmumps"] + libraries

        scotchlibs = find_libraries(libraries, root=self.prefix, recursive=True, shared=shared)
        if "+compression" in self.spec:
            zlibs = self.spec["zlib-api"].libs

        return scotchlibs + zlibs


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("BUILD_LIBSCOTCHMETIS", "metis"),
            self.define_from_variant("INSTALL_METIS_HEADERS", "metis"),
            self.define_from_variant("BUILD_LIBESMUMPS", "esmumps"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_PTSCOTCH", "mpi"),
            self.define_from_variant("THREADS", "threads"),
            self.define_from_variant("MPI_THREAD_MULTIPLE", "mpi_thread"),
        ]

        if "+int64" in spec:
            args.append("-DINTSIZE=64")

        return args

    @when("+noarch")
    def setup_build_environment(self, env):
        env.unset("SPACK_TARGET_ARGS")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    build_directory = "src"

    def edit(self, pkg, spec, prefix):
        makefile_inc = []
        cflags = ["-O3", "-DCOMMON_RANDOM_FIXED_SEED", "-DSCOTCH_DETERMINISTIC", "-DSCOTCH_RENAME"]

        if "+int64" in self.spec:
            # SCOTCH_Num typedef: size of integers in arguments
            cflags.append("-DINTSIZE64")
            cflags.append("-DIDXSIZE64")  # SCOTCH_Idx typedef: indices for addressing
        else:
            cflags.append("-DIDXSIZE32")  # SCOTCH_Idx typedef: indices for addressing

        if self.spec.satisfies("platform=darwin"):
            cflags.extend(["-Drestrict=__restrict"])

        if "~metis" in self.spec:
            # Scotch requires METIS to build, but includes its own patched,
            # vendored dependency. Prefix its internal symbols so they won't
            # conflict with another installation.
            cflags.append("-DSCOTCH_METIS_PREFIX")

        # Library Build Type #
        if "+shared" in self.spec:
            if self.spec.satisfies("platform=darwin"):
                makefile_inc.extend(
                    [
                        "LIB       = .dylib",
                        "CLIBFLAGS = -dynamiclib {0}".format(pkg.compiler.cc_pic_flag),
                        "RANLIB    = echo",
                        "AR        = $(CC)",
                        (
                            "ARFLAGS = -dynamiclib $(LDFLAGS) "
                            "-Wl,-install_name -Wl,%s/$(notdir $@) "
                            "-undefined dynamic_lookup -o "
                        )
                        % prefix.lib,
                    ]
                )
            else:
                makefile_inc.extend(
                    [
                        "LIB       = .so",
                        "CLIBFLAGS = -shared {0}".format(pkg.compiler.cc_pic_flag),
                        "RANLIB    = echo",
                        "AR        = $(CC)",
                        "ARFLAGS   = -shared $(LDFLAGS) -o",
                    ]
                )
            cflags.append(pkg.compiler.cc_pic_flag)
        else:
            makefile_inc.extend(
                [
                    "LIB       = .a",
                    "CLIBFLAGS = ",
                    "RANLIB    = ranlib",
                    "AR        = ar",
                    "ARFLAGS   = -ruv ",
                ]
            )

        # Compiler-Specific Options #

        if pkg.compiler.name == "gcc":
            cflags.append("-Drestrict=__restrict")
        elif pkg.compiler.name == "intel":
            cflags.append("-Drestrict=")

        mpicc_path = self.spec["mpi"].mpicc if "+mpi" in self.spec else "mpicc"
        makefile_inc.append("CCS       = $(CC)")
        makefile_inc.append("CCP       = %s" % mpicc_path)
        makefile_inc.append("CCD       = $(CCS)")

        # Extra Features #

        ldflags = []

        if "+compression" in self.spec:
            cflags.append("-DCOMMON_FILE_COMPRESS_GZ")
            ldflags.append(" {0} ".format(self.spec["zlib-api"].libs.joined()))

        cflags.append("-DCOMMON_PTHREAD")

        # NOTE: bg-q platform needs -lpthread (and not -pthread)
        # otherwise we get illegal instruction error during runtime
        if self.spec.satisfies("platform=darwin"):
            cflags.append("-DCOMMON_PTHREAD_BARRIER")
            ldflags.append("-lm -pthread")
        else:
            ldflags.append("-lm -lrt -pthread")

        makefile_inc.append("LDFLAGS   = %s" % " ".join(ldflags))

        # General Features #

        flex_path = self.spec["flex"].command.path
        bison_path = self.spec["bison"].command.path
        makefile_inc.extend(
            [
                "EXE       =",
                "OBJ       = .o",
                "MAKE      = make",
                "CAT       = cat",
                "LN        = ln",
                "MKDIR     = mkdir",
                "MV        = mv",
                "CP        = cp",
                "CFLAGS    = %s" % " ".join(cflags),
                "LEX       = %s -Pscotchyy -olex.yy.c" % flex_path,
                "YACC      = %s -pscotchyy -y -b y" % bison_path,
                "prefix    = %s" % self.prefix,
            ]
        )

        with working_dir("src"):
            with open("Makefile.inc", "w") as fh:
                fh.write("\n".join(makefile_inc))

    @property
    def build_targets(self):
        targets = ["scotch"]
        if "+mpi" in self.spec:
            targets.append("ptscotch")

        if self.spec.version >= Version("6.0.0"):
            if "+esmumps" in self.spec:
                targets.append("esmumps")
                if "+mpi" in self.spec:
                    targets.append("ptesmumps")
        return targets
