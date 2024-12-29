# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ams(CMakePackage, CudaPackage):
    """AMS Autonomous Multiscale Framework."""

    homepage = "https://github.com/LLNL/AMS"
    git = "https://github.com/LLNL/AMS.git"

    maintainers("koparasy", "lpottier")

    version("develop", branch="develop", submodules=False)
    version(
        "11.08.23.alpha",
        tag="11.08.23.alpha",
        commit="1a42b29268bb916dae301654ca0b92fdfe288732",
        submodules=False,
    )
    version(
        "07.25.23-alpha",
        tag="07.25.23-alpha",
        commit="3aa8421f1f1ce1ae448d017214c602b9def19c90",
        submodules=False,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "faiss",
        default=False,
        description="Build with FAISS index as uncertainty quantification module",
    )
    variant(
        "caliper", default=False, description="Build with caliper for gather performance counters"
    )
    variant("torch", default=False, description="Use torch for surrogate models")
    variant("mpi", default=False, description="Enable MPI support")
    variant("examples", default=False, description="Enable examples")
    variant("redis", default=False, description="Enable redis database")
    variant("hdf5", default=False, description="Enable HDF5 data storage")
    variant("rabbitmq", default=False, description="Enable RabbitMQ as data broker")
    variant(
        "verbose",
        default=False,
        description="Enable AMSLib verbose output (controlled by environment variable)",
    )

    depends_on("umpire")
    depends_on("mpi", when="+mpi")

    depends_on("caliper+cuda", when="+caliper +cuda")
    depends_on("faiss+cuda", when="+faiss +cuda")
    depends_on("mfem+cuda", when="+examples +cuda")
    depends_on("py-torch+cuda", when="+torch +cuda")

    depends_on("py-torch~cuda", when="+torch ~cuda")
    depends_on("caliper ~cuda", when="+caliper ~cuda")
    depends_on("faiss ~cuda", when="+faiss ~cuda")
    depends_on("mfem ~cuda", when="+examples ~cuda")

    depends_on("redis-plus-plus", when="+redis")
    depends_on("hdf5", when="+hdf5")
    depends_on("amqp-cpp +tcp", when="+rabbitmq")

    with when("+cuda"):
        cuda_archs = CudaPackage.cuda_arch_values
        with when("+examples"):
            depends_on("mfem+cuda")
            for sm_ in cuda_archs:
                depends_on(
                    "mfem +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_)
                )

        with when("+torch"):
            depends_on("py-torch+cuda")
            for sm_ in cuda_archs:
                depends_on(
                    "py-torch +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_)
                )

        with when("+caliper"):
            depends_on("caliper+cuda", when="+caliper")
            for sm_ in cuda_archs:
                depends_on(
                    "caliper +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_)
                )

        depends_on("umpire+cuda")
        for sm_ in cuda_archs:
            depends_on("umpire +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))

        with when("+faiss"):
            depends_on("faiss+cuda", when="+faiss")
            for sm_ in cuda_archs:
                depends_on(
                    "umpire +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_)
                )

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append("-DUMPIRE_DIR={0}".format(spec["umpire"].prefix))
        args.append("-DWITH_MPI={0}".format("On" if "+mpi" in spec else "Off"))

        args.append(
            "-DWITH_DB={0}".format(
                "On" if ("+redis" in spec or "hdf5" in spec or "+rabbitmq" in spec) else "Off"
            )
        )

        if spec.satisfies("+verbose"):
            args.append("-DWITH_AMS_DEBUG=On")

        if spec.satisfies("+hdf5"):
            args.append("-DWITH_HDF5=On")
            args.append("-DHDF5_Dir={0}".format(spec["hdf5"].prefix))

        if spec.satisfies("+cuda"):
            args.append("-DWITH_CUDA=On")
            cuda_arch = spec.variants["cuda_arch"].value[0]
            args.append("-DAMS_CUDA_ARCH={0}".format(cuda_arch))

        if spec.satisfies("+caliper"):
            args.append("-DWITH_CALIPER=On")
            args.append("-DCALIPER_DIR={0}/share/cmake/caliper".format(spec["caliper"].prefix))
        else:
            args.append("-DWITH_CALIPER=Off")

        if spec.satisfies("+faiss"):
            args.append("-DWITH_FAISS=On")
            args.append("-DFAISS_DIR={0}".format(spec["faiss"].prefix))
        else:
            args.append("-DWITH_FAISS=Off")

        if spec.satisfies("+torch"):
            args.append("-DWITH_TORCH=On")
            args.append(
                "-DTorch_DIR={0}/lib/python{1}/site-packages"
                "/torch/share/cmake/Torch".format(
                    spec["py-torch"].prefix, spec["python"].version.up_to(2)
                )
            )

        if spec.satisfies("+redis"):
            args.append("-DWITH_REDIS=On")
            args.append("-DREDIS_PLUS_PLUS_DIR={0}".format(spec["redis-plus-plus"].prefix))

        if spec.satisfies("+rabbitmq"):
            args.append("-DWITH_RMQ=On")
            args.append("-Damqpcpp_DIR={0}/cmake".format(spec["amqp-cpp"].prefix))

        if spec.satisfies("+examples"):
            args.append("-DWITH_EXAMPLES=On")
            args.append("-DMFEM_DIR={0}".format(spec["mfem"].prefix))

        return args
