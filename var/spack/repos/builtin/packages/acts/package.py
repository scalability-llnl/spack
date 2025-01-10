# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Acts(CMakePackage, CudaPackage):
    """
    A Common Tracking Software (Acts)

    This project contains an experiment-independent set of track reconstruction
    tools. The main philosophy is to provide high-level track reconstruction
    modules that can be used for any tracking detector. The description of the
    tracking detector's geometry is optimized for efficient navigation and
    quick extrapolation of tracks. Converters for several common geometry
    description languages exist. Having a highly performant, yet largely
    customizable implementation of track reconstruction algorithms was a
    primary objective for the design of this toolset. Additionally, the
    applicability to real-life HEP experiments plays major role in the
    development process. Apart from algorithmic code, this project also
    provides an event data model for the description of track parameters and
    measurements.

    Key features of this project include: tracking geometry description which
    can be constructed from TGeo, DD4Hep, or GDML input, simple and efficient
    event data model, performant and highly flexible algorithms for track
    propagation and fitting, basic seed finding algorithms.
    """

    homepage = "https://acts.web.cern.ch/ACTS/"
    git = "https://github.com/acts-project/acts.git"
    list_url = "https://github.com/acts-project/acts/releases/"
    maintainers("wdconinc", "stephenswat")

    tags = ["hep"]

    license("MPL-2.0")

    # Supported Acts versions
    version("main", branch="main")
    version("master", branch="main", deprecated=True)  # For compatibility
    version("38.2.0", commit="9cb8f4494656553fd9b85955938b79b2fac4c9b0", submodules=True)
    version("38.1.0", commit="8a20c88808f10bf4fcdfd7c6e077f23614c3ab90", submodules=True)
    version("38.0.0", commit="0a6b5155e29e3b755bf351b8a76067fff9b4214b", submodules=True)
    version("37.4.0", commit="4ae9a44f54c854599d1d753222ec36e0b5b4e9c7", submodules=True)
    version("37.3.0", commit="b3e856d4dadcda7d1a88a9b846ce5a7acd8410c4", submodules=True)
    version("37.2.0", commit="821144dc40d35b44aee0d7857a0bd1c99e4a3932", submodules=True)
    version("37.1.0", commit="fa6ad4d52e0bd09cf8c78507fcbb18e9ac2c87a3", submodules=True)
    version("37.0.1", commit="998b9c9dd42d5160c2540f8fa820505869bfdb79", submodules=True)
    version("37.0.0", commit="117feaaadc7a2336755274e0cd70ba58a047a1de", submodules=True)
    version("36.3.2", commit="01e124d253a3c9c9b9f5d2fde16682ce9d4599cd", submodules=True)
    version("36.3.1", commit="b58e5b0c33fb8423ce60a6a45f333edd0d178acd", submodules=True)
    version("36.3.0", commit="3b875cebabdd10462e224279558429f49ed75945", submodules=True)
    version("36.2.0", commit="e2fb53da911dc481969e56d635898a46b8d78df9", submodules=True)
    version("36.1.0", commit="3f19d1a0eec1d11937d66d0ef603f0b25b9b4e96", submodules=True)
    version("36.0.0", commit="6eca77c45b136861272694edbb61bb77200948a5", submodules=True)
    version("35.2.0", commit="b3b09f46d064c43050dd3d21cdf51d7a412134fc", submodules=True)
    version("35.1.0", commit="9dfb47b8edeb8b9c75115462079bcb003dd3f031", submodules=True)
    version("35.0.0", commit="352b423ec31934f825deb9897780246d60ffc44e", submodules=True)
    version("34.1.0", commit="8e1b7a659d912cd98db9d700906ff59e708da574", submodules=True)
    version("34.0.0", commit="daafd83adf0ce50f9667f3c9d4791a459e39fd1b", submodules=True)
    version("33.1.0", commit="00591a593a648430820e980b031301d25c18f1c7", submodules=True)
    version("33.0.0", commit="f6ed9013e76120137ae456583a04b554d88d9452", submodules=True)
    version("32.1.0", commit="5333c67b49b4bfcd45558090e4ba37b4f86b82db", submodules=True)
    version("32.0.2", commit="3d23e16a2d0ba68ce5a596ced16883f90de1fae4", submodules=True)
    version("32.0.1", commit="6317634ec16eb40e52ca85445a014e378c9a4829", submodules=True)
    version("32.0.0", commit="9385e36691bb2687437c39ad02ddb2ac21acccdc", submodules=True)
    version("31.2.0", commit="1d2e90f534ff2c9bf1c40914980b426f4b5d3096", submodules=True)
    version("31.1.0", commit="95c3ceef79a7b68fcfc7fd558c3134d0c7529dac", submodules=True)
    version("31.0.0", commit="2cf3fe0254d2bf9434899fdcfbe316366a970956", submodules=True)
    version("30.3.2", commit="76826f208f5929d8326798c87263f2563d0ae7e9", submodules=True)
    version("30.3.1", commit="bbee459dd93855417d5717d53cbbb2bace7de2bb", submodules=True)
    version("30.3.0", commit="311acb9ab41c2d79a4b90b193e5b25297182d670", submodules=True)
    version("30.2.0", commit="264b0a3214cbf8ca013623fc196e2d90d647c58f", submodules=True)
    version("30.1.1", commit="3d43492b2775e62051e9ad31f06b91d6e2357ab9", submodules=True)
    version("30.1.0", commit="60d9eec916f6c81373858c8d99d821861d7efeb8", submodules=True)
    version("30.0.0", commit="00fa3fabac86a1e65198d4b94dd263b1c731a84c", submodules=True)
    version("29.2.0", commit="b2d65308399d8f653fa8bdd73a2a203c58608358", submodules=True)
    version("29.1.0", commit="4681c3b142db469b00ca03e92e6b237f7c89d141", submodules=True)
    version("29.0.0", commit="9c6e4597af39f826e17d46850fdb407a48817ba6", submodules=True)
    version("28.2.0", commit="c612e7c625f961330e383fb7856cc7398dd82881", submodules=True)
    version("28.1.0", commit="08e51b5f93c0d09f2d1e7e4f062e715072ec3e9b", submodules=True)
    version("28.0.0", commit="0d8aa418c00e8f79bab2cf88234f3433670b447c", submodules=True)
    version("27.1.0", commit="219480220738318fbedb943cac85415687d75b66", submodules=True)
    version("27.0.0", commit="4d7029bd4e9285fcda2770aef6d78a7f833cb14f", submodules=True)
    version("26.0.0", commit="d43af5c3bcf44f593721940e569ba267579e0334", submodules=True)
    version("25.0.1", commit="1772d2a1a96acfd918a538c14a9e24fe7ce7f50b", submodules=True)
    version("25.0.0", commit="c7b538d7b92fe6bffd619de7885b7ea97ddcd26a", submodules=True)
    version("24.0.0", commit="4da149cd27ae3802a54f21a48e1757e475aa8189", submodules=True)
    version("23.5.0", commit="8fad985ab78ceb9aaec25d1f658197833e4586fa", submodules=True)
    version("23.4.0", commit="52723f7e7a2e6f9f59d6d7ca1cf183ca1cd43380", submodules=True)
    version("23.3.0", commit="ec3e69da90b9dff52bdbe30cb7953417b6184d4b", submodules=True)
    version("23.2.1", commit="a9fe5167d4d3b6b53b28d3b17060a5f3e380cf3a", submodules=True)
    version("23.2.0", commit="bc3120d23a72cfdd0ea8f9a0997f59caf311672b", submodules=True)
    version("23.1.0", commit="4479f182a37650a538344f749b967d6f757bdf60", submodules=True)
    version("23.0.0", commit="5af1b1b5feb8ca8f4c2c69106a1b9ef612c70d9c", submodules=True)
    version("22.0.1", commit="a4ac99dd72828c5eb3fac06e146f3391958fca8c", submodules=True)
    version("22.0.0", commit="0fb6f8d2ace65338915451201e9ceb6cee11fb5e", submodules=True)
    version("21.1.1", commit="8ae825de246e8e574d05d9eaf05ba4a937c69aa9", submodules=True)
    version("21.1.0", commit="3b4b5c741c8541491d496a36b917b00b344d52d1", submodules=True)
    version("21.0.0", commit="d8cb0fac3a44e1d44595a481f977df9bd70195fb", submodules=True)
    version("20.3.0", commit="b1859b322744cb033328fd57d9e74fb5326aa56b", submodules=True)
    version("20.2.0", commit="7750c1d24714314e8de716b92ebcd4a92cc4e303", submodules=True)
    version("20.1.0", commit="be36226fb1be88d7be7c9b17a1c1f6e76ff0e006", submodules=True)
    version("20.0.0", commit="3740e6cdbfb1f75d8e481686acdfa5b16d3c41a3", submodules=True)
    version("19.11.0", commit="d56ca2583e55b48e77c853b7c567070d07fc1cae", submodules=True)
    version("19.10.0", commit="2d07f60eb2280a46af1085600ec8327679bbb630", submodules=True)
    version("19.9.0", commit="b655e18929ae0ccb6926d8e217b1b3fc02978d35", submodules=True)
    version("19.8.0", commit="7582072dbaa70802264f20b392de4313afd25667", submodules=True)
    version("19.7.0", commit="03cf7a3ae74b632b3f89416dc27cc993c9ae4628", submodules=True)
    version("19.6.0", commit="333082914e6a51b381abc1cf52856829e3eb7890", submodules=True)
    version("19.5.0", commit="bf9f0270eadd8e78d283557b7c9070b80dece4a7", submodules=True)
    version("19.4.0", commit="498af243755219486c26d32fb125b7ebf2557166", submodules=True)
    version("19.3.0", commit="747053f60254c5ad3aa1fe7b18ae89c19029f4a6", submodules=True)
    version("19.2.0", commit="adf079e0f7e278837093bf53988da73730804e22", submodules=True)
    version("19.1.0", commit="82f42a2cc80d4259db251275c09b84ee97a7bd22", submodules=True)
    version("19.0.0", commit="1ce9c583150060ba8388051685433899713d56d9", submodules=True)
    version("18.0.0", commit="fe03b5af6ca2b092dec87c4cef77dd552bbbe719", submodules=True)
    version("17.1.0", commit="0d9c3a6da022da48d6401e10c273896a1f775a9e", submodules=True)
    version("17.0.0", commit="ccbf4c7d4ec3698bac4db9687fab2455a3f9c203", submodules=True)
    version("16.0.0", commit="9bd86921155e708189417b5a8019add10fd5b273", submodules=True)
    version("15.1.0", commit="a96e6db7de6075e85b6d5346bc89845eeb89b324", submodules=True)
    version("15.0.1", commit="b9469b8914f6a1bc47af0998eb7c9e8e20e4debc", submodules=True)
    version("15.0.0", commit="0fef9e0831a90e946745390882aac871b211eaac", submodules=True)
    version("14.1.0", commit="e883ab6acfe5033509ad1c27e8e2ba980dfa59f6", submodules=True)
    version("14.0.0", commit="f902bef81b60133994315c13f7d32d60048c79d8", submodules=True)
    version("13.0.0", commit="ad05672e48b693fd37156f1ad62ed57aa82f858c", submodules=True)
    version("12.0.1", commit="a80d1ef995d8cdd4190cc09cb249276a3e0161f4", submodules=True)
    version("12.0.0", commit="e0aa4e7dcb70df025576e050b6e652a2f736454a", submodules=True)
    version("11.0.0", commit="eac3def261f65b343af6d8ce4bc40443ac57b57e")
    version("10.0.0", commit="9bfe0b83f277f686408b896a84d2b9b53610f623")
    version("9.02.0", commit="c438ee490e94eaf1c854a336ef54f398da637a48")
    version("9.01.0", commit="bf8fd4c03dd94f497d8501df510d8f6a48434afd")
    version("9.00.1", commit="7d59bc508d898d2cb67ba05a7150a978b9fcc32d")
    version("9.00.0", commit="e6e3092bf3a9411aac7c11a24d7586abddb75d59")
    version("8.03.0", commit="601c0a18b6738cae81c3e23422cfeb3ec7bddce9")
    version("8.02.0", commit="f25cf639915fc2ac65b03882ad3eb11fb037ed00")
    version("8.01.0", commit="ccc8c77bbc011f3adc020c565a509815be0ea029")
    version("8.00.0", commit="50c972823144c007b406ae12d7ca25a1e0c35532")
    version("7.00.0", commit="e663df7ab023bdb5ef206202efc2e54ccb71d416")
    version("6.00.0", commit="a5cf04acd4b1a2c625e0826189109472a3392558")
    version("5.00.0", commit="df77b91a7d37b8db6ed028a4d737014b5ad86bb7")
    version("4.01.0", commit="c383bf434ef69939b47e840e0eac0ba632e6af9f")
    version("4.00.0", commit="ed64b4b88d366b63adc4a8d1afe5bc97aa5751eb")
    version("3.00.0", commit="e20260fccb469f4253519d3f0ddb3191b7046db3")
    version("2.00.0", commit="8708eae2b2ccdf57ab7b451cfbba413daa1fc43c")
    version("1.02.1", commit="f6ebeb9a28297ba8c54fd08b700057dd4ff2a311")
    version("1.02.0", commit="e69b95acc9a264e63aded7d1714632066e090542")
    version("1.01.0", commit="836fddd02c3eff33825833ff97d6abda5b5c20a0")
    version("1.00.0", commit="ec9ce0bcdc837f568d42a12ddf3fc9c80db62f5d")
    version("0.32.0", commit="a4cedab7e727e1327f2835db29d147cc86b21054")
    version("0.31.0", commit="cfbd901555579a2f32f4efe2b76a7048442b42c3")
    version("0.30.0", commit="a71ef0a9c742731611645214079884585a92b15e")
    version("0.29.0", commit="33aa3e701728112e8908223c4a7fd521907c8ea4")
    version("0.28.0", commit="55626b7401eeb93fc562e79bcf385f0ad0ac48bf")
    version("0.27.1", commit="8ba3010a532137bc0ab6cf83a38b483cef646a01")
    version("0.27.0", commit="f7b1a1c27d5a95d08bb67236ad0e117fcd1c679f")
    version("0.26.0", commit="cf542b108b31fcc349fc18fb0466f889e4e42aa6")
    version("0.25.2", commit="76bf1f3e4be51d4d27126b473a2caa8d8a72b320")
    version("0.25.1", commit="6e8a1ea6d2c7385a78e3e190efb2a8a0c1fa957f")
    version("0.25.0", commit="0aca171951a214299e8ff573682b1c5ecec63d42")
    version("0.24.0", commit="ef4699c8500bfea59a5fe88bed67fde2f00f0adf")
    version("0.23.0", commit="dc443dd7e663bc4d7fb3c1e3f1f75aaf57ffd4e4")
    version("0.22.1", commit="ca1b8b1645db6b552f44c48d2ff34c8c29618f3a")
    version("0.22.0", commit="2c8228f5843685fc0ae69a8b95dd8fc001139efb")
    version("0.21.0", commit="10b719e68ddaca15b28ac25b3daddce8c0d3368d")
    version("0.20.0", commit="1d37a849a9c318e8ca4fa541ef8433c1f004637b")
    version("0.19.0", commit="408335636486c421c6222a64372250ef12544df6")
    version("0.18.0", commit="d58a68cf75b52a5e0f563bc237f09250aa9da80c")
    version("0.17.0", commit="0789f654ff484b013fd27e5023cf342785ea8d97")
    version("0.16.0", commit="b3d965fe0b8ae335909d79114ef261c6b996773a")
    version("0.15.0", commit="267c28f69c561e64369661a6235b03b5a610d6da")
    version("0.14.0", commit="38d678fcb205b77d60326eae913fbb1b054acea1")
    version("0.13.0", commit="b33f7270ddbbb33050b7ec60b4fa255dc2bfdc88")
    version("0.12.1", commit="a8b3d36e7c6cb86487637589e0eff7bbe626054a")
    version("0.12.0", commit="f9cda77299606d78c889fb1db2576c1971a271c4")
    version("0.11.1", commit="c21196cd6c3ecc6da0f14d0a9ef227a274be584b")
    version("0.11.0", commit="22bcea1f19adb0021ca61b843b95cfd2462dd31d")
    version("0.10.5", commit="b6f7234ca8f18ee11e57709d019c14bf41cf9b19")
    version("0.10.4", commit="42cbc359c209f5cf386e620b5a497192c024655e")
    version("0.10.3", commit="a3bb86b79a65b3d2ceb962b60411fd0df4cf274c")
    version("0.10.2", commit="64cbf28c862d8b0f95232b00c0e8c38949d5015d")
    version("0.10.1", commit="0692dcf7824efbc504fb16f7aa00a50df395adbc")
    version("0.10.0", commit="30ef843cb00427f9959b7de4d1b9843413a13f02")
    version("0.09.5", commit="12b11fe8b0d428ccb8e92dda7dc809198f828672")
    version("0.09.4", commit="e5dd9fbe179201e70347d1a3b9fa1899c226798f")
    version("0.09.3", commit="a8f31303ee8720ed2946bfe2d59e81d0f70e307e")
    version("0.09.2", commit="4e1f7fa73ffe07457080d787e206bf6466fe1680")
    version("0.09.1", commit="69c451035516cb683b8f7bc0bab1a25893e9113d")
    version("0.09.0", commit="004888b0a412f5bbaeef2ffaaeaf2aa182511494")
    version("0.08.2", commit="c5d7568714e69e7344582b93b8d24e45d6b81bf9")
    version("0.08.1", commit="289bdcc320f0b3ff1d792e29e462ec2d3ea15df6")
    version("0.08.0", commit="99eedb38f305e3a1cd99d9b4473241b7cd641fa9")

    depends_on("cxx", type="build")  # generated

    # Variants that affect the core Acts library
    variant(
        "benchmarks", default=False, description="Build the performance benchmarks", when="@0.16:"
    )
    _cxxstd_values = (
        conditional("14", when="@:0.8.1"),
        conditional("17", when="@:35"),
        conditional("20", when="@24:"),
    )
    _cxxstd_common = {
        "values": _cxxstd_values,
        "multi": False,
        "description": "Use the specified C++ standard when building.",
    }
    variant("cxxstd", default="17", when="@:35", **_cxxstd_common)
    variant("cxxstd", default="20", when="@36:", **_cxxstd_common)
    variant(
        "examples",
        default=False,
        description="Build the examples",
        when="@0.23:16 +digitization +fatras +identification +json +tgeo",
    )
    variant(
        "examples",
        default=False,
        description="Build the examples",
        when="@17:34 +fatras +identification +json +tgeo",
    )
    variant(
        "examples",
        default=False,
        description="Build the examples",
        when="@35: +fatras +json +tgeo",
    )
    variant("integration_tests", default=False, description="Build the integration tests")
    variant("unit_tests", default=False, description="Build the unit tests")
    variant(
        "log_failure_threshold",
        default="MAX",
        description="Log level above which examples should auto-crash",
    )
    _scalar_values = ["float", "double"]
    variant(
        "scalar",
        default="double",
        values=_scalar_values,
        multi=False,
        sticky=True,
        description="Scalar type to use throughout Acts.",
    )

    # Variants that enable / disable Acts plugins
    variant("alignment", default=False, description="Build the alignment package", when="@13:")
    variant(
        "autodiff",
        default=False,
        description="Build the auto-differentiation plugin",
        when="@1.2:32",
    )
    variant("dd4hep", default=False, description="Build the DD4hep plugin", when="+tgeo")
    variant(
        "digitization",
        default=False,
        description="Build the geometric digitization plugin",
        when="@:16",
    )
    variant("edm4hep", default=False, description="Build EDM4hep plugin", when="@25:")
    # FIXME: Can't build Exa.TrkX plugin+examples yet, missing cuGraph dep
    variant(
        "fatras",
        default=False,
        description="Build the FAst TRAcking Simulation package",
        when="@0.16:",
    )
    variant("fatras_geant4", default=False, description="Build Geant4 Fatras package")
    variant("geomodel", default=False, description="Build GeoModel plugin", when="@33:")
    variant(
        "identification", default=False, description="Build the Identification plugin", when="@:34"
    )
    variant("json", default=False, description="Build the Json plugin")
    variant("legacy", default=False, description="Build the Legacy package")
    variant("mlpack", default=False, description="Build MLpack plugin", when="@25:31")
    variant("onnx", default=False, description="Build ONNX plugin")
    variant("odd", default=False, description="Build the Open Data Detector", when="@19.1:")
    variant("podio", default=False, description="Build Podio plugin", when="@30.3:")
    variant(
        "profilecpu",
        default=False,
        description="Enable CPU profiling using gperftools",
        when="@19.3:",
    )
    variant(
        "profilemem",
        default=False,
        description="Enable memory profiling using gperftools",
        when="@19.3:",
    )
    variant("sycl", default=False, description="Build the SyCL plugin", when="@1:34")
    variant(
        "tgeo", default=False, description="Build the TGeo plugin", when="@:34 +identification"
    )
    variant("tgeo", default=False, description="Build the TGeo plugin", when="@35:")
    variant("traccc", default=False, description="Build the Traccc plugin", when="@35.1:")

    # Variants that only affect Acts examples for now
    variant(
        "binaries",
        default=False,
        description="Build the examples binaries",
        when="@23:32 +examples",
    )
    variant(
        "edm4hep",
        default=False,
        description="Build the EDM4hep examples",
        when="@19.4.0:24 +examples",
    )
    variant(
        "geant4",
        default=False,
        description="Build the Geant4-based examples",
        when="@0.23: +examples",
    )
    variant(
        "hepmc3",
        default=False,
        description="Build the HepMC3-based examples",
        when="@0.23: +examples",
    )
    variant(
        "pythia8",
        default=False,
        description="Build the Pythia8-based examples",
        when="@0.23: +examples",
    )
    variant(
        "python",
        default=False,
        description="Build python bindings for the examples",
        when="@14: +examples",
    )
    variant("svg", default=False, description="Build ActSVG display plugin", when="@20.1:")
    variant(
        "tbb",
        default=True,
        description="Build the examples with Threading Building Blocks library",
        when="@19.8:19,20.1:37.2 +examples",
    )
    variant("analysis", default=False, description="Build analysis applications in the examples")

    # Build dependencies
    depends_on("acts-dd4hep", when="@19 +dd4hep")
    with when("+svg"):
        depends_on("actsvg@0.4.20:", when="@20.1:")
        depends_on("actsvg@0.4.28:", when="@23.2:")
        depends_on("actsvg@0.4.29:", when="@23.4:")
        depends_on("actsvg@0.4.30:", when="@23.5:")
        depends_on("actsvg@0.4.33:", when="@25:27")
        depends_on("actsvg@0.4.35:", when="@28:")
        depends_on("actsvg@0.4.39:", when="@32:")
        depends_on("actsvg@0.4.40:", when="@32.1:")
        depends_on("actsvg@0.4.50:", when="@37:")
    depends_on("acts-algebra-plugins @0.24:", when="+traccc")
    depends_on("autodiff @0.6:", when="@17: +autodiff")
    depends_on("autodiff @0.5.11:0.5.99", when="@1.2:16 +autodiff")
    depends_on("boost @1.62:1.69 +program_options +test", when="@:0.10.3")
    depends_on("boost @1.71: +filesystem +program_options +test", when="@0.10.4:")
    depends_on("cmake @3.14:", type="build")
    depends_on("covfie @0.10:", when="+traccc")
    depends_on("cuda @12:", when="+traccc")
    depends_on("dd4hep @1.11: +dddetectors +ddrec", when="+dd4hep")
    depends_on("dd4hep @1.21: +dddetectors +ddrec", when="@20: +dd4hep")
    depends_on("dd4hep +ddg4", when="+dd4hep +geant4 +examples")
    depends_on("detray @0.72.1:", when="+traccc")
    depends_on("detray @0.75.3:", when="@37: +traccc")
    depends_on("edm4hep @0.4.1:", when="+edm4hep")
    depends_on("edm4hep @0.7:", when="@25: +edm4hep")
    depends_on("eigen @3.3.7:", when="@15.1:")
    depends_on("eigen @3.3.7:3.3.99", when="@:15.0")
    depends_on("eigen @3.4:", when="@36.1:")
    depends_on("geant4", when="+fatras_geant4")
    depends_on("geant4", when="+geant4")
    depends_on("geomodel +geomodelg4", when="+geomodel")
    depends_on("geomodel @4.6.0:", when="+geomodel")
    depends_on("geomodel @6.3.0:", when="+geomodel @36.1:")
    depends_on("git-lfs", when="@12.0.0:")
    depends_on("gperftools", when="+profilecpu")
    depends_on("gperftools", when="+profilemem")
    depends_on("hepmc3 @3.2.1:", when="+hepmc3")
    depends_on("heppdt", when="+hepmc3 @:4.0")
    depends_on("intel-tbb @2020.1:", when="+examples +tbb")
    depends_on("intel-tbb @2020.1:", when="+examples @37.3:")
    depends_on("mlpack@3.1.1:", when="+mlpack")
    depends_on("nlohmann-json @3.9.1:", when="@0.14: +json")
    depends_on("nlohmann-json @3.10.5:", when="@37: +json")
    depends_on("podio @0.6:", when="@25: +edm4hep")
    depends_on("podio @0.16:", when="@30.3: +edm4hep")
    depends_on("podio @:0", when="@:35 +edm4hep")
    depends_on("podio @0.16:", when="+podio")
    depends_on("podio @:0", when="@:35 +podio")
    depends_on("pythia8", when="+pythia8")
    depends_on("python", when="+python")
    depends_on("python@3.8:", when="+python @19.11:19")
    depends_on("python@3.8:", when="+python @21:")
    depends_on("py-onnxruntime@:1.12", when="+onnx @:23.2")
    depends_on("py-onnxruntime@1.12:", when="+onnx @23.3:")
    depends_on("py-pybind11 @2.6.2:", when="+python @18:")
    depends_on("py-pybind11 @2.13.1:", when="+python @36:")
    depends_on("py-pytest", when="+python +unit_tests")

    with when("+tgeo"):
        depends_on("root @6.10:")
        depends_on("root @6.20:", when="@0.8.1:")

    depends_on("sycl", when="+sycl")
    depends_on("vecmem@0.4: +sycl", when="+sycl")

    # ACTS imposes requirements on the C++ standard values used by ROOT
    for _cxxstd in _cxxstd_values:
        for _v in _cxxstd:
            depends_on(f"geant4 cxxstd={_v.value}", when=f"cxxstd={_v.value} +geant4")
            depends_on(f"geant4 cxxstd={_v.value}", when=f"cxxstd={_v.value} +fatras_geant4")
            depends_on(f"root cxxstd={_v.value}", when=f"cxxstd={_v.value} +tgeo")

    # When the traccc plugin is enabled, detray should match the Acts scalars
    with when("+traccc"):
        for _scalar in _scalar_values:
            depends_on(f"detray scalar={_scalar}", when=f"scalar={_scalar}")

    # ACTS has been using C++17 for a while, which precludes use of old GCC
    conflicts("%gcc@:7", when="@0.23:")
    # When using C++20, disable gcc 9 and lower.
    conflicts("%gcc@:9", when="cxxstd=20")
    # See https://github.com/acts-project/acts/pull/3512
    conflicts("^boost@1.85.0")
    # See https://github.com/acts-project/acts/pull/3921
    conflicts("^edm4hep@0.99:", when="@:37")

    def cmake_args(self):
        spec = self.spec

        def cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies("+" + spack_variant)
            return f"-DACTS_BUILD_{cmake_label}={enabled}"

        def enable_cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies(spack_variant)
            return f"-DACTS_ENABLE_{cmake_label}={enabled}"

        def example_cmake_variant(cmake_label, spack_variant, type="BUILD"):
            enabled = spec.satisfies("+examples +" + spack_variant)
            return f"-DACTS_{type}_EXAMPLES_{cmake_label}={enabled}"

        def plugin_label(plugin_name):
            if spec.satisfies("@0.33:"):
                return "PLUGIN_" + plugin_name
            else:
                return plugin_name + "_PLUGIN"

        def plugin_cmake_variant(plugin_name, spack_variant):
            return cmake_variant(plugin_label(plugin_name), spack_variant)

        integration_tests_label = "INTEGRATIONTESTS"
        unit_tests_label = "UNITTESTS"
        legacy_plugin_label = "LEGACY_PLUGIN"
        if spec.satisfies("@:0.15"):
            integration_tests_label = "INTEGRATION_TESTS"
            unit_tests_label = "TESTS"
        if spec.satisfies("@:0.32"):
            legacy_plugin_label = "LEGACY"

        args = [
            cmake_variant("ALIGNMENT", "alignment"),
            cmake_variant("ANALYSIS_APPS", "analysis"),
            plugin_cmake_variant("AUTODIFF", "autodiff"),
            cmake_variant("BENCHMARKS", "benchmarks"),
            example_cmake_variant("BINARIES", "binaries"),
            plugin_cmake_variant("CUDA", "cuda"),
            plugin_cmake_variant("DD4HEP", "dd4hep"),
            example_cmake_variant("DD4HEP", "dd4hep"),
            plugin_cmake_variant("DIGITIZATION", "digitization"),
            plugin_cmake_variant("EDM4HEP", "edm4hep"),
            example_cmake_variant("EDM4HEP", "edm4hep"),
            cmake_variant("EXAMPLES", "examples"),
            cmake_variant("FATRAS", "fatras"),
            cmake_variant("FATRAS_GEANT4", "fatras_geant4"),
            example_cmake_variant("GEANT4", "geant4"),
            plugin_cmake_variant("GEANT4", "geant4"),
            plugin_cmake_variant("GEOMODEL", "geomodel"),
            example_cmake_variant("HEPMC3", "hepmc3"),
            plugin_cmake_variant("IDENTIFICATION", "identification"),
            cmake_variant(integration_tests_label, "integration_tests"),
            plugin_cmake_variant("JSON", "json"),
            cmake_variant(legacy_plugin_label, "legacy"),
            plugin_cmake_variant("MLPACK", "mlpack"),
            cmake_variant("ODD", "odd"),
            plugin_cmake_variant("ONNX", "onnx"),
            enable_cmake_variant("CPU_PROFILING", "profilecpu"),
            enable_cmake_variant("MEMORY_PROFILING", "profilemem"),
            plugin_cmake_variant("PODIO", "podio"),
            example_cmake_variant("PYTHIA8", "pythia8"),
            example_cmake_variant("PYTHON_BINDINGS", "python"),
            self.define_from_variant("ACTS_CUSTOM_SCALARTYPE", "scalar"),
            plugin_cmake_variant("ACTSVG", "svg"),
            plugin_cmake_variant("SYCL", "sycl"),
            plugin_cmake_variant("TGEO", "tgeo"),
            example_cmake_variant("TBB", "tbb", "USE"),
            plugin_cmake_variant("TRACCC", "traccc"),
            cmake_variant(unit_tests_label, "unit_tests"),
        ]

        log_failure_threshold = spec.variants["log_failure_threshold"].value
        args.append(f"-DACTS_LOG_FAILURE_THRESHOLD={log_failure_threshold}")
        if spec.satisfies("@19.4.0:"):
            args.append("-DACTS_ENABLE_LOG_FAILURE_THRESHOLD=ON")

        # Use dependencies provided by spack
        if spec.satisfies("@20.3:"):
            args.append("-DACTS_USE_SYSTEM_LIBS=ON")
            if spec.satisfies("@35.1:36.0"):
                args.append("-DACTS_USE_SYSTEM_DFELIBS=OFF")
        else:
            if spec.satisfies("+autodiff"):
                args.append("-DACTS_USE_SYSTEM_AUTODIFF=ON")

            if spec.satisfies("@19:20.2 +dd4hep"):
                args.append("-DACTS_USE_SYSTEM_ACTSDD4HEP=ON")

            if spec.satisfies("@0.33: +json"):
                args.append("-DACTS_USE_SYSTEM_NLOHMANN_JSON=ON")
            elif spec.satisfies("@0.14.0:0.32 +json"):
                args.append("-DACTS_USE_BUNDLED_NLOHMANN_JSON=OFF")

            if spec.satisfies("@18: +python"):
                args.append("-DACTS_USE_SYSTEM_PYBIND11=ON")

            if spec.satisfies("@20.1: +svg"):
                args.append("-DACTS_USE_SYSTEM_ACTSVG=ON")

            if spec.satisfies("@14: +vecmem"):
                args.append("-DACTS_USE_SYSTEM_VECMEM=ON")

        if spec.satisfies("+cuda"):
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch != "none":
                args.append(f"-DCUDA_FLAGS=-arch=sm_{cuda_arch[0]}")
                arch_str = ";".join(self.spec.variants["cuda_arch"].value)
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))

        args.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))

        return args
