# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pumi(CMakePackage):
    """SCOREC RPI's Parallel Unstructured Mesh Infrastructure (PUMI).
    An efficient distributed mesh data structure and methods to support
    parallel adaptive analysis including general mesh-based operations,
    such as mesh entity creation/deletion, adjacency and geometric
    classification, iterators, arbitrary (field) data attachable to mesh
    entities, efficient communication involving entities duplicated
    across multiple tasks, migration of mesh entities between tasks,
    and dynamic load balancing."""

    homepage = "https://www.scorec.rpi.edu/pumi"
    git = "https://github.com/SCOREC/core.git"

    maintainers("cwsmith")

    tags = ["e4s"]

    license("BSD-3-Clause")

    # We will use the scorec/core master branch as the 'nightly' version
    # of pumi in spack.  The master branch is more stable than the
    # scorec/core develop branch and we prefer not to expose spack users
    # to the added instability.
    version("master", submodules=True, branch="master")
    version(
        "2.2.8", submodules=True, commit="736bb87ccd8db51fc499a1b91e53717a88841b1f"
    )  # tag 2.2.8
    version(
        "2.2.7", submodules=True, commit="a295720d7b4828282484f2b78bac1f6504512de4"
    )  # tag 2.2.7
    version("2.2.6", commit="4dd330e960b1921ae0d8d4039b8de8680a20d993")  # tag 2.2.6
    version("2.2.5", commit="73c16eae073b179e45ec625a5abe4915bc589af2")  # tag 2.2.5
    version("2.2.4", commit="8072fdbafd53e0c9a63248a269f4cce5000a4a8e")  # tag 2.2.4
    version("2.2.3", commit="d200cb366813695d0f18b514d8d8ecc382cb79fc")  # tag 2.2.3
    version("2.2.2", commit="bc34e3f7cfd8ab314968510c71486b140223a68f")  # tag 2.2.2
    version("2.2.1", commit="cd826205db21b8439026db1f6af61a8ed4a18564")  # tag 2.2.1
    version("2.2.0", commit="8c7e6f13943893b2bc1ece15003e4869a0e9634f")  # tag 2.2.0
    version("2.1.0", commit="840fbf6ec49a63aeaa3945f11ddb224f6055ac9f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("int64", default=False, description="Enable 64bit mesh entity ids")
    variant("shared", default=False, description="Build shared libraries")
    variant("zoltan", default=False, description="Enable Zoltan Features")
    variant("fortran", default=False, description="Enable FORTRAN interface")
    variant("testing", default=False, description="Enable all tests")
    variant(
        "simmodsuite",
        default="none",
        values=("none", "base", "kernels", "full"),
        description="Enable Simmetrix SimModSuite Support: 'base' enables "
        "the minimum set of functionality, 'kernels' adds CAD kernel "
        "support to 'base', and 'full' enables all functionality.",
    )
    variant(
        "simmodsuite_version_check",
        default=True,
        description="Enable check of Simmetrix SimModSuite version. "
        "Disable the check for testing new versions.",
    )

    depends_on("cxx", type="build")
    depends_on("c", type="build")
    depends_on("fortran", type="build", when="+fortran")

    depends_on("mpi")
    depends_on("cmake@3:", type="build")
    depends_on("zoltan", when="+zoltan")
    depends_on("zoltan+int64", when="+zoltan+int64")
    simbase = "+base"
    simkernels = simbase + "+parasolid+acis+discrete"
    simfull = (
        simkernels
        + "+abstract+adv+advmodel\
                            +import+paralleladapt+parallelmesh"
    )
    depends_on("simmetrix-simmodsuite" + simbase, when="simmodsuite=base")
    depends_on("simmetrix-simmodsuite" + simkernels, when="simmodsuite=kernels")
    depends_on("simmetrix-simmodsuite" + simfull, when="simmodsuite=full")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DSCOREC_CXX_WARNINGS=OFF",
            self.define_from_variant("ENABLE_ZOLTAN", "zoltan"),
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PUMI_FORTRAN_INTERFACE", "fortran"),
            "-DMDS_ID_TYPE=%s" % ("long" if "+int64" in spec else "int"),
            "-DSKIP_SIMMETRIX_VERSION_CHECK=%s"
            % ("ON" if "~simmodsuite_version_check" in spec else "OFF"),
            self.define_from_variant("IS_TESTING", "testing"),
            "-DMESHES=%s" % join_path(self.stage.source_path, "pumi-meshes"),
        ]
        if spec.satisfies("fortran"):
            args += ["-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc]
        if spec.satisfies("@2.2.3"):
            args += ["-DCMAKE_CXX_STANDARD=11"]
        if self.spec.variants["simmodsuite"].value != "none":
            args.append("-DENABLE_SIMMETRIX=ON")
            mpi_id = spec["mpi"].name + spec["mpi"].version.up_to(1).string
            args.append("-DSIM_MPI=" + mpi_id)
            if self.spec.variants["simmodsuite"].value in ["kernels", "full"]:
                args.append("-DENABLE_SIMMETRIX=ON")
                args.append("-DSIM_PARASOLID=ON")
                args.append("-DSIM_ACIS=ON")
                args.append("-DSIM_DISCRETE=ON")
        return args

    def test_partition(self):
        """Testing pumi mesh partitioning"""
        if self.spec.satisfies("@:2.2.6"):
            raise SkipTest("Package must be installed as version @2.2.7 or later")

        options = [
            "-n",
            "2",
            join_path(self.prefix.bin, "split"),
            join_path(self.prefix.share.testdata, "pipe.dmg"),
            join_path(self.prefix.share.testdata, "pipe.smb"),
            "pipe_2_.smb",
            "2",
        ]
        exe = which(self.spec["mpi"].prefix.bin.mpiexec)
        out = exe(*options, output=str.split, error=str.split)
        assert "mesh pipe_2_.smb written" in out

    def test_refine(self):
        """Testing pumi uniform mesh refinement"""
        if self.spec.satisfies("@:2.2.6"):
            raise SkipTest("Package must be installed as version @2.2.7 or later")

        options = [
            join_path(self.prefix.share.testdata, "pipe.dmg"),
            join_path(self.prefix.share.testdata, "pipe.smb"),
            "pipe_unif.smb",
        ]
        exe = which(self.prefix.bin.uniform)
        out = exe(*options, output=str.split, error=str.split)
        assert "mesh pipe_unif.smb written" in out
