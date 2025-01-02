# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import datetime as dt
import os

from spack.build_environment import optimization_flags
from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Lammps(CMakePackage, CudaPackage, ROCmPackage, PythonExtension):
    """LAMMPS stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator.
    """

    homepage = "https://www.lammps.org/"
    url = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"
    git = "https://github.com/lammps/lammps.git"

    tags = ["ecp", "ecp-apps"]

    maintainers("rbberger")

    license("GPL-2.0-only")

    # rules for new versions and deprecation
    # * new stable versions should be added to stable_versions set
    # * a stable version that has updates and any of its outdated update releases should be
    #   marked deprecated=True
    # * patch releases older than a stable release should be marked deprecated=True
    version("develop", branch="develop")
    version(
        "20240829.1",
        sha256="3aea41869aa2fb8120fc4814cab645686f969e2eb7c66aa5587e500597d482dc",
        preferred=True,
    )
    version(
        "20240829",
        sha256="6112e0cc352c3140a4874c7f74db3c0c8e30134024164509ecf3772b305fde2e",
        deprecated=True,
    )
    version(
        "20240627",
        sha256="2174a99d266279823a8c57629ee1c21ec357816aefd85f964d9f859fe9222aa5",
        deprecated=True,
    )
    version(
        "20240417",
        sha256="158b288725c251fd8b30dbcf61749e0d6a042807da92af865a7d3c413efdd8ea",
        deprecated=True,
    )
    version(
        "20240207.1",
        sha256="3ba62c2a1ed463fceedf313a1c3ea2997994aa102379a8d35b525ea424f56776",
        deprecated=True,
    )
    version(
        "20240207",
        sha256="d518f32de4eb2681f2543be63926411e72072dd7d67c1670c090b5baabed98ac",
        deprecated=True,
    )
    version(
        "20231121",
        sha256="704d8a990874a425bcdfe0245faf13d712231ba23f014a3ebc27bc14398856f1",
        deprecated=True,
    )
    version(
        "20230802.4", sha256="6eed007cc24cda80b5dd43372b2ad4268b3982bb612669742c8c336b79137b5b"
    )
    version(
        "20230802.3",
        sha256="6666e28cb90d3ff01cbbda6c81bdb85cf436bbb41604a87f2ab2fa559caa8510",
        deprecated=True,
    )
    version(
        "20230802.2",
        sha256="3bcecabc9cad08d0a4e4d989b52d29c58505f7ead8ebacf43c9db8d9fd3d564a",
        deprecated=True,
    )
    version(
        "20230802.1",
        sha256="0e5568485e5ee080412dba44a1b7a93f864f1b5c75121f11d528854269953ed0",
        deprecated=True,
    )
    version(
        "20230802",
        sha256="48dc8b0b0583689e80ea2052275acbc3e3fce89707ac557e120db5564257f7df",
        deprecated=True,
    )
    version(
        "20230615",
        sha256="8470ed7b26ccd3728f4b44a7f1c520f1af23a648af685fd30b42b840fdfae2ff",
        deprecated=True,
    )
    version(
        "20230328",
        sha256="14f5a5c37e4b46466e90d8b35476800e66acee74999f7358f4c12dfe662bfd99",
        deprecated=True,
    )
    version(
        "20230208",
        sha256="60221242145da4479e5b207d9a0eed90af4168d7a297b4dc8c0e7f2b3215602e",
        deprecated=True,
    )
    version(
        "20221222",
        sha256="75372ee7ef982767fc4ed4dc95e20ddca8247419adeb0c1276c40e43d1eab955",
        deprecated=True,
    )
    version(
        "20221103",
        sha256="d28517b84b157d4e46a1a64ed787b4662d8f2f5ade3f5a04bb0caed068f32f7e",
        deprecated=True,
    )
    version(
        "20220915",
        sha256="392b8d35fc7919b0efaf8b389259a9b795a817e58e75e380467c63d03a0dab75",
        deprecated=True,
    )
    version(
        "20220803",
        sha256="f37cb0b35c1682ffceae5826aadce47278aa7003099a1655fcea43acd7d37926",
        deprecated=True,
    )
    version(
        "20220623.4", sha256="42541b4dbd0d339d16ddb377e76d192bc3d1d5712fdf9e2cdc838fc980d0a0cf"
    )
    version(
        "20220623.3",
        sha256="8a276a01b50d37eecfe6eb36f420f354cde51936d20aca7944dea60d3c098c89",
        deprecated=True,
    )
    version(
        "20220623.2",
        sha256="8a560213e83919623525c4a7c4b5f0eda35cdf3b0c0e6548fd891379e04ca9e6",
        deprecated=True,
    )
    version(
        "20220623.1",
        sha256="58e3b2b984f8935bb0db5631e143be2826c45ffd48844f7c394f36624a3e17a2",
        deprecated=True,
    )
    version(
        "20220623",
        sha256="d27ede095c9f00cd13a26f967a723d07cf8f4df65c700ed73573577bc173d5ce",
        deprecated=True,
    )
    version(
        "20220602",
        sha256="3e8f54453e53b3b387a68317277f832b8cf64a981e64b21e98bb37ea36ac4a60",
        deprecated=True,
    )
    version(
        "20220504",
        sha256="fe05bae8090fd0177b3c1b987cd32a9cb7cd05d790828ba954c764eb52e10b52",
        deprecated=True,
    )
    version(
        "20220324",
        sha256="d791cc93eedfc345fdf87bfa5b6f7e17e461f86ba197f9e9c3d477ce8657a7ef",
        deprecated=True,
    )
    version(
        "20220217",
        sha256="e5bd2bf325835fa98d1b95f0667c83076580916027df5b8109d5470d1b97da98",
        deprecated=True,
    )
    version(
        "20220107",
        sha256="fbf6c6814968ae0d772d7b6783079ff4f249a8faeceb39992c344969e9f1edbb",
        deprecated=True,
    )
    version(
        "20211214",
        sha256="9f7b1ee2394678c1a6baa2c158a62345680a952eee251783e3c246b3f12db4c9",
        deprecated=True,
    )
    version(
        "20211027",
        sha256="c06f682fcf9d5921ca90c857a104e90fba0fe65decaac9732745e4da49281938",
        deprecated=True,
    )
    version(
        "20210929.3", sha256="e4c274f0dc5fdedc43f2b365156653d1105197a116ff2bafe893523cdb22532e"
    )
    version(
        "20210929.2",
        sha256="9318ca816cde16a9a4174bf22a1966f5f2155cb32c0ad5a6757633276411fb36",
        deprecated=True,
    )
    version(
        "20210929.1",
        sha256="5000b422c9c245b92df63507de5aa2ea4af345ea1f00180167aaa084b711c27c",
        deprecated=True,
    )
    version(
        "20210929",
        sha256="2dff656cb21fd9a6d46c818741c99d400cfb1b12102604844663b655fb2f893d",
        deprecated=True,
    )
    version(
        "20210920",
        sha256="e3eba96933c1dd3177143c7ac837cae69faceba196948fbad2970425db414d8c",
        deprecated=True,
    )
    version(
        "20210831",
        sha256="532c42576a79d72682deaf43225ca773ed9f9e35deb484a82f91905b6cba23ec",
        deprecated=True,
    )
    version(
        "20210730",
        sha256="c5e998c8282a835d2bcba4fceffe3cecdf9aed9bdf79fa9c945af573e632f6e7",
        deprecated=True,
    )
    version(
        "20210728",
        sha256="6b844d2c3f7170a59d36fbf761483aa0c63d95eda254d00fe4d10542403abe36",
        deprecated=True,
    )
    version(
        "20210702",
        sha256="4fdd8ca2dbde8809c0048716650b73ae1f840e22ebe24b25f6f7a499377fea57",
        deprecated=True,
    )
    version(
        "20210527",
        sha256="f9f29970941f406d5c250de52a4cd07e5a4e44ae3b5ffed46edd019d998b8c33",
        deprecated=True,
    )
    version(
        "20210514",
        sha256="74d9c4386f2181b15a024314c42b7a0b0aaefd3b4b947aeca00fe07e5b2f3317",
        deprecated=True,
    )
    version(
        "20210408",
        sha256="1645147b7777de4f616b8232edf0b597868084f969c777fa0a757949c3f71f56",
        deprecated=True,
    )
    version(
        "20210310",
        sha256="25708378dbeccf794bc5045aceb84380bf4a3ca03fc8e5d150a26ca88d371474",
        deprecated=True,
    )
    version(
        "20210210",
        sha256="2c5ba2c7935ad559ca94ee826e8727e65b49ef4582eb856534fffba70e44101a",
        deprecated=True,
    )
    version("20201029", sha256="759705e16c1fedd6aa6e07d028cc0c78d73c76b76736668420946a74050c3726")
    version(
        "20200721",
        sha256="845bfeddb7b667799a1a5dbc166b397d714c3d2720316604a979d3465b4190a9",
        deprecated=True,
    )
    version(
        "20200630",
        sha256="413cbfabcc1541a339c7a4ab5693fbeb768f46bb1250640ba94686c6e90922fc",
        deprecated=True,
    )
    version(
        "20200505",
        sha256="c49d77fd602d28ebd8cf10f7359b9fc4d14668c72039028ed7792453d416de73",
        deprecated=True,
    )
    version("20200303", sha256="a1a2e3e763ef5baecea258732518d75775639db26e60af1634ab385ed89224d1")
    version(
        "20200227",
        sha256="1aabcf38bc72285797c710b648e906151a912c36b634a9c88ac383aacf85516e",
        deprecated=True,
    )
    version(
        "20200218",
        sha256="73bcf146660804ced954f6a0a8dce937482677778d46018ca5a688127bf97211",
        deprecated=True,
    )
    version(
        "20200204",
        sha256="3bf3de546ede34ffcd89f1fca5fd66aa78c662e7c8a76e30ce593e44a00d23ce",
        deprecated=True,
    )
    version(
        "20200124",
        sha256="443829560d760690e1ae21ad54922f56f34f640a81e817f5cc65d2a4af3a6a5d",
        deprecated=True,
    )
    version(
        "20200109",
        sha256="f2fd24f6c10837801f490913d73f672ec7c6becda08465d7e834a2bfbe3d7cd6",
        deprecated=True,
    )
    version(
        "20191120",
        sha256="fd146bf517a6c2fb8a69ecb3749dc352eef94414739cd7855c668c690af85d27",
        deprecated=True,
    )
    version(
        "20191030",
        sha256="5279567f731386ffdb87800b448903a63de2591064e13b4d5216acae25b7e541",
        deprecated=True,
    )
    version(
        "20190919",
        sha256="0f693203afe86bc70c084c55f29330bdeea3e3ad6791f81c727f7a34a7f6caf3",
        deprecated=True,
    )
    version(
        "20190807",
        sha256="895d71914057e070fdf0ae5ccf9d6552b932355056690bdb8e86d96549218cc0",
        deprecated=True,
    )
    version(
        "20190605",
        sha256="c7b35090aef7b114d2b47a7298c1e8237dd811da87995c997bf7639cca743152",
        deprecated=True,
    )
    version(
        "20181212",
        sha256="ccc5d2c21c4b62ce4afe7b3a0fe2f37b83e5a5e43819b7c2e2e255cce2ce0f24",
        deprecated=True,
    )
    version(
        "20181207",
        sha256="d92104d008a7f1d0b6071011decc5c6dc8b936a3418b20bd34b055371302557f",
        deprecated=True,
    )
    version(
        "20181127",
        sha256="c076b633eda5506f895de4c73103df8b995d9fec01be82c67c7608efcc345179",
        deprecated=True,
    )
    version(
        "20181115",
        sha256="3bc9c166e465cac625c4a8e4060e597003f4619dadd57d3bc8d25bcd930f286e",
        deprecated=True,
    )
    version(
        "20181109",
        sha256="dd30fe492fa147fb6f39bfcc79d8c786b9689f7fbe86d56de58cace53b6198c9",
        deprecated=True,
    )
    version(
        "20181024",
        sha256="a171dff5aff7aaa2c9606ab2abc9260f2b685a5c7f6d650e7f2b59cf4aa149d6",
        deprecated=True,
    )
    version(
        "20181010",
        sha256="bda762ee2d2dcefe0b4e36fb689c6b9f7ede49324444ccde6c59cba727b4b02d",
        deprecated=True,
    )
    version(
        "20180918",
        sha256="02f143d518d8647b77137adc527faa9725c7afbc538d670253169e2a9b3fa0e6",
        deprecated=True,
    )
    version(
        "20180905",
        sha256="ee0df649e33a9bf4fe62e062452978731548a56b7487e8e1ce9403676217958d",
        deprecated=True,
    )
    version(
        "20180831",
        sha256="6c604b3ebd0cef1a5b18730d2c2eb1e659b2db65c5b1ae6240b8a0b150e4dff3",
        deprecated=True,
    )
    version(
        "20180822",
        sha256="9f8942ca3f8e81377ae88ccfd075da4e27d0dd677526085e1a807777c8324074",
        deprecated=True,
    )
    version(
        "20180629",
        sha256="1acf7d9b37b99f17563cd4c8bb00ec57bb2e29eb77c0603fd6871898de74763b",
        deprecated=True,
    )
    version(
        "20180316",
        sha256="a81f88c93e417ecb87cd5f5464c9a2570384a48ff13764051c5e846c3d1258c1",
        deprecated=True,
    )
    version(
        "20180222",
        sha256="374254d5131b7118b9ab0f0e27d20c3d13d96b03ed2b5224057f0c1065828694",
        deprecated=True,
    )
    version(
        "20170922",
        sha256="f0bf6eb530d528f4d261d0a261e5616cbb6e990156808b721e73234e463849d3",
        deprecated=True,
    )
    version(
        "20170901",
        sha256="5d88d4e92f4e0bb57c8ab30e0d20de556830af820223778b9967bec2184efd46",
        deprecated=True,
    )

    depends_on("cxx", type="build")

    # mdi, scafacos, ml-quip, qmmm require C, but not available in Spack
    for c_pkg in ("adios", "atc", "awpmd", "ml-pod", "electrode", "kim", "h5md", "tools", "rheo"):
        depends_on("c", type="build", when=f"+{c_pkg}")

    # scafacos, ml-quip require Fortran, but not available in Spack
    for fc_pkg in ("kim",):
        depends_on("fortran", type="build", when=f"+{fc_pkg}")

    stable_versions = {
        "20240829.1",
        "20240829",
        "20230802.4",
        "20230802.3",
        "20230802.2",
        "20230802.1",
        "20230802",
        "20220623.4",
        "20220623.3",
        "20220623.2",
        "20220623.1",
        "20220623",
        "20210929.3",
        "20210929.2",
        "20210929.1",
        "20210929",
        "20201029",
        "20200303",
    }

    def url_for_version(self, version):
        split_ver = str(version).split(".")
        vdate = dt.datetime.strptime(split_ver[0], "%Y%m%d")
        if len(split_ver) < 2:
            update = ""
        else:
            update = "_update{0}".format(split_ver[1])

        return "https://github.com/lammps/lammps/archive/{0}_{1}{2}.tar.gz".format(
            "stable" if str(version) in Lammps.stable_versions else "patch",
            vdate.strftime("%d%b%Y").lstrip("0"),
            update,
        )

    # List of supported optional packages
    # Note: package `openmp` in this recipe is called `openmp-package`, to avoid clash
    # with the pre-existing `openmp` variant
    # version ranges generates using utility script:
    # https://gist.github.com/rbberger/fdaa38ff08e5961c4741624a4719cdb6
    supported_packages = {
        "adios": {"when": "@20210702:"},
        "amoeba": {"when": "@20220803:"},
        "asphere": {},
        "atc": {"when": "@20210702:"},
        "awpmd": {"when": "@20210702:"},
        "bocs": {"when": "@20210702:"},
        "body": {},
        "bpm": {"when": "@20220504:"},
        "brownian": {"when": "@20210702:"},
        "cg-dna": {"when": "@20210702:"},
        "cg-sdk": {"when": "@20210702:20220623"},
        "cg-spica": {"when": "@20220803:"},
        "class2": {},
        "colloid": {},
        "colvars": {"when": "@20210702:"},
        "compress": {},
        "coreshell": {},
        "dielectric": {"when": "@20210702:"},
        "diffraction": {"when": "@20210702:"},
        "dipole": {},
        "dpd-basic": {"when": "@20210702:"},
        "dpd-meso": {"when": "@20210702:"},
        "dpd-react": {"when": "@20210702:"},
        "dpd-smooth": {"when": "@20210702:"},
        "drude": {"when": "@20210702:"},
        "eff": {"when": "@20210702:"},
        "electrode": {"when": "@20220504:"},
        "extra-compute": {"when": "@20210728:"},
        "extra-dump": {"when": "@20210728:"},
        "extra-fix": {"when": "@20210728:"},
        "extra-molecule": {"when": "@20210728:"},
        "extra-pair": {"when": "@20210728:"},
        "fep": {"when": "@20210702:"},
        "granular": {},
        "h5md": {"when": "@20210702:"},
        "intel": {"when": "@20210702:"},
        "interlayer": {"when": "@20210728:"},
        "kim": {},
        "kokkos": {},
        "kspace": {"default": True},
        "latboltz": {"when": "@20210702:"},
        "latte": {"when": "@20170922:20230328"},
        "lepton": {"when": "@20230208:"},
        "machdyn": {"when": "@20210702:"},
        "manifold": {"when": "@20210702:"},
        "manybody": {"default": True},
        "mc": {},
        "meam": {"when": "@:20181212,20210702:"},
        "mesont": {"when": "@20210702:"},
        "mgpt": {"when": "@20210702:"},
        "misc": {},
        "ml-hdnnp": {"when": "@20210702:"},
        "ml-iap": {"when": "@20210702:"},
        "ml-pod": {"when": "@20221222:"},
        "ml-rann": {"when": "@20210702:"},
        "ml-snap": {"when": "@20210702:"},
        "ml-uf3": {"when": "@20240627:"},
        "mliap": {"when": "@20200630:20210527"},
        "mofff": {"when": "@20210702:"},
        "molecule": {"default": True},
        "molfile": {"when": "@20210702:"},
        "mpiio": {"when": "@:20230802.1"},
        "netcdf": {"when": "@20210702:"},
        "openmp-package": {},
        "opt": {},
        "orient": {"when": "@20210728:"},
        "peri": {},
        "phonon": {"when": "@20210702:"},
        "plugin": {"when": "@20210408:"},
        "plumed": {"when": "@20210702:"},
        "poems": {},
        "ptm": {"when": "@20210702:"},
        "python": {},
        "qeq": {},
        "qtb": {"when": "@20210702:"},
        "reaction": {"when": "@20210702:"},
        "reax": {"when": "@:20181212"},
        "reaxff": {"when": "@20210702:"},
        "rheo": {"when": "@20240829:"},
        "replica": {},
        "rigid": {"default": True},
        "shock": {},
        "smtbq": {"when": "@20210702:"},
        "snap": {"when": "@:20210527"},
        "sph": {"when": "@20210702:"},
        "spin": {"when": "@20180629:"},
        "srd": {},
        "tally": {"when": "@20210702:"},
        "uef": {"when": "@20210702:"},
        "user-adios": {"when": "@20190228:20210527"},
        "user-atc": {"when": "@:20210527"},
        "user-awpmd": {"when": "@:20210527"},
        "user-bocs": {"when": "@20180511:20210527"},
        "user-brownian": {"when": "@20210514:20210527"},
        "user-cgsdk": {"when": "@20170504:20210527"},
        "user-colvars": {"when": "@:20210527"},
        "user-diffraction": {"when": "@:20210527"},
        "user-dpd": {"when": "@:20210527"},
        "user-drude": {"when": "@:20210527"},
        "user-eff": {"when": "@:20210527"},
        "user-fep": {"when": "@:20210527"},
        "user-h5md": {"when": "@:20210527"},
        "user-hdnnp": {"when": "@20210527"},
        "user-intel": {"when": "@:20210527"},
        "user-lb": {"when": "@:20210527"},
        "user-manifold": {"when": "@:20210527"},
        "user-meamc": {"when": "@20170706:20210527"},
        "user-mesodpd": {"when": "@20200319:20210527"},
        "user-mesont": {"when": "@20200615:20210527"},
        "user-mgpt": {"when": "@:20210527"},
        "user-misc": {"when": "@:20210702"},
        "user-mofff": {"when": "@20180205:20210527"},
        "user-molfile": {"when": "@:20210527"},
        "user-netcdf": {"when": "@20170504:20210527"},
        "user-omp": {"when": "@:20210527"},
        "user-phonon": {"when": "@:20210527"},
        "user-plumed": {"when": "@20181109:20210527"},
        "user-ptm": {"when": "@20181010:20210527"},
        "user-qtb": {"when": "@:20210527"},
        "user-rann": {"when": "@20210527"},
        "user-reaction": {"when": "@20200319:20210527"},
        "user-reaxc": {"when": "@:20210527"},
        "user-sdpd": {"when": "@20181109:20210527"},
        "user-smd": {"when": "@:20210527"},
        "user-smtbq": {"when": "@:20210527"},
        "user-sph": {"when": "@:20210527"},
        "user-tally": {"when": "@:20210527"},
        "user-uef": {"when": "@20171023:20210527"},
        "user-vtk": {"when": "@20210527"},
        "user-yaff": {"when": "@20190201:20210527"},
        "voronoi": {},
        "vtk": {"when": "@20210702:"},
        "yaff": {"when": "@20210702:"},
        # "mdi": {"when": "@20210702:"}, no mdi package
        # "ml-pace": {"when": "@20210702:"}, no pace package
        # "ml-quip": {"when": "@20210702:"}, no quip package
        # "scafacos": {"when": "@20210702:"}, no scafacos package
        # "user-quip": {"when": "@20190201:20210527"}, no quip package
        # "user-scafacos": {"when": "@20180905:20210527"}, no scafacos package
    }

    for pkg_name, pkg_options in supported_packages.items():
        variant(
            pkg_name,
            default=pkg_options.get("default", False),
            description="Activate the {} package".format(pkg_name.replace("-package", "")),
            when=pkg_options.get("when", None),
        )
    variant("lib", default=True, description="Build the liblammps in addition to the executable")
    variant("mpi", default=True, description="Build with mpi")
    variant("jpeg", default=False, description="Build with jpeg support")
    variant("png", default=False, description="Build with png support")
    variant("ffmpeg", default=False, description="Build with ffmpeg support")
    variant("curl", default=False, description="Build with curl support", when="@20240829:")
    variant("openmp", default=True, description="Build with OpenMP")
    variant("opencl", default=False, description="Build with OpenCL")
    variant(
        "exceptions",
        default=False,
        description="Build with lammps exceptions",
        when="@:20230802.1",
    )
    variant(
        "cuda_mps",
        default=False,
        description="(CUDA only) Enable tweaks for running "
        + "with Nvidia CUDA Multi-process services daemon",
    )

    variant(
        "lammps_sizes",
        default="smallbig",
        description="LAMMPS integer sizes (smallsmall: all 32-bit, smallbig:"
        + "64-bit #atoms #timesteps, bigbig: also 64-bit imageint, 64-bit atom ids)",
        values=("smallbig", "bigbig", "smallsmall"),
        multi=False,
    )
    variant(
        "fftw_precision",
        default="double",
        when="+kspace",
        description="Select FFTW precision (used by Kspace)",
        values=("single", "double"),
        multi=False,
    )
    variant(
        "fft",
        default="fftw3",
        when="+kspace",
        description="FFT library for KSPACE package",
        values=("kiss", "fftw3", "mkl"),
        multi=False,
    )
    variant(
        "heffte",
        default=False,
        when="+kspace @20240207:",
        description="Use heffte as distubuted FFT engine",
    )

    variant(
        "fft_kokkos",
        default="fftw3",
        when="@20240417: +kspace+kokkos",
        description="FFT library for Kokkos-enabled KSPACE package",
        values=("kiss", "fftw3", "mkl", "hipfft", "cufft"),
        multi=False,
    )
    variant(
        "gpu_precision",
        default="mixed",
        when="~kokkos",
        description="Select GPU precision (used by GPU package)",
        values=("double", "mixed", "single"),
        multi=False,
    )
    variant("tools", default=False, description="Build LAMMPS tools (msi2lmp, binary2txt, chain)")

    depends_on("cmake@3.16:", when="@20231121:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+mpiio")
    depends_on("fftw-api@3", when="+kspace fft=fftw3")
    depends_on("heffte", when="+heffte")
    depends_on("heffte+fftw", when="+heffte fft=fftw3")
    depends_on("heffte+mkl", when="+heffte fft=mkl")
    depends_on("mkl", when="+kspace fft=mkl")
    depends_on("hipfft", when="+kokkos+kspace+rocm fft_kokkos=hipfft")
    depends_on("fftw-api@3", when="+kokkos+kspace fft_kokkos=fftw3")
    depends_on("mkl", when="+kokkos+kspace fft_kokkos=mkl")
    depends_on("voropp", when="+voronoi")
    depends_on("netcdf-c+mpi", when="+user-netcdf")
    depends_on("netcdf-c+mpi", when="+netcdf")
    depends_on("blas", when="+user-atc")
    depends_on("blas", when="+atc")
    depends_on("lapack", when="+user-atc")
    depends_on("lapack", when="+atc")
    depends_on("opencl", when="+opencl")
    depends_on("latte@1.0.1", when="@:20180222+latte")
    depends_on("latte@1.1.1:", when="@20180316:20180628+latte")
    depends_on("latte@1.2.1:", when="@20180629:20200505+latte")
    depends_on("latte@1.2.2:", when="@20200602:20230328+latte")
    depends_on("blas", when="+latte")
    depends_on("lapack", when="+latte")
    depends_on("python", when="+python")
    depends_on("mpi", when="+user-lb")
    depends_on("mpi", when="+latboltz")
    depends_on("mpi", when="+user-h5md")
    depends_on("mpi", when="+h5md")
    depends_on("hdf5", when="+user-h5md")
    depends_on("hdf5", when="+h5md")
    depends_on("jpeg", when="+jpeg")
    depends_on("kim-api", when="+kim")
    depends_on("curl", when="@20190329:+kim")
    depends_on("curl", when="+curl")
    depends_on("libpng", when="+png")
    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("kokkos+deprecated_code+shared@3.0.00", when="@20200303+kokkos")
    depends_on("kokkos+shared@3.1:", when="@20200505:+kokkos")
    depends_on("kokkos@3.7.01:", when="@20230208: +kokkos")
    depends_on("kokkos@4.3.00:", when="@20240417: +kokkos")
    depends_on("kokkos@4.3.01:", when="@20240627: +kokkos")
    depends_on("adios2", when="+user-adios")
    depends_on("adios2", when="+adios")
    depends_on("plumed", when="+user-plumed")
    depends_on("plumed", when="+plumed")
    depends_on("eigen@3:", when="+user-smd")
    depends_on("eigen@3:", when="+machdyn")
    depends_on("py-cython", when="+mliap+python", type="build")
    depends_on("py-cython", when="+ml-iap+python", type="build")
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-build", when="+python", type="build")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python+mpi", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@20220217:+python", type=("build", "run"))
    for _n2p2_cond in ("+user-hdnnp", "+ml-hdnnp"):
        with when(_n2p2_cond):
            depends_on("n2p2@2.1.4:")
            depends_on("n2p2+shared", when="+lib")
    depends_on("vtk", when="+user-vtk")
    depends_on("vtk", when="+vtk")
    depends_on("hipcub", when="~kokkos +rocm")
    depends_on("llvm-amdgpu ", when="+rocm", type="build")
    depends_on("rocm-openmp-extras", when="+rocm +openmp", type="build")
    depends_on("gsl@2.6:", when="+rheo")

    # propagate CUDA and ROCm architecture when +kokkos
    for arch in CudaPackage.cuda_arch_values:
        depends_on("kokkos+cuda cuda_arch=%s" % arch, when="+kokkos+cuda cuda_arch=%s" % arch)

    for arch in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos+rocm amdgpu_target=%s" % arch, when="+kokkos+rocm amdgpu_target=%s" % arch
        )

    depends_on("googletest", type="test")
    depends_on("libyaml", type="test")

    extends("python", when="+python")

    conflicts("+cuda", when="+opencl")
    conflicts("+rocm", when="+opencl")
    conflicts("+body", when="+poems@:20180628")
    conflicts("+python", when="~lib")
    conflicts("+qeq", when="~manybody")
    conflicts("+user-atc", when="~manybody")
    conflicts("+atc", when="~manybody")
    conflicts("+user-misc", when="~manybody")
    conflicts("+user-phonon", when="~kspace")
    conflicts("+phonon", when="~kspace")
    conflicts("%gcc@9:", when="@:20200303+openmp")
    conflicts("+kokkos", when="@:20200227")
    conflicts("+dielectric", when="~kspace")
    conflicts("+dielectric", when="@:20210702~user-misc")
    conflicts("+dielectric", when="@20210728:~extra-pair")
    conflicts("+electrode", when="~kspace")
    conflicts("+mliap", when="~snap")
    conflicts("+ml-iap", when="~ml-snap")
    conflicts(
        "+user-adios +mpi",
        when="^adios2~mpi",
        msg="With +user-adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "+user-adios ~mpi",
        when="^adios2+mpi",
        msg="With +user-adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "+adios +mpi",
        when="^adios2~mpi",
        msg="With +adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "+adios ~mpi",
        when="^adios2+mpi",
        msg="With +adios, mpi setting for adios2 and lammps must be the same",
    )
    conflicts(
        "~kokkos+rocm",
        when="@:20220602",
        msg="ROCm builds of the GPU package not maintained prior to version 20220623",
    )
    conflicts("+intel", when="%aocc@:3.2.9999", msg="+intel with AOCC requires version 4 or newer")

    # Backport of https://github.com/lammps/lammps/pull/3726
    conflicts("+kokkos+rocm+kspace", when="@:20210929.3")
    patch(
        "https://github.com/lammps/lammps/commit/ebb8eee941e52c98054fdf96ea78ee4d5f606f47.patch?full_index=1",
        sha256="3dedd807f63a21c543d1036439099f05c6031fd98e7cb1ea7825822fc074106e",
        when="@20220623.3:20230208 +kokkos +rocm +kspace",
    )
    # Fixed in https://github.com/lammps/lammps/pull/4305
    patch(
        "https://github.com/lammps/lammps/commit/49bdc3e26449634f150602a66d0dab34d09dbc0e.patch?full_index=1",
        sha256="b8d1f08a82329e493e040de2bde9d2291af173a0fe6c7deb24750cc22823c421",
        when="@20240829 %cce",
    )

    # Older LAMMPS does not compile with Kokkos 4.x
    conflicts(
        "^kokkos@4:",
        when="@:20230802.1",
        msg="LAMMPS is incompatible with Kokkos 4.x until @20230802.1",
    )

    patch("lib.patch", when="@20170901")
    patch("660.patch", when="@20170922")
    patch("gtest_fix.patch", when="@:20210310 %aocc@3.2.0")

    # This patch merged to LAMMPS trunk at 20221222 and backported to
    # stable version 20220623.4. We still patch all other affected
    # versions here
    patch("intel-aocc.patch", when="@20220324:20220623.3,20220803:20221103 +intel %aocc")

    patch(
        "https://github.com/lammps/lammps/commit/562300996285fdec4ef74542383276898555af06.patch?full_index=1",
        sha256="e6f1b62bbfdc79d632f4cea98019202d0dd25aa4ae61a70df1164cb4f290df79",
        when="@20200721 +cuda",
    )
    patch("hip_cmake.patch", when="@20220623:20221222 ~kokkos+rocm")

    # Add large potential files
    resource(
        name="C_10_10.mesocnt",
        url="https://download.lammps.org/potentials/C_10_10.mesocnt",
        sha256="923f600a081d948eb8b4510f84aa96167b5a6c3e1aba16845d2364ae137dc346",
        expand=False,
        placement={"C_10_10.mesocnt": "potentials/C_10_10.mesocnt"},
        when="+mesont",
    )

    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        spec = self.spec

        mpi_prefix = "ENABLE"
        pkg_prefix = "ENABLE"
        if spec.satisfies("@20180629:"):
            mpi_prefix = "BUILD"
            pkg_prefix = "PKG"

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "lib"),
            self.define_from_variant("LAMMPS_EXCEPTIONS", "exceptions"),
            self.define_from_variant("{}_MPI".format(mpi_prefix), "mpi"),
            self.define_from_variant("BUILD_OMP", "openmp"),
            self.define_from_variant("BUILD_TOOLS", "tools"),
            self.define("ENABLE_TESTING", self.run_tests),
            self.define("DOWNLOAD_POTENTIALS", False),
        ]
        if spec.satisfies("~kokkos"):
            # LAMMPS can be build with the GPU package OR the KOKKOS package
            # Using both in a single build is discouraged.
            # +cuda only implies that one of the two is used
            # by default it will use the GPU package if kokkos wasn't enabled
            if spec.satisfies("+cuda"):
                args.append(self.define("PKG_GPU", True))
                args.append(self.define("GPU_API", "cuda"))
                args.append(self.define_from_variant("GPU_PREC", "gpu_precision"))
                cuda_arch = spec.variants["cuda_arch"].value
                if cuda_arch != "none":
                    args.append(self.define("GPU_ARCH", "sm_{0}".format(cuda_arch[0])))
                args.append(self.define_from_variant("CUDA_MPS_SUPPORT", "cuda_mps"))
            elif spec.satisfies("+opencl"):
                # LAMMPS downloads and bundles its own OpenCL ICD Loader by default
                args.append(self.define("USE_STATIC_OPENCL_LOADER", False))
                args.append(self.define("PKG_GPU", True))
                args.append(self.define("GPU_API", "opencl"))
                args.append(self.define_from_variant("GPU_PREC", "gpu_precision"))
            elif spec.satisfies("+rocm"):
                args.append(self.define("PKG_GPU", True))
                args.append(self.define("GPU_API", "hip"))
                args.append(self.define_from_variant("GPU_PREC", "gpu_precision"))
                args.append(self.define_from_variant("HIP_ARCH", "amdgpu_target"))
            else:
                args.append(self.define("PKG_GPU", False))
        else:
            args.append(self.define("EXTERNAL_KOKKOS", True))
            if spec.satisfies("@20240207: +kokkos+kspace"):
                args.append(self.define_from_variant("FFT_KOKKOS", "fft_kokkos"))

        if spec.satisfies("@20180629:+lib"):
            args.append(self.define("BUILD_LIB", True))

        if spec.satisfies("%aocc"):
            if spec.satisfies("+intel"):
                cxx_flags = (
                    "-O3 -fno-math-errno -fno-unroll-loops "
                    "-fveclib=AMDLIBM -muse-unaligned-vector-move"
                )
                if spec.satisfies("%aocc@4.1:4.2"):
                    cxx_flags += (
                        " -mllvm -force-gather-overhead-cost=50"
                        " -mllvm -enable-masked-gather-sequence=false"
                    )
                elif spec.satisfies("%aocc@5.0:"):
                    cxx_flags += " -mllvm -enable-aggressive-gather"
                    if spec.target >= "zen5":
                        cxx_flags += " -fenable-restrict-based-lv"

                # add -fopenmp-simd if OpenMP not already turned on
                if spec.satisfies("~openmp"):
                    cxx_flags += " -fopenmp-simd"
                cxx_flags += " -DLMP_SIMD_COMPILER -DUSE_OMP_SIMD -DLMP_INTEL_USELRT"
            else:
                cxx_flags = "-O3 -mfma -fvectorize -funroll-loops"
            args.append(self.define("CMAKE_CXX_FLAGS_RELEASE", cxx_flags))
            args.append(self.define("CMAKE_CXX_FLAGS_RELWITHDEBINFO", cxx_flags))

        # Overwrite generic cpu tune option
        cmake_tune_flags = optimization_flags(self.compiler, spec.target)
        args.append(self.define("CMAKE_TUNE_FLAGS", cmake_tune_flags))

        args.append(self.define_from_variant("LAMMPS_SIZES", "lammps_sizes"))

        args.append(self.define_from_variant("WITH_JPEG", "jpeg"))
        args.append(self.define_from_variant("WITH_PNG", "png"))
        args.append(self.define_from_variant("WITH_FFMPEG", "ffmpeg"))
        args.append(self.define_from_variant("WITH_CURL", "curl"))

        for pkg, params in self.supported_packages.items():
            if "when" not in params or spec.satisfies(params["when"]):
                opt = "{0}_{1}".format(pkg_prefix, pkg.replace("-package", "").upper())
                args.append(self.define(opt, "+{0}".format(pkg) in spec))

        if spec.satisfies("+kspace"):
            args.append(self.define_from_variant("FFT", "fft"))
            args.append(self.define_from_variant("FFT_USE_HEFFTE", "heffte"))
            if spec.satisfies("fft=fftw3 ^armpl-gcc") or spec.satisfies("fft=fftw3 ^acfl"):
                args.append(self.define("FFTW3_LIBRARY", self.spec["fftw-api"].libs[0]))
                args.append(
                    self.define("FFTW3_INCLUDE_DIR", self.spec["fftw-api"].headers.directories[0])
                )
            # Using the -DFFT_SINGLE setting trades off a little accuracy
            # for reduced memory use and parallel communication costs
            # for transposing 3d FFT data.
            args.append(self.define("FFT_SINGLE", spec.satisfies("fftw_precision=single")))

        if spec.satisfies("+user-adios") or spec.satisfies("+adios"):
            args.append(self.define("ADIOS2_DIR", self.spec["adios2"].prefix))
        if spec.satisfies("+user-plumed") or spec.satisfies("+plumed"):
            args.append(self.define("DOWNLOAD_PLUMED", False))
            if "+shared" in self.spec["plumed"]:
                args.append(self.define("PLUMED_MODE", "shared"))
            else:
                args.append(self.define("PLUMED_MODE", "static"))
        if spec.satisfies("+user-smd") or spec.satisfies("+machdyn"):
            args.append(self.define("DOWNLOAD_EIGEN3", False))
            args.append(self.define("EIGEN3_INCLUDE_DIR", self.spec["eigen"].prefix.include))
        if spec.satisfies("+user-hdnnp") or spec.satisfies("+ml-hdnnp"):
            args.append(self.define("DOWNLOAD_N2P2", False))
            args.append(self.define("N2P2_DIR", self.spec["n2p2"].prefix))

        if spec.satisfies("+rocm"):
            args.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
            if spec.satisfies("@:20231121"):
                if spec.satisfies("^hip@:5.4"):
                    args.append(self.define("HIP_PATH", f"{spec['hip'].prefix}/hip"))
                elif spec.satisfies("^hip@5.5:"):
                    args.append(self.define("HIP_PATH", spec["hip"].prefix))

        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("+intel %aocc"):
            env.append_flags("LDFLAGS", "-lalm -lm")

    def setup_run_environment(self, env):
        env.set("LAMMPS_POTENTIALS", self.prefix.share.lammps.potentials)
        if self.spec.satisfies("+python"):
            if self.spec.platform == "darwin":
                env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", self.prefix.lib)
                env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", self.prefix.lib64)
            else:
                env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
                env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)
        if self.spec.satisfies("+plugin"):
            env.prepend_path("LAMMPS_PLUGIN_PATH", self.prefix.lib.lammps.plugins)
            env.prepend_path("LAMMPS_PLUGIN_PATH", self.prefix.lib64.lammps.plugins)

    @run_after("install")
    def make_plugins_directories(self):
        os.makedirs(self.prefix.lib.lammps.plugins, exist_ok=True)
        os.makedirs(self.prefix.lib64.lammps.plugins, exist_ok=True)

    @run_after("install")
    def install_python(self):
        # do LAMMPS Python package installation using pip
        if self.spec.satisfies("@20230328: +python"):
            with working_dir("python"):
                os.environ["LAMMPS_VERSION_FILE"] = join_path(
                    self.stage.source_path, "src", "version.h"
                )
                pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
