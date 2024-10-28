# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPetsc4py(PythonPackage):
    """This package provides Python bindings for the PETSc package."""

    homepage = "https://gitlab.com/petsc/petsc4py"
    url = (
        "https://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc4py-3.20.0.tar.gz"
    )
    git = "https://gitlab.com/petsc/petsc.git"

    maintainers("balay")

    license("BSD-2-Clause")

    version("main", branch="main")
    version("3.22.0", sha256="b35fc833d41c7969be8a530494fcc81741d77e0dc33fba2f4050cdbd0ad881ae")
    version("3.21.6", sha256="d7a6d41e1463b04b9711b53b347d15f590f9354fae37aae14ad69100286129aa")
    version("3.21.5", sha256="70e6fa795e9abd8014faec0203cd0cc3efd79f4647c97cafc33776421c9ab1e8")
    version("3.21.4", sha256="4ba702558cc91186912eeacef26b171255f3adaa7ea02bec40c2f4c919eccecd")
    version("3.21.3", sha256="1c3664d5b527354171077c89c4b1fef3df4a41be7196d12bca74b2759c7e2648")
    version("3.21.2", sha256="6ce1e1a45407da300c6869d0d9abe17b5b077424aa4895713642dda0bb19ab4e")
    version("3.21.1", sha256="ea8c6afb16541167d39f87d5fcad98c32d856fe8a2173504ef2a31c16647d53d")
    version("3.21.0", sha256="b2000a3f8ef60920e1f82fa4772372d7941bc737bcc421a234a2507097a44d00")
    version("3.20.6", sha256="bcc4cb35231ba6664309ea195cc8ce8a9bb61f3e24b39be480eee59c52139dc2")
    version("3.20.5", sha256="2f40a6a7bfdaa2bca7c1f3e739ab7c74aba8d95db05aa1d120826eec904bbc16")
    version("3.20.4", sha256="3ebdb4c605ad59d71b7b7adc5f06b6d2a7ce9225c9b56e672923cb5bd6e43440")
    version("3.20.3", sha256="8e10884df5ca38191b71294dc7e89f7479b18cca83fedfe27f89105e57c40785")
    version("3.20.2", sha256="d3f24aa6612ded3e9b9ae11d5533f319d1df1705bea6d81385fea023d01175c9")
    version("3.20.1", sha256="dcc9092040d13130496f1961b79c36468f383b6ede398080e004f1966c06ad38")
    version("3.20.0", sha256="c2461eef3977ae5c214ad252520adbb92ec3a31d00e79391dd92535077bbf03e")
    version("3.19.6", sha256="bd7891b651eb83504c744e70706818cf63ecbabee3206c1fed7c3013873802b9")
    version("3.19.5", sha256="e059fdb8b23936c3182c9226924029dbdc8f1f72a623be0fe8c2caf8646c7a45")
    version("3.19.4", sha256="5621ddee63d0c631d2e8fed2d5d9763b183ad164c227dde8d3abcdb6c35c5ffb")
    version("3.19.3", sha256="dcbadebf0c4fe78b4dc13b8cd910577b9cacf65636ea980523e61d95c6959e5b")
    version("3.19.2", sha256="5f207eb95f87ddafa32229681a95af61912871cd7fbd38780bc63019dad3e7b8")
    version("3.19.1", sha256="d04def9995ed6395e125c605da169438d77d410d5019dc57be42e428ade30190")
    version("3.19.0", sha256="d1660092c9be9547e9a17d3d5bb139eaad737c3e1c4ef2ee41c71c8dc3bb9955")
    version("3.18.6", sha256="e4976e42895955cbb2c56f1b0f791c838338348a10664b8dcfc3fe56198bf943")
    version("3.18.5", sha256="625cbb99d7d3000ad05afe60585c6aa24ca650894b09a1989127febb64b65470")
    version("3.18.4", sha256="84a055b7f38d1200a8c486c89db05ce0724fe28da56afb656660cef054384e24")
    version("3.18.3", sha256="853ab9620c4832cbfe1f490edde827a505c8a376cc1a7b4fa6406faac9059433")
    version("3.18.2", sha256="1b6761b02ec6ef9099e2a048e234065c1c4096ace01e52e353624b80417cceec")
    version("3.18.1", sha256="6d9d9632e2da0920c4e3905b7bac919837bdd85ecfaf1b9e461ba7e05ec4a5ce")
    version("3.18.0", sha256="76bad2d35f380f698f5649c3f38eabd153b9b19b1fe3ce3a1d3de9aa5824a4d2")
    version("3.17.5", sha256="e435d927bf22950c71c30bda538e1ae75f48f6931a63205c6fbeff6cf4393f09")
    version("3.17.4", sha256="216c3da074557946615d37d0826bc89f1f2e599323e2dacbdc45326d78bd50c6")
    version("3.17.3", sha256="c588ab4a17deebe7f0a57f966b3368d88f01d1a1c09f220f63fe8e3b37a32899")
    version("3.17.2", sha256="7e256e13013ce12c8e52edee35920e3d2c1deaae1b71597a3064201eba7abc1c")
    version("3.17.1", sha256="f73a6eb0b453ec2500c9b353dc8427f205bcc12910b263bc4351fea3c6e0af71")
    version("3.17.0", sha256="a3543ebb87dc2b47046e1950b3a356e249d365526515b5e6b328aa7bfae94d29")
    version("3.16.6", sha256="a9b4ed19ca2e62b38da51ac3a70539d9581a1354cc4464c93963d7e95bd8ef66")
    version("3.16.5", sha256="f0ab5c5947ee0b58e51f741f46fab0d32e6458245e8f8b81fcf3da77bad50d25")
    version("3.16.4", sha256="51ac59be9d741ede95c8e0e13b6062b6fb1bd1c975da26732ba059ee8c5bb7eb")
    version("3.16.3", sha256="10e730d50716e40de55b200ff53b461bc4f3fcc798ba89b74dfe6bdf63fa7b6e")
    version("3.16.2", sha256="906634497ae9c59f2c97e12b935954e5ba95df2e764290c24fff6751b7510b04")
    version("3.16.1", sha256="c218358217c436947f8fd61f247f73ac65fa29ea3489ad00bef5827b1436b95f")
    version("3.16.0", sha256="4044accfdc2c80994e80e4e286478d1ba9ac358512d1b74c42e1327eadb0d802")
    version("3.15.5", sha256="cdbc8a7485960c80565268ae851639f6c620663f245708263a349903dd07e5ae")
    version("3.15.4", sha256="f3e1ae8db824d7ac6994f6ae4e04fdd76381f060ca350fee2a85aac668125a8c")
    version("3.15.3", sha256="06e7a5de3509067d8625330b10c1ab200b36df1dfdc2e93922038784b2722f8e")
    version("3.15.2", sha256="d7ed1d79d88b35da563d25e733f276595ba538c52756225f79ba92e1cc4658d3")
    version("3.15.1", sha256="4ec8f42081e4d6a61157b32869b352dcb18c69077f2d1e4160f3837efd9e150f")
    version("3.15.0", sha256="87dcc5ef63a1f0e1a963619f7527e623f52341b2806056b0ef5fdfb0b8b287ad")
    version("3.14.1", sha256="f5f8daf3a4cd1dfc945876b0d83a05b25f3c54e08046312eaa3e3036b24139c0")
    version("3.14.0", sha256="33ac9fb55a541e4c1deabd6e2144da96d5ae70e70c830a55de558000cf3f0ec5")
    version("3.13.0", sha256="0e11679353c0c2938336a3c8d1a439b853e20d3bccd7d614ad1dbea3ec5cb31f")
    version("3.12.0", sha256="4c94a1dbbf244b249436b266ac5fa4e67080d205420805deab5ec162b979df8d")
    version("3.11.0", sha256="ec114b303aadaee032c248a02021e940e43c6437647af0322d95354e6f2c06ad")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Activates MPI support")

    patch("ldshared.patch", when="@:3.18")

    depends_on("py-cython@3:", when="@3.20:", type="build")
    depends_on("py-cython@0.29.32:", when="^python@3.11:", type="build")
    depends_on("py-cython@0.24:", type="build")
    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-mpi4py", when="+mpi", type=("build", "run"))

    depends_on("petsc+mpi", when="+mpi")
    depends_on("petsc~mpi", when="~mpi")
    depends_on("petsc@main", when="@main")
    for ver in [
        "3.22",
        "3.21",
        "3.20",
        "3.19",
        "3.18",
        "3.17",
        "3.16",
        "3.15",
        "3.13",
        "3.12",
        "3.11",
    ]:
        depends_on(f"petsc@{ver}", when=f"@{ver}")
    depends_on("petsc@3.14.2:3.14", when="@3.14.1:3.14")
    depends_on("petsc@3.14.0:3.14.1", when="@3.14.0")

    @property
    def build_directory(self):
        import os

        if self.spec.satisfies("@main"):
            return os.path.join(self.stage.source_path, "src", "binding", "petsc4py")
        else:
            return self.stage.source_path

    @run_before("install")
    def cythonize(self):
        with working_dir(self.build_directory):
            python(join_path("conf", "cythonize.py"))
