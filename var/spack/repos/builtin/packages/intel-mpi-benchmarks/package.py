# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelMpiBenchmarks(MakefilePackage):
    """Intel MPI Benchmarks provides a set of elementary benchmarks that
    conform to MPI-1, MPI-2, and MPI-3 standard. You can run all of
    the supported benchmarks, or a subset specified in the command
    line using one executable file. Use command-line parameters to
    specify various settings, such as time measurement, message
    lengths, and selection of communicators.

    """

    homepage = "https://software.intel.com/en-us/articles/intel-mpi-benchmarks"
    url = "https://github.com/intel/mpi-benchmarks/archive/IMB-v2021.3.tar.gz"
    maintainers("carsonwoods")

    license("BSD-3-Clause")

    version("2021.7", sha256="acee02cc719a74e6853194576cb7e6bf1fdc74f8971578e1b2141306c3c19477")
    version("2021.6", sha256="57d1bcc0027f8fc7bffe323ab70cc9d3f1d7482d456c47b4a9e7c4337089bd54")
    version("2021.5", sha256="ac144dbfad8759e4956d99569dfcbec25758ba10abfb5ae2d83831660f27be60")
    version("2021.4", sha256="786570f0ff46aab01c4e5ecbde72c8051682809b23a04e55554f265b761ddde3")
    version("2021.3", sha256="9b58a4a7eef7c0c877513152340948402fd87cb06270d2d81308dc2ef740f4c7")
    version("2021.2", sha256="ade3bfe18b4313a31fc09f0bf038e0a6c169c4145089bfc6f1f827687b81be6a")
    version("2021.1", sha256="9089bb81e3091af3481e03b898b339fb2d9fb6574d4ef059adb1f5410112b23a")
    version("2019.6", sha256="1cd0bab9e947228fced4666d907f77c51336291533919896a923cff5fcad62e9")
    version("2019.5", sha256="61f8e872a3c3076af53007a68e4da3a8d66be2ba7a051dc21e626a4e2d26e651")
    version("2019.4", sha256="aeb336be10275c1a2f579b491b6631122876b461ac7148b1d0764f13b7552690")
    version("2019.3", sha256="4f256d11bfed9ca6166548486d61a062e67be61f13dd9f30690232720e185f31")
    version("2019.2", sha256="0bc2224a913073aaa5958f6ae08341e5fcd39cedc6722a09bfd4a3d7591a340b")
    version("2019.1", sha256="fe0d065b9936b6943ea83cb3d00aede43b17565285c6b1791fee8e340853ef79")
    version("2019.0", sha256="1c7d44aa7fd86ca84ac7cae1a69a8426243048d6294582337f1de7b4ffe68d37")
    version("2018.1", sha256="718a4eb155f18cf15a736f6496332407b5837cf1f19831723d4cfe5266c43507")
    version("2018.0", sha256="2e60a9894a686a95791be2227bc569bf81ca3875421b5307df7d83f885b1de88")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("mpi", when="@2019:")
    depends_on("intel-mpi", when="@2018")
    depends_on("gmake", type="build", when="@2018")

    conflicts(
        "^openmpi",
        when="@:2019.0",
        msg="intel-mpi-benchmarks <= v2019.0 cannot be built with OpenMPI, "
        "please specify a different MPI implementation",
    )

    # https://github.com/intel/mpi-benchmarks/pull/19
    patch("add_const.patch", when="@2019")
    # https://github.com/intel/mpi-benchmarks/pull/20
    patch("reorder_benchmark_macros.patch", when="@2019.1:2019.6")

    variant("mpi1", default=True, description="Build MPI1 benchmark")
    variant("ext", default=True, description="Build EXT benchmark")
    variant("io", default=True, description="Build IO benchmark")
    variant("nbc", default=True, description="Build NBC benchmark")
    variant("p2p", default=True, description="Build P2P benchmark", when="@2018:")
    variant("rma", default=True, description="Build RMA benchmark")
    variant("mt", default=True, description="Build MT benchmark")
    variant(
        "check", default=False, description="Build with MPI implementation verification checks"
    )

    # Handle missing variants in previous versions
    conflicts("+p2p", when="@:2019")
    conflicts("+mt", when="@:2019")

    def url_for_version(self, version):
        if version <= Version("2019.1"):
            url = "https://github.com/intel/mpi-benchmarks/archive/refs/tags/v{0}.tar.gz"
        else:
            url = "https://github.com/intel/mpi-benchmarks/archive/refs/tags/IMB-v{0}.tar.gz"
        return url.format(version)

    @property
    def build_directory(self):
        if self.spec.satisfies("@2018"):
            return "src"
        else:
            return "."

    @property
    def parallel(self):
        if self.spec.satisfies("@:2019"):
            return False
        return True

    @property
    def build_targets(self):
        spec = self.spec
        targets = []
        if spec.satisfies("+mpi1"):
            targets.append("MPI1")
        if spec.satisfies("+ext"):
            targets.append("EXT")
        if spec.satisfies("+io"):
            targets.append("IO")
        if spec.satisfies("+nbc"):
            targets.append("NBC")
        if spec.satisfies("+p2p"):
            targets.append("P2P")
        if spec.satisfies("+rma"):
            targets.append("RMA")
        if spec.satisfies("+mt"):
            targets.append("MT")

        if spec.satisfies("@2019:"):
            targets = ["TARGET=" + target for target in targets]

        if spec.satisfies("+check"):
            targets.append("CPPFLAGS=-DCHECK")

        return targets

    def edit(self, spec, prefix):
        env["CC"] = spec["mpi"].mpicc
        env["CXX"] = spec["mpi"].mpicxx

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        with working_dir(self.build_directory):
            if spec.satisfies("+mpi1"):
                install("IMB-MPI1", prefix.bin)
            if spec.satisfies("+ext"):
                install("IMB-EXT", prefix.bin)
            if spec.satisfies("+io"):
                install("IMB-IO", prefix.bin)
            if spec.satisfies("+nbc"):
                install("IMB-NBC", prefix.bin)
            if spec.satisfies("+p2p"):
                install("IMB-P2P", prefix.bin)
            if spec.satisfies("+rma"):
                install("IMB-RMA", prefix.bin)
            if spec.satisfies("+mt"):
                install("IMB-MT", prefix.bin)
