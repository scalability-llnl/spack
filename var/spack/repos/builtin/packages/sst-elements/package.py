# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstElements(AutotoolsPackage):
    """SST Elements implements a range of components for performing
    architecture simulation from node-level to system-level using
    the SST discrete event core.
    """

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/sstsimulator/sst-elements.git"
    url = "https://github.com/sstsimulator/sst-elements/releases/download/v14.1.0_Final/sstelements-14.1.0.tar.gz"

    maintainers("berquist", "naromero77")

    license("BSD-3-Clause")

    version("14.1.0", sha256="433994065810d3afee4e355173e781cd76171043cce8835bbc40887672a33350")
    version("14.0.0", sha256="68eab77febdd0138a497249d854e1cb0c3a67b1c56c4d51f1fe35df12dcd1b9c")
    version("13.1.0", sha256="ebda6ee5af858192dff8a7faf3125010001d5c439beec22afe5b9828a74adf1a")
    version("13.0.0", sha256="1f6f6b403a8c1b22a27cdf2943c9e505825ee14866891e7bc944d4471b7b0321")
    version("12.1.0", sha256="77948cf8e1f8bf8d238d475cea111c9a72b307cbf403cb429ef0426d0cf708a4")
    version("12.0.1", sha256="fe6bd9e2c14ffca77cfb31ee39410d0df3a353524b6a5a35270104dd25836e48")
    version("12.0.0", sha256="d3caacf8ba621a644151e1670dfc0fd8e91b45a583699998f94312897b0eca26")
    version("11.1.0", sha256="2dd20ecf2e0896b59eb9d65d31ef928daa0188239016216f4ad11b7e6447ca0b")
    version("11.0.0", sha256="bf265cb25afc041b74422cc5cddc8e3ae1e7c3efa3e37e699dac4e3f7629be6e")
    version("10.1.0", sha256="a790561449795dac48a84c525b8e0b09f05d0b0bff1a0da1aa2e903279a03c4a")
    version("10.0.0", sha256="ecf28ef97b27ea75be7e64cb0acb99d36773a888c1b32ba16034c62174b02693")
    version("9.1.0", sha256="e19b05aa6e59728995fc059840c79e476ba866b67887ccde7eaf52a18a1f52ca")
    version("9.0.0", sha256="6bd0743059daecadfb9c4e8cab337e2414db5630c3e3b1f2498ba133e2691692")
    version("8.0.0", sha256="805c3549eb6cb134d6aed38df441af9cb72c4457d48c9f14e9f2e89ba63b6e92")
    version("7.2.0", sha256="0a8494b38e987e26aea5d7a793ed7f2dc07a64c2805d806113e9de74ccab6269")
    version("7.1.0", sha256="c01e381d2217b745388a8871a0137bd5002b7a473f59fc5e24da8184893d93bf")
    version("7.0.0", sha256="0c842754d506df594a643ae9562aae4e652c897298504dec0a237e730600febe")
    version("6.1.0", sha256="baf553bf9097f674741be750184d5868af0add630865fd7f92a6d68d6fcdc0d4")
    version("6.0.0", sha256="0ede237fa3c8f6afd1ebb497069d91260bae12d19df67a179d739c9ded535604")

    version("develop", branch="devel")
    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Contact SST developers (https://github.com/sstsimulator)
    # if your use case requires support for:
    #   - balar
    #   - stake (riscv simulator)

    variant("pin", default=False, description="Enable the Ariel CPU model")
    variant("dramsim2", default=False, description="Build with DRAMSim2 support")
    variant("dramsim3", default=False, description="Build with DRAMSim3 support")
    variant("dumpi", default=False, description="Build with Dumpi support")
    variant("flashdimmsim", default=False, description="Build with FlashDIMMSim support")
    variant("nvdimmsim", default=False, description="Build with NVDimmSim support")
    variant("hybridsim", default=False, description="Build with HybridSim support")
    variant("goblin", default=False, description="Build with GoblinHMCSim support")
    variant("hbm", default=False, description="Build with HBM DRAMSim2 support")
    variant("ramulator", default=False, description="Build with Ramulator support")
    variant("otf", default=False, description="Build with OTF")
    variant("otf2", default=False, description="Build with OTF2")

    depends_on("python@:3.11", type=("build", "run"))
    depends_on("sst-core")
    depends_on("sst-core@develop", when="@develop")
    depends_on("sst-core@master", when="@master")

    depends_on("intel-pin", when="+pin")
    depends_on("dramsim2@2:", when="+dramsim2")
    depends_on("dramsim3@master", when="+dramsim3")
    depends_on("sst-dumpi@master", when="+dumpi")
    depends_on("flashdimmsim", when="+flashdimmsim")
    depends_on("hybridsim@2.0.1", when="+hybridsim")
    depends_on("dramsim3@master", when="+hybridsim")
    depends_on("nvdimmsim@2.0.0", when="+hybridsim")
    depends_on("nvdimmsim@2.0.0", when="+nvdimmsim")
    depends_on("goblin-hmc-sim", when="+goblin")
    depends_on("ramulator@sst", when="+ramulator")
    depends_on("hbm-dramsim2", when="+hbm")
    depends_on("otf", when="+otf")
    depends_on("otf2", when="+otf2")
    depends_on("gettext")
    depends_on("zlib-api")

    for version_name in ("master", "develop"):
        depends_on("autoconf@1.68:", type="build", when="@{}".format(version_name))
        depends_on("automake@1.11.1:", type="build", when="@{}".format(version_name))
        depends_on("libtool@1.2.4:", type="build", when="@{}".format(version_name))
        depends_on("m4", type="build", when="@{}".format(version_name))

    conflicts("+dumpi", msg="Dumpi not currently supported, contact SST Developers for help")
    conflicts("+otf", msg="OTF not currently supported, contact SST Developers for help")
    conflicts(
        "~dramsim2",
        when="+hybridsim",
        msg="hybridsim requires dramsim2, spec should include +dramsim2",
    )
    conflicts(
        "~nvdimmsim",
        when="+hybridsim",
        msg="hybridsim requires nvdimmsim, spec should include +nvdimmsim",
    )

    # force out-of-source builds
    build_directory = "spack-build"

    @when("@develop,master")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("autogen.sh")

    def configure_args(self):
        spec = self.spec
        args = []

        if "+pdes_mpi" in spec["sst-core"]:
            env["CC"] = spec["mpi"].mpicc
            env["CXX"] = spec["mpi"].mpicxx
            env["F77"] = spec["mpi"].mpif77
            env["FC"] = spec["mpi"].mpifc

        if "+pin" in spec:
            args.append("--with-pin=%s" % spec["intel-pin"].prefix)

        if "+dramsim2" in spec or "+hybridsim" in spec:
            args.append("--with-dramsim=%s" % spec["dramsim2"].prefix)

        if "+dramsim3" in spec:
            args.append("--with-dramsim3=%s" % spec["dramsim3"].prefix)

        if "+dumpi" in spec:
            args.append("--with-dumpi=%s" % spec["sst-dumpi"].prefix)

        if "+flashdimmsim" in spec:
            args.append("--with-fdsim=%s" % spec["flashdimmsim"].prefix)

        if "+nvdimmsim" in spec or "+hybridsim" in spec:
            args.append("--with-nvdimmsim=%s" % spec["nvdimmsim"].prefix)

        if "+hybridsim" in spec:
            args.append("--with-hybridsim=%s" % spec["hybridsim"].prefix)

        if "+goblin" in spec:
            args.append("--with-goblin-hmcsim=%s" % spec["goblin-hmc-sim"].prefix)

        if "+hbm" in spec:
            args.append("--with-hbmdramsim=%s" % spec["hbm-dramsim2"].prefix)

        if "+ramulator" in spec:
            args.append("--with-ramulator=%s" % spec["ramulator"].prefix)

        if "+otf2" in spec:
            args.append("--with-otf2=%s" % spec["otf2"].prefix)

        if "+otf" in spec:
            args.append("--with-otf=%s" % spec["otf"].prefix)

        args.append("--with-sst-core=%s" % spec["sst-core"].prefix)
        return args

    def setup_run_environment(self, env):
        """Setup runtime environment for SST Elements."""

        if "+pin" in self.spec:
            env.set("INTEL_PIN_DIRECTORY", self.spec["intel-pin"].prefix)
