# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack.package import *


class Reframe(Package):
    """ReFrame is a framework for writing regression tests for HPC systems.
    The goal of this framework is to abstract away the complexity of the
    interactions with the system, separating the logic of a regression test
    from the low-level details, which pertain to the system configuration and
    setup. This allows users to write easily portable regression tests,
    focusing only on the functionality."""

    homepage = "https://reframe-hpc.readthedocs.io"
    url = "https://github.com/eth-cscs/reframe/archive/v2.21.tar.gz"
    git = "https://github.com/eth-cscs/reframe.git"

    # notify when the package is updated.
    maintainers("victorusu", "vkarak")

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("4.6.3", sha256="0f335e588d21a26d76beb011bc86baf80ba633d875512ecd564d0aeb320fcf2c")
    version("4.6.2", sha256="d3343815ee3d2c330b91a1cdb924ba184119ed7d9fc88a4a754b939a4259df82")
    version("4.6.1", sha256="058b05c430af26d2958851af0da32bac0f4bff1af7d78ce6a132c32bbe40ec5c")
    version("4.6.0", sha256="fcd29a419eebcb990b3e9be94b44e4ea59ce0de76f271e38f10cf5a6545ed29d")
    version("4.5.2", sha256="3f8750d0cd53261c763f9403723d87fc87361a7b0f9ba38e237d6c570fdc50df")
    version("4.5.1", sha256="8629c0adef897ccea971d6513f64acadf14e2532a543bc055213f2f5719436b5")
    version("4.5.0", sha256="5d1773d0bc76c9cd74de8688aa508a14ac7dfcdcea65d7f9473821905c60dacb")
    version("4.4.2", sha256="d773ce7f48fb177331f92920117d90cba3b9fea6b78f96f2bb83ad7239a55c3c")
    version("4.4.1", sha256="0fc8c711ccf53be8a5c687572317040e55a4edd3d935421b5957b2d9f218a0fe")
    version("4.4.0", sha256="3a5de3eab90a1b9ac5d1b272721602b1460eea6fbbda9ba691c38995f2ed3d2b")
    version("4.3.4", sha256="6a38279dd58da63316143c6f58b92798c1fd9523d50876bc2df19769f1562d3b")
    version("4.3.3", sha256="3d1a1a6d2c8e3b362dadc47f642f23f7574fb81b03be31055040afe9738829c2")
    version("4.3.2", sha256="b4e42915cf3d6c7c0f975f12eecd609ae5f165b764989f4ee066a209ff0150ae")
    version("4.3.1", sha256="63e149b516048d522c36d29c9961cba4d4e7fde9cfcdf9f599d7a1ca0358b9e0")
    version("4.3.0", sha256="89a73695a6c963eb1a2e6807b019fbad25793261829e3a7032f0b61ac3db66c8")
    version("4.2.2", sha256="c210999d506f7b0582f58f390c4e35bc89a38ca277915532f9fd68ff562e8ca9")
    version("4.2.1", sha256="c33c5406227b3fa34ee489769cb178f9dd04ead353062c21a837f31c23205bbe")
    version("4.2.0", sha256="f1d38133023b37d01fdee46b2bf472f8fd36bf410d1c909db043b9f9d7df6122")
    version("4.1.3", sha256="33e56bdabbc80cb80ac519ad9c341b296788b0954492059410674eba86044740")
    version("4.1.2", sha256="b33f44f977ed1942af5fcca0bac291daefb3353e05321832310a0c8d99d09bf6")
    version("4.1.1", sha256="68f82248dc424197e5254ca5f364565de40ed392ec02b14e8e10cab3eaf5e563")
    version("4.1.0", sha256="2f6f6793e53fd03cdc8e457b7ed4f9b2105213c26e9d5308c8f3824ea89c936c")
    version("4.0.5", sha256="4902258e5a201cb72ef9dc175a0970dcfc5869f3270a198dcd8bc47cc1a3cabd")
    version("4.0.4", sha256="a9fb10bf2dc01f721142453297e348084683acfc0b8caa38ad1daa1b5c66456e")
    version("4.0.3", sha256="ae216b0ccfda9f5f5c09f0be46cf8ab04183a0c30edf581917767dc3bb8de010")
    version("4.0.2", sha256="48ec55645256d8686e077c7a9d4d2aa7d327eec27ff2ae2c78dd1db818b76ec7")
    version("4.0.1", sha256="1680b8f0dd405dcf98be23473570595a424cbee830b2dbb665459e2974723f6f")
    version("4.0.0", sha256="50fc0462747b8b1f504912cd8072c49c46c1744567f4f1884e753abbe8d7c6e1")
    version(
        "4.0.0-dev.4", sha256="35d37ee2747807b539b2c5b75073619870371d1e0fed9778f2a33a8abd37b8a1"
    )
    version(
        "4.0.0-dev.3", sha256="830f00bcf27f693e7c0288e53a7b7fcf5aa5721ba8d451e693da018cf4af9bf4"
    )
    version(
        "4.0.0-dev.2", sha256="a02ed4077965e38a2897984b79d938a229b7e52095cd9d803e6121448efbde11"
    )
    version(
        "4.0.0-dev.1", sha256="6db55c20b79764fc1f0e0a13de062850007425fa2c7f54a113b96adee50741ed"
    )
    version(
        "4.0.0-dev.0", sha256="a96162a88a36ea0793836c492a39470010f6e63b8d9bd324c033614d27304fa6"
    )
    version("3.12.0", sha256="425cc546e24edd5b2dbfcdcb61dbbf723ca1a2a2977948e359e893514f5eb10f")
    version("3.11.2", sha256="d6f36071df316d6a5ef5ce6f0477b3385d9dac5c1b82e54ae6954dc9b68f9440")
    version("3.11.1", sha256="7f591cd8f4fbb2c6255cc8ea02e3814393355a8931ac883e9f57490fde699b63")
    version("3.11.0", sha256="3ddfef5482f0c304286a6c8f1ad0b3d75c4c61d0b9f9f8429b6157c189f2bb64")
    version("3.10.1", sha256="5fd649872bf93ba72a835896ea1a581b9b8c3e04150247be2359b95a7cdb89b5")
    version("3.10.0", sha256="b137f034be09abcf1bb8c3ceaf1a00d9c22c51c10738312eccf12c1c3e04b9ef")
    version("3.9.3", sha256="3dc28f89d85f837ad6c33f3322b5eaa0ea6df2ba5a7890cc76d79f4b96e305d5")
    version("3.9.2", sha256="2b60422615d5b52e5dca54ace0f53a712419bcce00a5515775e57e5f5f9d6e92")
    version("3.9.1", sha256="8f7f4991d1c32cc23f8b10a7509166030548bfe84e4785d017d8d797e31b0498")
    version("3.9.0", sha256="ccc36cb1db12148fe7658583e83c2717f5aae0d8c58f6b6ddd398e187c3edc3a")
    version("3.8.3", sha256="50b05b0952954215ac00a8b2e8944c946f387043660184f2fbf75995d0579d83")
    version("3.8.2", sha256="89116b320021193156f3d7f27057aeb900936502219e2aefa880bc0311052dbf")
    version("3.8.1", sha256="aa8ba4fb862de8ff333add73fd0fbb706a4d4f1381432b094bcdd7acbdcb80d4")
    version("3.8.0", sha256="b8a0486fd78786606586364968d1e2a4e7fc424d523b12b2c0ea8a227b485e30")
    version("3.7.3", sha256="52427fbbaa558082b71f73b2b8aea37340584d14dc3b1aca1e9bdd8923fa4c65")
    version("3.7.2", sha256="b4ba0f0a8788ee43471202d40be43157ec2687ad510c3b02c0869af6c48bb7d0")
    version("3.7.1", sha256="fb2efc3ad31056156e797f1d4fe705c79d20ebf66472b2144e84d4e2f4b2b125")
    version("3.7.0", sha256="aa2513fafef44ce31120c7d0e3e3788b6c8a57535499e646086bd01af88f2013")
    version("3.6.3", sha256="3616478c886c89385385d04f5bce625a690eec6bdca603cd5ac3a6f443168ac2")
    version("3.6.2", sha256="b4725e434f4cd721ca825a56a652e67aa77e7af5ed7ca00f281747585827060d")
    version("3.6.1", sha256="1ee35a2de42cdd2476c17cc15caf6a7795d976ba7b058d518da7d314e7af2136")
    version("3.6.0", sha256="de1e0ea2677f2a49af4b64544379579515db36c2164f6dc647c3fbaab5f78462")
    version("3.5.3", sha256="5e7f8b93cd672dcb702c657ec2f595d34d3335b1d16484a596a083b5ef81d7ec")
    version("3.5.2", sha256="50d461811f6bba7c9b897866a290063e1bd229e7055f5acc2de1f749b99bfce7")
    version("3.5.1", sha256="656ac4c5cddd2af3fc358a7782b0a57c86d61adaeec99181ab7e1ddc630427b7")
    version("3.5.0", sha256="81b501be4252c99f12043cb21b0b7b8059207a340fc94173b180444599773f1a")
    version("3.4.2", sha256="0c5c6dbd234b8007be929be2ccbe6a00d9a5ec75cc86e129557590b83f71acca")
    version("3.4.1", sha256="aed5752a2f687002839923c5432784d3a25d3a29d43b69122dcbf72befa0fdbf")
    version("3.4", sha256="7e74b1c7468b94e89cff4cd4a91934645ab227ad61d57a9ddf6a7d3d0726010e")
    version("3.3", sha256="9da150a051e9fa4ffea1361f30e8593261e7f6ebc71ec91ed32143539f871ad7")
    version("3.2", sha256="dc7f72e31386e549a874699067666607a72835914fef18c38ae6032ab5e5ed51")
    version("3.1", sha256="a9f6ac1ae8fdc51be8032d5cc79c117ff602f57b57aace2e195b2cfe1bd3a16f")
    version("3.0", sha256="fb76b4513c03b84f5b3bbbc988f7747e5b58f04c983b3935bab1f2e81adccb82")
    version("2.21", sha256="f35d4fda2f9672c87d3ef664d9a2d6eb0c01c88218a31772a6645c32c8934c4d")
    version("2.20", sha256="310c18d705858bbe6bd9a2dc4d382b254c1f093b0671d72363f2111e8c162ba4")
    version("2.17.3", sha256="dc8dfb2ccb9a966303879b7cdcd188c47063e9b7999cbd5d6255223b066bf357")
    version("2.17.2", sha256="092241cdc15918040aacb922c806aecb59c5bdc3ff7db034a4f355d39aecc101")
    version("2.17.1", sha256="0b0d32a892607840a7d668f5dcea6f03f7022a26b23e5042a0faf5b8c41cb146")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("docs", default=False, description="Build ReFrame's man page documentation")
    variant("gelf", default=False, description="Add graylog handler support")

    # ReFrame requires git up to version 3.1, see:
    # https://github.com/eth-cscs/reframe/issues/1464
    depends_on("git", when="@2.0:3.1", type="run")

    # supported python versions
    depends_on("python@3.5:", when="@2.0:2", type="run")
    depends_on("python@3.6:", when="@3.0:", type="run")

    # build dependencies
    depends_on("py-setuptools", type="build")

    # runtime dependencies
    depends_on("py-archspec", when="@3.7.0:", type="run")
    depends_on("py-argcomplete", when="@3.4.1:", type="run")
    depends_on("py-importlib-metadata", when="^python@:3.7", type="run")
    depends_on("py-jsonschema", type="run")
    depends_on("py-lxml", when="@3.6.0:", type="run")
    depends_on("py-pyyaml", when="@3.4.1:", type="run")
    depends_on("py-requests", when="@3.4.1:", type="run")
    depends_on("py-semver", when="@3.4.2:", type="run")

    # extension dependencies
    depends_on("py-pygelf", when="+gelf", type="run")

    # documentation dependencies
    depends_on("py-sphinx", when="+docs", type="build")
    depends_on("py-sphinx-rtd-theme", when="+docs", type="build")

    # sanity check
    sanity_check_is_file = ["bin/reframe"]
    sanity_check_is_dir = ["bin", "config", "docs", "reframe", "tutorials", "unittests"]

    # check if we can run reframe
    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_list(self):
        with working_dir(self.stage.source_path):
            reframe = Executable(self.prefix + "/bin/reframe")
            reframe("-l")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_hpctestlib(self):
        if self.spec.satisfies("@3.9.0:"):
            if not can_access("hpctestlib"):
                tty.warn("the test library was not installed")

    def install(self, spec, prefix):
        if spec.satisfies("@3.0:"):
            if "+docs" in spec:
                with working_dir("docs"):
                    make("man")
                    make("html")
                    with working_dir("man"):
                        mkdir("man1")
                        shutil.move("reframe.1", "man1")
                        mkdir("man8")
                        shutil.move("reframe.settings.8", "man8")
        install_tree(self.stage.source_path, self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix)
        if self.spec.satisfies("@3.0:"):
            if "+docs" in self.spec:
                env.prepend_path("MANPATH", self.prefix.docs.man)
