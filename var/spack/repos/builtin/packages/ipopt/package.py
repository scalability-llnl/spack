# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ipopt(AutotoolsPackage):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
    software package for large-scale nonlinear optimization."""

    homepage = "https://github.com/coin-or/Ipopt"
    url = "https://github.com/coin-or/Ipopt/archive/refs/tags/releases/3.13.2.tar.gz"
    maintainers("chapman39", "tepperly")

    license("EPL-2.0")

    version("3.14.14", sha256="264d2d3291cd1cd2d0fa0ad583e0a18199e3b1378c3cb015b6c5600083f1e036")
    version("3.14.13", sha256="2afcb057e7cf8ed7e07f50ee0a4a06d2e4d39e0f964777e9dd55fe56199a5e0a")
    version("3.14.12", sha256="6b06cd6280d5ca52fc97ca95adaaddd43529e6e8637c274e21ee1072c3b4577f")
    version("3.14.9", sha256="e12eba451269ec30f4cf6e2acb8b35399f0d029c97dff10465416f5739c8cf7a")
    version("3.14.5", sha256="9ebbbbf14a64e998e3fba5d2662a8f9bd03f97b1406017e78ae54e5d105ae932")
    version("3.14.4", sha256="60865150b6fad19c5968395b57ff4a0892380125646c3afa2a714926f5ac9487")
    version("3.14.3", sha256="29bbf8bbadd5f2965e18e33451723d1fed0c42b14f6493396cf53a05cdfd2c09")
    version("3.14.2", sha256="3ec6776b9a1ed8895f662bfc9939b067722770297be78ca4d6dc1cb42557da62")
    version("3.14.1", sha256="afa37bbb0d91003c58284113717dc304718a1f236c97fe097dfab1672cb879c6")
    version("3.14.0", sha256="9bed72a5456ef37f1b95746c932986e6664eb70b983d4fab61cf8aa811facdf1")
    version("3.13.4", sha256="1fdd0f8ea637856d66b1ebdd7d52ad1b8b8c1142d1a4ce0976b200ab280e5683")
    version("3.13.3", sha256="86354b36c691e6cd6b8049218519923ab0ce8a6f0a432c2c0de605191f2d4a1c")
    version("3.13.2", sha256="891ab9e9c7db29fc8ac5c779ccec6313301098de7bbf735ca230cd5544c49496")
    version("3.13.1", sha256="64fc63a3fe27cf5efaf17ebee861f7db5bf70aacf9c316c0d37e4beb4eb72e11")
    version("3.13.0", sha256="dc392396be28c4a0d49bfab399320cb3f70db5b8f090028a883d826a47744ecf")
    version("3.12.13", sha256="ab8b9457dc6c7240a45e74b4a3851821ccafc2927cfa5c8998e95941d67a94d0")
    version("3.12.12", sha256="7587c21f48bc85ae3a84d544fc67cff0d61c41bf2168879f46f7500ee5cabf73")
    version("3.12.11", sha256="d2c402b9e760f8a20314324ff967b8a3dee73d5bcf3739dd8c06a9f2e99da927")
    version("3.12.10", sha256="dfd29dc95ec815e1ff0a3b7dc86ecc8944b24977e40724c35dac25aa192ac3cd")
    version("3.12.9", sha256="af2b65338d388c9b5528cc3952ecf8d943c46564b6705087d964d0fcdb79a552")
    version("3.12.8", sha256="fa120112cd3722927f4c9ab3fb7eff9a25638ea28d467874854779a81c7cdde8")
    version("3.12.7", sha256="f20017c8e880ec1e55d3efbb615209dfe28a58d0ec5147ce9490fe90afe9d445")
    version("3.12.6", sha256="6e7253705d5c2d1e9bab2dad9f6b0658439cc83f1c51b923aac056bd26bc0f6f")
    version("3.12.5", sha256="0f0a3a93c1bf46f588b2cdc4989bb3d8b646890aefbe531606c88f143bcf7bd2")
    version("3.12.4", sha256="75e8ea3b0246a56e09ad78a4a54d0986b5be28d547ae808ea6ee2055fe2ae4aa")
    version("3.12.3", sha256="fb828fd94ede8c529e29e562947172ceff2052126f6bd91d9a2bfae96fa7bfad")
    version("3.12.2", sha256="0fa4498e61b301a65ba395bcecb2c1c1df49e56d6c6d109f0f26a0f75e3f43ee")
    version("3.12.1", sha256="bde8c415136bb38d5a3c5935757399760c6cabf67e9362702e59ab6027f030ec")
    version("3.12.0", sha256="b42f44eb53540205ede4584cced5d88a7b3ec2f1fac6e173a105496307e273a0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("coinhsl", default=False, description="Build with Coin Harwell Subroutine Libraries")
    variant("metis", default=False, description="Build with METIS partitioning support")
    variant("debug", default=False, description="Build debug instead of optimized version")
    variant("mumps", default=True, description="Build with support for linear solver MUMPS")
    variant("java", default=False, description="Include Java support")

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkgconfig", type="build")
    depends_on("mumps+double", when="+mumps")
    depends_on("coinhsl", when="+coinhsl")
    depends_on("metis@4.0:", when="+metis")

    # Must have at least one linear solver available!
    conflicts("~mumps", when="~coinhsl")

    patch("ipopt_ppc_build.patch", when="arch=ppc64le")
    patch("ipopt_mumps_mpi_comm_option.patch", when="+mumps")

    flag_handler = build_system_flags
    build_directory = "spack-build"

    # IPOPT does not build correctly in parallel on OS X
    parallel = False

    def configure_args(self):
        spec = self.spec
        # Dependency directories
        blas_dir = spec["blas"].prefix
        lapack_dir = spec["lapack"].prefix

        blas_lib = spec["blas"].libs.ld_flags
        lapack_lib = spec["lapack"].libs.ld_flags

        args = ["--prefix=%s" % self.prefix, "--enable-shared", "coin_skip_warn_cxxflags=yes"]

        if spec.satisfies("@:3.12.13"):
            args.extend(
                [
                    "--with-lapack-lib={0}".format(lapack_lib),
                    "--with-lapack-incdir={0}".format(lapack_dir.include),
                    "--with-blas-lib={0}".format(blas_lib),
                    "--with-blas-incdir={0}".format(blas_dir.include),
                ]
            )
        else:
            args.extend(["--with-lapack-lflags={0} {1}".format(lapack_lib, blas_lib)])

        if spec.satisfies("+mumps"):
            mumps_dir = spec["mumps"].prefix
            mumps_flags = "-ldmumps -lmumps_common -lpord"
            if "^mumps~mpi" in spec:
                mumps_flags = mumps_flags + "-lmpiseq"
            mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags
            if spec.satisfies("@:3.12.13"):
                args.extend(
                    [
                        "--with-mumps-incdir=%s" % mumps_dir.include,
                        "--with-mumps-lib=%s" % mumps_libcmd,
                    ]
                )
            else:
                args.extend(
                    [
                        "--with-mumps",
                        "--with-mumps-lflags=%s" % mumps_libcmd,
                        "--with-mumps-cflags=%s" % mumps_dir.include,
                    ]
                )
                if "^mumps+mpi" in spec:
                    args.extend(["--disable-mpiinit"])

        if spec.satisfies("+coinhsl"):
            hsl_ld_flags = "-ldl {0}".format(spec["coinhsl"].libs.ld_flags)

            if spec.satisfies("^coinhsl+blas"):
                hsl_ld_flags += " {0}".format(spec["blas"].libs.ld_flags)

            if spec.satisfies("@:3.12.13"):
                args.extend(
                    [
                        "--with-hsl-lib=%s" % hsl_ld_flags,
                        "--with-hsl-incdir=%s" % spec["coinhsl"].prefix.include,
                    ]
                )
            else:
                args.extend(
                    [
                        "--with-hsl",
                        "--with-hsl-lflags=%s" % hsl_ld_flags,
                        "--with-hsl-cflags=%s" % spec["coinhsl"].prefix.include,
                    ]
                )
        else:
            # Fixes dynamic linking errors relating to failure to find hsllib.so
            if spec.satisfies("@3.13:"):
                args.extend(["--without-hsl"])

        if spec.satisfies("+metis"):
            if spec.satisfies("@:3.12.13"):
                args.extend(
                    [
                        "--with-metis-lib=%s" % spec["metis"].libs.ld_flags,
                        "--with-metis-incdir=%s" % spec["metis"].prefix.include,
                    ]
                )

        if spec.satisfies("+java"):
            args.extend(["--enable-java"])
        else:
            args.extend(["--disable-java"])

        # The IPOPT configure file states that '--enable-debug' implies
        # '--disable-shared', but adding '--enable-shared' overrides
        # '--disable-shared' and builds a shared library with debug symbols
        if spec.satisfies("+debug"):
            args.append("--enable-debug")
        else:
            args.append("--disable-debug")

        return args
