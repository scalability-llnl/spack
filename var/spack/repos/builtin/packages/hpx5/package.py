# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hpx5(AutotoolsPackage):
    """The HPX-5 Runtime System. HPX-5 (High Performance ParalleX) is an
    open source, portable, performance-oriented runtime developed at
    CREST (Indiana University). HPX-5 provides a distributed
    programming model allowing programs to run unmodified on systems
    from a single SMP to large clusters and supercomputers with
    thousands of nodes. HPX-5 supports a wide variety of Intel and ARM
    platforms. It is being used by a broad range of scientific
    applications enabling scientists to write code that performs and
    scales better than contemporary runtimes."""

    homepage = "http://hpx.crest.iu.edu"
    url = "https://github.com/adk9/hpx5/archive/v3.1.0.tar.gz"

    version("4.1.0", sha256="3f01009f5e517c8dfca266dabb49894d688db5adce09608fb1c877263605a9f8")
    version("4.0.0", sha256="e35b1161566a65ffbd875c1413ea97a84be0c7b528a3dee99f5e250b2aecbd19")
    version("3.1.0", sha256="359d457a26b87abb415605911d791ce0ff6edbb064bc40b0f830960f8f612b84")
    version("3.0.0", sha256="10f14ba198a32787cee05962e346bafb922f74a5135fb09a1ba8c32a1e942800")
    version("2.2.0", sha256="e34c7513a287d517e67cce5aa3011474c48718e7860c3860ba1290c702be28a8")
    version("2.1.0", sha256="675826f669eeb3eab40947715af8c8495e2b3d299223372431dc01c1f7d5d616")
    version("2.0.0", sha256="0278728557b6684aeb86228f44d548ac809302f05a0b9c8b433cdd157629e384")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Don't second-guess what compiler we are using on Cray
    patch("configure.patch", when="@4.0.0")

    variant("cuda", default=False, description="Enable CUDA support")
    variant("cxx11", default=False, description="Enable C++11 hpx++ interface")
    variant("debug", default=False, description="Build debug version of HPX-5")
    variant(
        "instrumentation",
        default=False,
        description="Enable instrumentation (may affect performance)",
    )
    variant("metis", default=False, description="Enable METIS support")
    variant("mpi", default=False, description="Enable MPI support")
    variant("opencl", default=False, description="Enable OpenCL support")
    variant("photon", default=False, description="Enable Photon support")
    variant("pic", default=True, description="Produce position-independent code")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("hwloc")
    depends_on("hwloc +cuda", when="+cuda")
    # Note: We could disable CUDA support via "hwloc ~cuda"
    depends_on("jemalloc")
    # depends_on("libffi")
    depends_on("libtool", type="build")
    # depends_on("lz4")   # hpx5 always builds its own lz4
    depends_on("m4", type="build")
    depends_on("metis", when="+metis")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+photon")
    depends_on("opencl", when="+opencl")
    # depends_on("papi")
    depends_on("pkgconfig", type="build")

    configure_directory = "hpx"
    build_directory = "spack-build"

    def configure_args(self):
        spec = self.spec
        args = [
            "--enable-agas",  # make this a variant?
            "--enable-jemalloc",  # make this a variant?
            "--enable-percolation",  # make this a variant?
            # '--enable-rebalancing',   # this seems broken
            "--with-hwloc=hwloc",
            "--with-jemalloc=jemalloc",
            # Spack's libffi installs its headers strangely,
            # leading to problems
            "--with-libffi=contrib",
            # '--with-papi=papi',   # currently disabled in HPX
        ]

        if spec.satisfies("+cxx11"):
            args += ["--enable-hpx++"]

        if spec.satisfies("+debug"):
            args += ["--enable-debug"]

        if spec.satisfies("+instrumentation"):
            args += ["--enable-instrumentation"]

        if spec.satisfies("+mpi") or spec.satisfies("+photon"):
            # photon requires mpi
            args += ["--enable-mpi"]
            # Choose pkg-config name for MPI library
            if spec.satisfies("^openmpi"):
                args += ["--with-mpi=ompi-cxx"]
            elif spec.satisfies("^mpich"):
                args += ["--with-mpi=mpich"]
            elif spec.satisfies("^mvapich2"):
                args += ["--with-mpi=mvapich2-cxx"]
            else:
                args += ["--with-mpi=system"]

        # METIS does not support pkg-config; HPX will pick it up automatically
        # if '+metis' in spec:
        #     args += ['--with-metis=???']

        if spec.satisfies("+opencl"):
            args += ["--enable-opencl"]
            if spec.satisfies("^pocl"):
                args += ["--with-opencl=pocl"]
            else:
                args += ["--with-opencl=system"]

        if spec.satisfies("+photon"):
            args += ["--enable-photon"]

        if spec.satisfies("+pic"):
            args += ["--with-pic"]

        return args
