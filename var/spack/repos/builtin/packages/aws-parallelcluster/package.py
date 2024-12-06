# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class AwsParallelcluster(PythonPackage):
    """AWS ParallelCluster is an AWS supported Open Source cluster management
    tool to deploy and manage HPC clusters in the AWS cloud."""

    homepage = "https://github.com/aws/aws-parallelcluster"
    pypi = "aws-parallelcluster/aws-parallelcluster-2.11.9.tar.gz"

    maintainers(
        "charlesg3",
        "chenwany",
        "demartinofra",
        "enrico-usai",
        "francesco-giordano",
        "gmarciani",
        "hanwen-pcluste",
        "lukeseawalker",
    )

    version("2.11.9", sha256="615de4d59d9fd56a31d4feb3aeefe685346538a8dd0c1c35b660029f891d4dfd")
    version("2.11.8", sha256="acf33f48f8e48b0bc7be20f539d61baa1e27248765ba355df753bdfca4abd3cb")
    version("2.11.7", sha256="f7c51cf1c94787f56e0661e39860ecc9275efeacc88716b7c9f14053ec7fbd35")
    version("2.11.6", sha256="4df4bcf966f523bcdf5b4f68ed0ef347eebae70a074cd098b15bc8a6be27217c")
    version("2.11.5", sha256="7499f88387cbe2cb73f9fddeee3363117f7ef1524d6a73e77bb07900040baebb")
    version("2.11.4", sha256="449537ccda57f91f4ec6ae0c94a8e2b1a789f08f80245fadb28f44a4351d5da4")
    version("2.11.3", sha256="7c1d74123f2f670846aed8fe1fcca5908bb46ec014e2dfc7d3ec8994447a37a0")
    version("2.11.2", sha256="60d96a5ea4dca4816ceffc4546549743abd1f6207c62f016c9c348adc64b2ec0")
    version("2.11.1", sha256="dc102eeb0db30fb183c1ee076e340223095fde7d9079004fde401b7ad658242d")
    version("2.11.0", sha256="ec2f54f752a355649ca065a41fa4ac19697f570a136e10e0a6548f5abad3ea8a")
    version("2.10.4", sha256="487dbf3e79f3e9b6750b1075cef4eb24956f7b310e5bd8de662b98d87491736c")
    version("2.10.3", sha256="02016358932375c1abb566c6b7f1c891fa617fc4a4ec4ce9969f87758d4039c7")
    version("2.10.2", sha256="95853535b82e8087c6635a946556ed886e68d3a77d67a375830c57d80f2bbd6e")
    version("2.10.1", sha256="b3d2ea836c08c9be1667d55a8999aae412d7c2b20f958ca5842e8fa440eb24e0")
    version("2.10.0", sha256="a7a27871b4f54cb913b0c1233e675131e9b2099549af0840d32c36b7e91b104b")
    version("2.9.1", sha256="12dc22286cd447a16931f1f8619bdd47d4543fd0de7905d52b6c6f83ff9db8a3")
    version("2.9.0", sha256="e98a8426bc46aca0860d9a2be89bbc4a90aab3ed2f60ca6c385b595fbbe79a78")
    version("2.8.1", sha256="c183dc3f053bc2445db724e561cea7f633dd5e7d467a7b3f9b2f2f703f7d5d49")
    version("2.8.0", sha256="4e67539d49fe987884a3ed7198dc13bc8a3a1778f0b3656dfe0ae899138678f2")
    version("2.7.0", sha256="7c34995acfcc256a6996541d330575fc711e1fd5735bf3d734d4e96c1dc8df60")
    version("2.6.1", sha256="2ce9015d90b5d4dc88b46a44cb8a82e8fb0bb2b4cca30335fc5759202ec1b343")
    version("2.6.0", sha256="aaed6962cf5027206834ac24b3d312da91e0f96ae8607f555e12cb124b869f0c")
    version("2.5.1", sha256="4fd6e14583f8cf81f9e4aa1d6188e3708d3d14e6ae252de0a94caaf58be76303")
    version("2.5.0", sha256="3b0209342ea0d9d8cc95505456103ad87c2d4e35771aa838765918194efd0ad3")

    depends_on("python@3.6:", when="@2.11:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", when="@:2.10", type=("build", "run"))

    depends_on("py-future@0.16.0:0.18.2", when="@:2.10", type=("build", "run"))

    depends_on("py-ipaddress@1.0.22:", type=("build", "run"))

    depends_on("py-tabulate@0.8.3:0.8.10", when="@2.11: ^python@:3.9", type=("build", "run"))
    depends_on("py-tabulate@0.8.8:0.8.10", when="@2.11: ^python@3.10:", type=("build", "run"))
    depends_on("py-tabulate@0.8.2:0.8.3", when="@:2.8", type=("build", "run"))
    depends_on("py-tabulate@0.8.2:0.8.7", when="@2.9:", type=("build", "run"))

    depends_on("py-pyyaml@5.3.1:", when="@2.9:", type=("build", "run"))
    depends_on("py-pyyaml@5.2", when="@2.6:2.10", type=("build", "run"))
    depends_on("py-pyyaml@5.1.2:", when="@:2.8", type=("build", "run"))

    depends_on("py-jinja2@2.11.3:", when="@2.11:", type=("build", "run"))
    depends_on("py-jinja2@2.11.0:", when="@2.9:", type=("build", "run"))

    depends_on("py-boto3@1.17.27:", when="@2.11:", type=("build", "run"))
    depends_on("py-boto3@1.16.14:", when="@2.10:", type=("build", "run"))
    depends_on("py-boto3@1.14.3:", when="@2.8:2.9", type=("build", "run"))
    depends_on("py-boto3@1.10.15:", when="@:2.7", type=("build", "run"))

    depends_on("py-setuptools", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        # Make sure executables work
        for exe in [
            "awsbhosts",
            "awsbkill",
            "awsbout",
            "awsbqueues",
            "awsbstat",
            "awsbsub",
            "pcluster",
        ]:
            exe = Executable(os.path.join(self.prefix.bin, exe))
            exe("--help")
