# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class OsuMicroBenchmarks(AutotoolsPackage, CudaPackage, ROCmPackage):
    """The Ohio MicroBenchmark suite is a collection of independent MPI
    message passing performance microbenchmarks developed and written at
    The Ohio State University. It includes traditional benchmarks and
    performance measures such as latency, bandwidth and host overhead
    and can be used for both traditional and GPU-enhanced nodes."""

    homepage = "https://mvapich.cse.ohio-state.edu/benchmarks/"
    url = "https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.0.1.tar.gz"

    maintainers("natshineman", "harisubramoni", "MatthewLieber")

    version("7.4", sha256="1edd0c2efa61999409bfb28740a7f39689a5b42b1a1b4c66d1656e5637f7cefc")
    version("7.3", sha256="8fa25b8aaa34e4b07ab3a4f30b7690ab46b038b08d204a853a9b6aa7bdb02f2f")
    version("7.2", sha256="1a4e1f2aab0e65404b3414e23bd46616184b69b6231ce9313d9c630bd6e633c1")
    version("7.1-1", sha256="85f4dd8be1df31255e232852769ae5b82e87a5fb14be2f8eba1ae9de8ffe391a")
    version("7.1", sha256="2c4c931ecaf19e8ab72a393ee732e25743208c9a58fa50023e3fac47064292cc")
    version("7.0.1", sha256="04954aea082ba1b90a461ffab82a3cee43fe2d5a60fed99f5cb4585ac7da8c66")
    version("7.0", sha256="958e2faf9f3a4a244d7baac3469acee0375447decff6026c442552f0f6f08306")
    version("6.2", sha256="bb9dbc87dcf8ec6785977a61f6fceee8febf1a682488eaab4c58cf50e4fa985f")
    version("6.1", sha256="ecccedc868264f75db4d9529af79005419a2775113c7fae8f4e4a8434362e4a7")
    version("6.0", sha256="309fb7583ff54562343b0e0df1eebde3fc245191e183be362f031ac74f4ab542")
    version("5.9", sha256="d619740a1c2cc7c02a9763931546b320d0fa4093c415ff3873c2958e121c0609")
    version(
        "5.7.1",
        sha256="cb5ce4e2e68ed012d9952e96ef880a802058c87a1d840a2093b19bddc7faa165",
        url="https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.7.1.tgz",
    )
    version("5.7", sha256="1470ebe00eb6ca7f160b2c1efda57ca0fb26b5c4c61148a3f17e8e79fbf34590")
    version("5.6.3", sha256="c5eaa8c5b086bde8514fa4cac345d66b397e02283bc06e44cb6402268a60aeb8")
    version("5.6.2", sha256="2ecb90abd85398786823c0716d92448d7094657d3f017c65d270ffe39afc7b95")
    version("5.6.1", sha256="943c426a653a6c56200193d747755efaa4c4e6f23b3571b0e3ef81ecd21b1063")
    version("5.5", sha256="1e5a4ae5ef2b03143a815b21fefc23373c1b079cc163c2fa1ed1e0c9b83c28ad")
    version("5.4", sha256="e1ca762e13a07205a59b59ad85e85ce0f826b70f76fd555ce5568efb1f2a8f33")
    version("5.3", sha256="d7b3ad4bee48ac32f5bef39650a88f8f2c23a3050b17130c63966283edced89b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("mpi")
    variant("papi", description="Enable/Disable support for papi", default=False)
    variant("graphing", description="Enable/Disable support for graphing", default=False)
    depends_on("papi", when="+papi")
    depends_on("gnuplot", when="+graphing")
    depends_on("imagemagick", when="+graphing")

    def configure_args(self):
        spec = self.spec
        config_args = ["CC=%s" % spec["mpi"].mpicc, "CXX=%s" % spec["mpi"].mpicxx]

        if "+cuda" in spec:
            config_args.extend(["--enable-cuda", "--with-cuda=%s" % spec["cuda"].prefix])
            cuda_arch = spec.variants["cuda_arch"].value
            if "none" not in cuda_arch:
                config_args.append("NVCCFLAGS=" + " ".join(self.cuda_flags(cuda_arch)))

        if "+rocm" in spec:
            config_args.extend(["--enable-rocm", "--with-rocm=%s" % spec["hip"].prefix])
            rocm_arch = spec.variants["amdgpu_target"].value
            if "none" not in rocm_arch:
                config_args.append("HCC_AMDGPU_TARGET=" + " ".join(self.hip_flags(rocm_arch)))

        if "+papi" in spec:
            config_args.extend(["--enable-papi", "--with-papi=%s" % spec["papi"].prefix])
        if "+graphing" in spec:
            config_args.extend(
                [
                    "--with-convert=%s/bin" % spec["imagemagick"].prefix,
                    "--with-gnuplot=%s/bin" % spec["gnuplot"].prefix,
                ]
            )

        # librt not available on darwin (and not required)
        if not sys.platform == "darwin":
            config_args.append("LDFLAGS=-lrt")
        return config_args

    def setup_run_environment(self, env):
        mpidir = join_path(self.prefix.libexec, "osu-micro-benchmarks", "mpi")
        env.prepend_path("PATH", join_path(mpidir, "startup"))
        env.prepend_path("PATH", join_path(mpidir, "pt2pt"))
        env.prepend_path("PATH", join_path(mpidir, "one-sided"))
        env.prepend_path("PATH", join_path(mpidir, "collective"))
