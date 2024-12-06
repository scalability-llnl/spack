# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import platform

from spack.package import *


class Hpcviewer(Package):
    """Binary distribution of hpcviewer and integrated hpctraceviewer for
    the Rice HPCToolkit (Linux x86_64, ppc64le and aarch64, and MacOSX
    x86_64 and M1/M2).

    Note: hpctoolkit databases are platform independent, so you don't
    need to install hpctoolkit to run the viewers and it's common to
    run hpcrun and hpcviewer on different machines.
    """

    homepage = "https://hpctoolkit.org"
    maintainers("mwkrentel")

    skip_version_audit = ["platform=windows"]

    darwin_sha = {
        ("2024.09", "aarch64"): "f2e5b516105fe99315950ac4cc3bce120afadeca57cfaa16d58684756950d373",
        ("2024.09", "x86_64"): "dd7a807a70c384e73d9abfe67b9e41de5dedcec2da4a36cc487bb9cd1ed6b366",
        ("2024.02", "aarch64"): "0f2bf2f89b7b9656b1b249efc8b24763f7865e8ddae5b22a3c21cc79fda49ce9",
        ("2024.02", "x86_64"): "7f61166155f326179e309aa18568b44d98a2219973a323cd4713123b5bf6fd54",
        ("2023.07", "aarch64"): "6e3146fc3c6d778a256938a3589818ad3ac6496415f9fe27a012b6c1e7fbe766",
        ("2023.07", "x86_64"): "0711a71d44e0323ec4a274983e63f07d13d09a41ead08427d273808326565cc9",
        ("2023.05", "aarch64"): "b34e1ebc021e91c7260cc91a888e966a81913691de04c5e972da613d0dc34294",
        ("2023.05", "x86_64"): "689c2c18f70d53a8e1f27527f65d30c61b6f70db98f63378a97f236926ef1ac5",
        ("2023.04", "aarch64"): "85fc1c8823e2ef442666d60e98674a55315771e57205a0d2cef739d39fea699f",
        ("2023.04", "x86_64"): "6a2497d52414ca131089a4819006e5bfe1d4b35e28bf66874105bfe051d658d4",
        ("2023.02", "aarch64"): "05356fcd0a84f70b07f556b55a02954aae05419d9fa12f0f64f8e2399566e622",
        ("2023.02", "x86_64"): "90fc0ac7dfbe4c29b1a3516d125b18ea368421789f16ba6cd34cf9ad1b5b7d0b",
        ("2023.01", "aarch64"): "97af564945799652cf3efc46146297ebc0f7ebe44258876a6995cbdb5b469990",
        ("2023.01", "x86_64"): "8efbb7234f86bfc8eedfd8c3b73f148eab298d63d988f95a87b75f91d35bba8b",
        ("2022.10", "aarch64"): "4c5b4d94d5d2d82c4e583cf2229ccfde7c74741416fdb31c94cfd13c8e940b12",
        ("2022.10", "x86_64"): "5e7c419ee5cf5527c24f075aae1eeb246a2e54f253b140c816dccae02fc0b871",
        ("2022.06", "aarch64"): "7536abac5159a5bdb3c662d90be94f813c91ee0ecd6646e2c52b49d37b9ac637",
        ("2022.06", "x86_64"): "bac852e97577a696d1d07f66340e60b9079b76372d3718c543055e76acf78a38",
        ("2022.03", "aarch64"): "622ea1e589de72039d31f6ee1d09de3b0dae4b8c9f14e419e4746cf13bb5d69c",
        ("2022.03", "x86_64"): "d8d1ea959f35fced7b624996d712e8e31965fea533092d104c388f750e80909b",
        ("2022.01", "x86_64"): "75ea439af63ba3824fb270e474902246a0713d7f5914a96c1d70db13618dcf60",
        ("2021.10", "x86_64"): "0b71f2d63d99eb00fbaf9c03cf8632c198627c80e4372eeec5f20864509cbbe8",
        ("2021.05", "x86_64"): "4643567b41dddbbf9272cb56b0720f4eddfb144ca05aaad7d08c878ffaf8f2fa",
    }

    viewer_sha = {
        ("2024.09", "aarch64"): "22f2fd477652a252375554270f82068691462e93d1fea4b7c1620e26ca0c9148",
        ("2024.09", "ppc64le"): "eabfa180fc023b9d0d3db06763ec5bb9abc278d65a9763cd26d214605d1b8dd4",
        ("2024.09", "x86_64"): "4b3acd19f96ffd387e5aca7a51fcaad4919449223ce77332c91d616660c2850a",
        ("2024.02", "aarch64"): "b64166060ee0d2165fdb885ca7a0658c0d7656b2fcf3e5fc735127f3e577ed7b",
        ("2024.02", "ppc64le"): "83ea588d547c4a8bc13db0ed5c763770e7b40b44b0318b75b54ccd226410aa0d",
        ("2024.02", "x86_64"): "fa4d769ef93c666f2702d0cbc4bb49bd5f48c0c15a0eb4cbad6105807bcd57b0",
        ("2023.07", "aarch64"): "641c151ed0bc5d85db40187eb39ba4bcb7a4fdeeb07d5b4d00ed6a6d457f59b4",
        ("2023.07", "ppc64le"): "e76558377b5e64d8a07f6232468c8098d5aba32c2a6210c58bef26acd3ce8c9b",
        ("2023.07", "x86_64"): "06db75b1aab80f1142058716ca295bb43956a2b315bd7f385ec4c3a74ade0cbb",
        ("2023.05", "aarch64"): "901b58b73890180b1cb7572d91c1b6cc205a5d3d50927c50d05d2b05554918c6",
        ("2023.05", "ppc64le"): "d948e4777aea3a0c06300aedd4ce04e28f97b3ac306f78d672a5f692152bbdef",
        ("2023.05", "x86_64"): "8c51df8b958ec600c9b7547461d7e9abb0e07a048d4031f58efd47df7ec79091",
        ("2023.04", "aarch64"): "826c6a83c88eda980f9106843863853804a74f117ef53bfdd0973429c121949a",
        ("2023.04", "ppc64le"): "4804ea59101d0301e9a2284b77757919ffc114330becc071bb69d3fc5f5df261",
        ("2023.04", "x86_64"): "24aad913a156996cd372439a4b2ae8a6d90aab0e2f5281f1fa81b5be9c9b9278",
        ("2023.02", "aarch64"): "f0fbf4bf1fce05cd19ddbeed0a4e8f44a83958c796e28709591926daa28cc6ba",
        ("2023.02", "ppc64le"): "a77c1e1de5b2f71cdf2bf2daaa8298278422121d9c7fbc7008a259010d552c7d",
        ("2023.02", "x86_64"): "dbd2bcdd20a616fe9f796ad36385809078539d84336e6d955b094e6755bc969f",
        ("2023.01", "aarch64"): "686ca752c3b1c362108ead984862170f4a48c70afd437210f367f2c1a35ad5e5",
        ("2023.01", "ppc64le"): "95980b48a783cd8c9a2b961525bad6d0ab576f70e035cf17a2c6b9cd553955d8",
        ("2023.01", "x86_64"): "3c4686d64c2e27c05a8e4012e4f24f86602e353263aab5bf5930a85d53919841",
        ("2022.10", "aarch64"): "b6ab0d16168e67ba5de3fb0b989cba7b8a683aa5210d4ed69b5c8581ab990ea8",
        ("2022.10", "ppc64le"): "72abc3ee923a4aae6fe75a5269210b2e92ada2c392eab70480f9950e5be18bd0",
        ("2022.10", "x86_64"): "444e101da54b0cc79769b91ef5119d38864e15e0166575af28f3bb75d7f905ea",
        ("2022.06", "aarch64"): "2714d44be798a63bc65e36b6bd35e690a3fcd79398b1b8ddcb447cd620b64e84",
        ("2022.06", "ppc64le"): "09867257c90371cf908347cf0ee3eddb381f8481625a6a80307f7de78467ada6",
        ("2022.06", "x86_64"): "a0ef849f5c46054b4db3c9bdeb9a1812af2355749d5a3966a473b8f04a8765e9",
        ("2022.03", "aarch64"): "8acbc7c5a3504a42f6014c2b252c474499a227815110afa811d38817df6925a3",
        ("2022.03", "ppc64le"): "660b642288940fa70c2fa642d17239caee62b6ebef500793c9d4509fdf574e19",
        ("2022.03", "x86_64"): "25297c18c6f9a3279a44125bd23d782131dc33d6d274c4367b67cc32140fd4e1",
        ("2022.01", "aarch64"): "4709d9511ad0b3fb22ea914053e36bb746f088e2a756e0f790be8a6908d1c16a",
        ("2022.01", "ppc64le"): "8403e3134a31a97ca71ce9f14d2b973b303b3c3c116d57c05e5b2792f7b59966",
        ("2022.01", "x86_64"): "a8e3090d8029afa5f853aa047d1a9bd792679c83b60374daeafdd45209d4e182",
        ("2021.10", "aarch64"): "c696a0ecc6696f9979de3940b5471a3d99c8d573736cabb24b86255d860a23dc",
        ("2021.10", "ppc64le"): "f0eda3510b71fd9115c5653efba29aaefcb335c66b118cf63f36e1353c39e24e",
        ("2021.10", "x86_64"): "d5a444e28d6c9d1a087c39bd3ffe55c6f982dc37a7a743b83bbba2fbfc7ca7c6",
        ("2021.05", "aarch64"): "a500bf14be14ca9b08a8382f1d122f59b45690b6a567df0932fc2cabd6382a9a",
        ("2021.05", "ppc64le"): "d39f9f6556abcd5a184db242711b72b2e8571d0b78bb08d0e497fd4e6dbe87a1",
        ("2021.05", "x86_64"): "f316c1fd0b134c96392cd4eb5e5aa2bffa36bd449f401d8fe950ab4f761c34ab",
        ("2021.03", "aarch64"): "1b1f7f51a319a159aa96dee21b2cd77ee23b01df263ea122980fa1567e4dab8d",
        ("2021.03", "ppc64le"): "8fc4683a9e61263ac78fe35391930b0cdc8e84dd50f8d41dcd0c6d8072b02937",
        ("2021.03", "x86_64"): "40b4453fe662b896a853d869486b481ded0d29abdf5e50aab2d8f3bdf8940b04",
        ("2021.01", "aarch64"): "fe797a1c97943f7509c36a570198291e674cd4a793c1d6538a2761d66542dc52",
        ("2021.01", "ppc64le"): "ba4035de2ae208280c3744000ea08d2d7f8c31bd7095f722e442ddc289648063",
        ("2021.01", "x86_64"): "99eba4e1c613203c4658f2874d0e79e1620db7a22ac7dcb810801886ba9f8a79",
        ("2020.12", "ppc64le"): "ce0d741aa8849621c03183dbf11a0dc1f6d296e3de80e25976a7f2a2750899c4",
        ("2020.12", "x86_64"): "29c5e1427893f0652e863fd6d54a8585077662597e5073532ec9f3b116626498",
        ("2020.07", "x86_64"): "19951662626c7c9817c4a75269c85810352dc48ae9a62dfb6ce4a5b502de2118",
        ("2020.07", "ppc64"): "3f5d9358ef8ff9ba4f6dcaa4d7132f41ba55f0c132d9fd1e2f6da18341648a4e",
        ("2020.07", "ppc64le"): "e236a8578dc247279d1021aa35bac47e2d4864b906efcef76c0610ee0086b353",
        ("2020.05", "x86_64"): "27f99c94a69abd005303fb58360b0d1b3eb7d223cab81c38ae6ccdd83ec15106",
        ("2020.05", "ppc64"): "469bce07a75476c132d3791ca49e38db015917c9c36b4810e477bc1c54a13d68",
        ("2020.05", "ppc64le"): "fc4491bf6d9eaf2b7f2d39b722c978597a881ece557fb05a4cf27caabb9e0b99",
        ("2020.04", "x86_64"): "5944c7b1e518b25d143df72b06a69cffb0bfc92186eb5efee2178fc2814a0b8b",
        ("2020.04", "ppc64"): "ba60615a550aa77a17eb94272b62365a22298cebc6dc2cb7463686741e58d874",
        ("2020.04", "ppc64le"): "128494077979b447875ed730f1e8c5470fafcd52ae6debe61625031248d91f7c",
        ("2020.02", "x86_64"): "af1f514547a9325aee30eb891b31e38c7ea3f33d2d1978b44f83e7daa3d5de6b",
        ("2020.02", "ppc64"): "7bb4926202db663aedd5a6830778c5f73f6b08a65d56861824ea95ba83b1f59c",
        ("2020.02", "ppc64le"): "cfcebb7ba301affd6d21d2afd43c540e6dd4c5bc39b0d20e8bd1e4fed6aa3481",
    }

    trace_sha = {
        ("2020.07", "x86_64"): "52aea55b1d40b9453c106ac5a83020a08839b9be1e71dbd1a9f471e5f3a55d43",
        ("2020.07", "ppc64"): "3d9222310a18618704015aecbcab7f7c5a2cedbd5ecd8ace1bfc7e98d11b8d36",
        ("2020.07", "ppc64le"): "2f0a8b95033a5816d468b87c8c139f08a307714e2e27a1cb4a35e1c5a8083cca",
        ("2020.05", "x86_64"): "a0b925099a00c10fcb38e937068e50937175fd46dc086121525e546a63a7fd83",
        ("2020.05", "ppc64"): "40526f62f36e5b6438021c2b557256638d41a6b8f4e101534b5230ac644a9b85",
        ("2020.05", "ppc64le"): "c16e83b59362adcebecd4231374916a2b3a3c016f75a45b24e8398f777a24f89",
        ("2020.04", "x86_64"): "695f7a06479c2b6958a6ebc3985b7ed777e7e126c04424ce980b224690f769f3",
        ("2020.04", "ppc64"): "78cfadaf7bc6130cc4257241499b36f4f1c47f22d0daa29f5e733ca824a87b3c",
        ("2020.04", "ppc64le"): "28c225023accbc85a19c6d8fdcc14dae64a475ed5de2b94f18e58aab4edd2c09",
        ("2020.02", "x86_64"): "b7b634e91108aa50a2e8647ac6bac87df775ae38aff078545efaa84735e0a666",
        ("2020.02", "ppc64"): "a3e845901689e1b32bc6ab2826c6ac6ed352df4839090fa530b20f747e6e0957",
        ("2020.02", "ppc64le"): "a64a283f61e706d988952a7cede9fac0328b09d2d0b64e4c08acc54e38781c98",
    }

    system = platform.system().lower()
    machine = platform.machine().lower()
    if machine == "arm64":
        machine = "aarch64"

    # Versions for MacOSX / Darwin
    if system == "darwin":
        for (ver, arch), sha in darwin_sha.items():
            if arch == machine:
                version(
                    ver,
                    url=f"https://gitlab.com/hpctoolkit/hpcviewer/-/releases/{ver}/downloads/hpcviewer-macosx.cocoa.{arch}.zip",
                    sha256=sha,
                    # Versions before 2022.01 are dead links
                    deprecated=(ver < "2022.01"),
                )

    # Versions for Linux and Cray front-end
    if system == "linux":
        for (ver, arch), sha in viewer_sha.items():
            if arch == machine:
                version(
                    ver,
                    url=f"https://gitlab.com/hpctoolkit/hpcviewer/-/releases/{ver}/downloads/hpcviewer-linux.gtk.{arch}.tgz",
                    sha256=sha,
                    # Versions before 2022.01 are dead links
                    deprecated=(ver < "2022.01"),
                )

                # Current versions include the viewer and trace viewer in
                # one tar file.  Before 2020.07, the trace viewer was a
                # separate tar file (resource).
                if (ver, arch) in trace_sha:
                    resource(
                        name="hpctraceviewer",
                        url=f"https://gitlab.com/hpctoolkit/hpcviewer/-/releases/{ver}/downloads/hpctraceviewer-linux.gtk.{arch}.tgz",
                        sha256=trace_sha[ver, arch],
                        placement="TRACE",
                        when=f"@{ver}",
                    )

    depends_on("java@17:", type=("build", "run"), when="@2024.09:")
    depends_on("java@11:", type=("build", "run"), when="@2021.0:2024.02")
    depends_on("java@8", type=("build", "run"), when="@:2020")

    # Install for MacOSX / Darwin
    @when("platform=darwin")
    def install(self, spec, prefix):
        # Add path to java binary to hpcviewer.ini file.
        ini_file = join_path("Contents", "Eclipse", "hpcviewer.ini")
        java_binary = join_path(spec["java"].prefix.bin, "java")
        filter_file("(-startup)", "-vm\n" + java_binary + "\n" + r"\1", ini_file, backup=False)

        # Copy files into prefix/hpcviewer.app.
        app_dir = join_path(prefix, "hpcviewer.app")
        mkdirp(app_dir)
        install_tree(".", app_dir)

        # Add launch script to call 'open' on app directory.
        mkdirp(prefix.bin)
        viewer_file = join_path(prefix.bin, "hpcviewer")
        with open(viewer_file, "w") as file:
            file.write("#!/bin/sh\n")
            file.write("open " + app_dir + "\n")
        os.chmod(viewer_file, 0o755)

    @when("platform=linux")
    def install(self, spec, prefix):
        self.linux_install(spec, prefix)

    # Both hpcviewer and trace viewer have an install script.
    def linux_install(self, spec, prefix):
        args = ["--java", spec["java"].home, prefix]

        # Sometimes the script is install.sh, sometimes install.
        inst_path = join_path(".", "install.sh")
        if not os.path.exists(inst_path):
            inst_path = join_path(".", "install")

        inst = Executable(inst_path)
        inst(*args)

        # Older versions used a separate resource for the traceviewer.
        if os.path.isdir("TRACE"):
            cd("TRACE")
            inst = Executable(inst_path)
            inst(*args)
