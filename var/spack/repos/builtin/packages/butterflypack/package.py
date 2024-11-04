# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Butterflypack(CMakePackage):
    """ButterflyPACK is a mathematical software for rapidly solving
    large-scale dense linear systems that exhibit off-diagonal rank-deficiency.
    These systems arise frequently from boundary element methods, or
    factorization phases in finite-difference/finite-element methods.
    ButterflyPACK relies on low-rank or butterfly formats under Hierarchical
    matrix, HODLR or other hierarchically nested frameworks to compress,
    factor and solve the linear system in quasi-linear time. The
    computationally most intensive phase, factorization, is accelerated via
    randomized linear algebras. The butterfly format, originally inspired by
    the butterfly data flow in fast Fourier Transform, is a linear algebra tool
    well-suited for compressing matrices arising from high-frequency wave
    equations or highly oscillatory integral operators."""

    homepage = "https://github.com/liuyangzhuan/ButterflyPACK"
    git = "https://github.com/liuyangzhuan/ButterflyPACK.git"
    url = "https://github.com/liuyangzhuan/ButterflyPACK/archive/v2.2.0.tar.gz"
    maintainers("liuyangzhuan")

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")
    version("2.4.0", sha256="12d04e7101b2c8292b5c62d9f42b5cd1e8a3c5af639d2665596e3e4255fd0804")
    version("2.2.2", sha256="73f67073e4291877f1eee19483a8a7b3c761eaf79a75805d52105ceedead85ea")
    version("2.2.1", sha256="4cedc2896a6b368773ce4f9003aa2c0230baf56a4464a6b899a155e01406a232")
    version("2.2.0", sha256="1ce5b8461b3c4f488cee6396419e8a6f0a1bcf95254f24d7c27bfa53b391c30b")
    version("2.1.1", sha256="0d4a1ce540c84de37e4398f72ecf685ea0c4eabceba13015add5b445a4ca3a15")
    version("2.1.0", sha256="ac76cc8d431797c1a3641b23124e3de5eb8c3a3afb71c336e7ba69c6cdf150ef")
    version("2.0.0", sha256="84f0e5ac40997409f3c80324238a07f9c700a1263b84140ed97275d67b577b80")
    version("1.2.1", sha256="cd61b0e033f55a932f13d9902e28a7abbf029c279cec9ab1b2a063525d036fa2")
    version("1.2.0", sha256="870b8acd826eb414dc38fa25e22c9c09ddeb5ca595b1dfdaa1fd65ae964d4e94")
    version("1.1.0", sha256="0e6fd0f9e27b3ee8a273dc52f4d24b8737e7279dc26d461ef5658b317215f1dc")
    version("1.0.3", sha256="acf9bc98dd7fea31ab73756b68b3333228b53ab0e85400a8250fcc749a1a6656")
    version("1.0.1", sha256="e8ada37466a19f49e13456b150700d4c3afaad2ddbe3678f4e933f9d556a24a5")
    version("1.0.0", sha256="86c5eb09a18522367d63ce2bacf67ca1c9813ef351a1443baaab3c53f0d77232")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("openmp", default=True, description="add OpenMP support")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")
    depends_on("arpack-ng")
    depends_on("sed", type="build")

    conflicts("%gcc@:7", when="@2.2.1:")

    # https://github.com/spack/spack/issues/31818
    patch("qopenmp-for-oneapi.patch", when="@2.1.1 %oneapi")

    patch("longline.patch", when="%fj")
    patch("fjfortran.patch", when="%fj")
    patch("isnan.patch", when="%fj")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            "-DTPL_BLAS_LIBRARIES=%s" % spec["blas"].libs.joined(";"),
            "-DTPL_LAPACK_LIBRARIES=%s" % spec["lapack"].libs.joined(";"),
            "-DTPL_SCALAPACK_LIBRARIES=%s" % spec["scalapack"].libs.joined(";"),
            "-DTPL_ARPACK_LIBRARIES=%s" % spec["arpack-ng"].libs.joined(";"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        args.append("-Denable_openmp=%s" % ("ON" if "+openmp" in spec else "OFF"))
        if spec.satisfies("%cce"):
            # Assume the proper Cray CCE module (cce) is loaded:
            craylibs_var = "CRAYLIBS_" + str(spec.target.family).upper()
            craylibs_path = env.get(craylibs_var, None)
            if not craylibs_path:
                raise InstallError(
                    f"The environment variable {craylibs_var} is not defined.\n"
                    "\tMake sure the 'cce' module is in the compiler spec."
                )
            env.setdefault("LDFLAGS", "")
            env["LDFLAGS"] += " -Wl,-rpath," + craylibs_path

        return args
