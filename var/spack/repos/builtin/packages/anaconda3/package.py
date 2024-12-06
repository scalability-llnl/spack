# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from os.path import split

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Anaconda3(Package):
    """
    Anaconda is a free and open-source distribution of the Python and R
    programming languages for scientific computing, that aims to simplify
    package management and deployment. Package versions are managed by
    the package management system conda.
    """

    homepage = "https://www.anaconda.com"
    url = "https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh"

    maintainers("ajkotobi")

    if platform.machine() == "ppc64le":
        version(
            "2023.09-0",
            sha256="5ea1ed9808af95eb2655fe6a4ffdb66bea66ecd1d053fc2ee69eacc7685ef665",
            expand=False,
        )
    elif platform.machine() == "aarch64":
        version(
            "2023.09-0",
            sha256="69ee26361c1ec974199bce5c0369e3e9a71541de7979d2b9cfa4af556d1ae0ea",
            expand=False,
        )
    elif platform.machine() == "x86_64":
        version(
            "2023.09-0",
            sha256="6c8a4abb36fbb711dc055b7049a23bbfd61d356de9468b41c5140f8a11abd851",
            expand=False,
        )
        version(
            "2023.07-2",
            sha256="589fb34fe73bc303379abbceba50f3131254e85ce4e7cd819ba4276ba29cad16",
            expand=False,
        )
        version(
            "2022.10",
            sha256="e7ecbccbc197ebd7e1f211c59df2e37bc6959d081f2235d387e08c9026666acd",
            expand=False,
        )
        version(
            "2022.05",
            sha256="a7c0afe862f6ea19a596801fc138bde0463abcbce1b753e8d5c474b506a2db2d",
            expand=False,
        )
        version(
            "2021.11",
            sha256="fedf9e340039557f7b5e8a8a86affa9d299f5e9820144bd7b92ae9f7ee08ac60",
            expand=False,
        )

        version(
            "2021.05",
            sha256="2751ab3d678ff0277ae80f9e8a74f218cfc70fe9a9cdc7bb1c137d7e47e33d53",
            expand=False,
        )
        version(
            "2020.11",
            sha256="cf2ff493f11eaad5d09ce2b4feaa5ea90db5174303d5b3fe030e16d29aeef7de",
            expand=False,
        )
        version(
            "2020.07",
            sha256="38ce717758b95b3bd0b1797cc6ccfb76f29a90c25bdfa50ee45f11e583edfdbf",
            expand=False,
        )
        version(
            "2020.02",
            sha256="2b9f088b2022edb474915d9f69a803d6449d5fdb4c303041f60ac4aefcc208bb",
            expand=False,
        )
        version(
            "2019.10",
            sha256="46d762284d252e51cd58a8ca6c8adc9da2eadc82c342927b2f66ed011d1d8b53",
            expand=False,
        )
        version(
            "2019.07",
            sha256="69581cf739365ec7fb95608eef694ba959d7d33b36eb961953f2b82cb25bdf5a",
            expand=False,
        )
        version(
            "2019.03",
            sha256="45c851b7497cc14d5ca060064394569f724b67d9b5f98a926ed49b834a6bb73a",
            expand=False,
        )
        version(
            "2018.12",
            sha256="1019d0857e5865f8a6861eaf15bfe535b87e92b72ce4f531000dc672be7fce00",
            expand=False,
        )
        version(
            "5.3.1",
            sha256="d4c4256a8f46173b675dd6a62d12f566ed3487f932bab6bb7058f06c124bcc27",
            expand=False,
        )
        version(
            "5.3.0",
            sha256="cfbf5fe70dd1b797ec677e63c61f8efc92dad930fd1c94d60390bb07fdc09959",
            expand=False,
        )
        version(
            "5.2.0",
            sha256="09f53738b0cd3bb96f5b1bac488e5528df9906be2480fe61df40e0e0d19e3d48",
            expand=False,
        )
        version(
            "5.1.0",
            sha256="7e6785caad25e33930bc03fac4994a434a21bc8401817b7efa28f53619fa9c29",
            expand=False,
        )
        version(
            "5.0.1",
            sha256="55e4db1919f49c92d5abbf27a4be5986ae157f074bf9f8238963cd4582a4068a",
            expand=False,
        )
        version(
            "5.0.0.1",
            sha256="092c92427f44687d789a41922ce8426fbdc3c529cc9d6d4ee6de5b62954b93b2",
            expand=False,
        )
        version(
            "5.0.0",
            sha256="67f5c20232a3e493ea3f19a8e273e0618ab678fa14b03b59b1783613062143e9",
            expand=False,
        )
        version(
            "4.4.0",
            sha256="3301b37e402f3ff3df216fe0458f1e6a4ccbb7e67b4d626eae9651de5ea3ab63",
            expand=False,
        )
        version(
            "4.3.1",
            sha256="4447b93d2c779201e5fb50cfc45de0ec96c3804e7ad0fe201ab6b99f73e90302",
            expand=False,
        )
        version(
            "4.3.0",
            sha256="e9169c3a5029aa820393ac92704eb9ee0701778a085ca7bdc3c57b388ac1beb6",
            expand=False,
        )
        version(
            "4.2.0",
            sha256="73b51715a12b6382dd4df3dd1905b531bd6792d4aa7273b2377a0436d45f0e78",
            expand=False,
        )
        version(
            "4.1.1",
            sha256="4f5c95feb0e7efeadd3d348dcef117d7787c799f24b0429e45017008f3534e55",
            expand=False,
        )
        version(
            "4.1.0",
            sha256="11d32cf4026603d3b327dc4299863be6b815905ff51a80329085e1bb9f96c8bd",
            expand=False,
        )
        version(
            "4.0.0",
            sha256="36a558a1109868661a5735f5f32607643f6dc05cf581fefb1c10fb8abbe22f39",
            expand=False,
        )
        version(
            "2.5.0",
            sha256="addadcb927f15cb0b5b6e36890563d3352a8ff6a901ea753d389047d274a29a9",
            expand=False,
        )
        version(
            "2.4.1",
            sha256="0735e69199fc37135930ea2fd4fb6ad0adef215a2a7ba9fd6b0a0a4daaadb1cf",
            expand=False,
        )
        version(
            "2.4.0",
            sha256="fb4e480059e991f2fa632b5a9bcdd284c7f0677814cd719c11d524453f96a40d",
            expand=False,
        )
        version(
            "2.3.0",
            sha256="3be5410b2d9db45882c7de07c554cf4f1034becc274ec9074b23fd37a5c87a6f",
            expand=False,
        )
        version(
            "2.2.0",
            sha256="4aac68743e7706adb93f042f970373a6e7e087dbf4b02ac467c94ca4ce33d2d1",
            expand=False,
        )
        version(
            "2.1.0",
            sha256="af3225ccbe8df0ffb918939e009aa57740e35058ebf9dfcf5fec794a77556c3c",
            expand=False,
        )
        version(
            "2.0.1",
            sha256="3c3b834793e461f3316ad1d9a9178c67859a9d74aaf7bcade076f04134dd1e26",
            expand=False,
        )
        version(
            "2.0.0",
            sha256="57ce4f97e300cf94c5724f72d992e9eecef708fdaa13bc672ae9779773056540",
            expand=False,
        )

    def url_for_version(self, version):
        url = "https://repo.anaconda.com/archive/Anaconda3-{0}-Linux-{1}.sh"
        return url.format(version, platform.machine())

    def install(self, spec, prefix):
        dir, anaconda_script = split(self.stage.archive_file)
        bash = which("bash")
        bash(anaconda_script, "-b", "-f", "-p", self.prefix)

    def setup_run_environment(self, env):
        filename = self.prefix.etc.join("profile.d").join("conda.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))
