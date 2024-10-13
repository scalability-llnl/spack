# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
from glob import glob

import llnl.util.tty as tty

from spack.package import *

# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()

_versions = {
    "12.6.2": {
        "Linux-aarch64": (
            "2249408848b705c18b9eadfb5161b52e4e36fcc5753647329cce93db141e5466",
            "https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda_12.6.2_560.35.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "3729a89cb58f7ca6a46719cff110d6292aec7577585a8d71340f0dbac54fb237",
            "https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda_12.6.2_560.35.03_linux.run",
        ),
    },
    "12.6.1": {
        "Linux-aarch64": (
            "b39ac88184798e8c313e6ced23dd128f13ab30c199b96bd9c0bee07dbdd31400",
            "https://developer.download.nvidia.com/compute/cuda/12.6.1/local_installers/cuda_12.6.1_560.35.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "73acce7243519625f259509f5dcff6dc8fbd23dca53b852aa9ce382009e92e9d",
            "https://developer.download.nvidia.com/compute/cuda/12.6.1/local_installers/cuda_12.6.1_560.35.03_linux.run",
        ),
    },
    "12.6.0": {
        "Linux-aarch64": (
            "398db7baca17d51ad5035c606714c96380c965fd1742478c743bc6bbb1d8f63c",
            "https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "31ab04394e69b14dd8656e2b44c2877db1a0e898dff8a7546a4c628438101b94",
            "https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux.run",
        ),
    },
    "12.5.1": {
        "Linux-aarch64": (
            "353e8abc52ca80adf05002b775c7b3a2d2feefcf1c25ae13f8757f9a11efba3e",
            "https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda_12.5.1_555.42.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "b5e0a779e089c86610051141c4cf498beef431858ec63398107391727ecbdb04",
            "https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda_12.5.1_555.42.06_linux.run",
        ),
    },
    "12.5.0": {
        "Linux-aarch64": (
            "e7b864c9ae27cef77cafc78614ec33cbb0a27606af9375deffa09c4269a07f04",
            "https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/cuda_12.5.0_555.42.02_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "90fcc7df48226434065ff12a4372136b40b9a4cbf0c8602bb763b745f22b7a99",
            "https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/cuda_12.5.0_555.42.02_linux.run",
        ),
    },
    "12.4.1": {
        "Linux-aarch64": (
            "b0fbc77effa225498974625b6b08b3f6eff4a37e379f5b60f1d3827b215ad19b",
            "https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "367d2299b3a4588ab487a6d27276ca5d9ead6e394904f18bccb9e12433b9c4fb",
            "https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run",
        ),
        "Linux-ppc64le": (
            "677f44da10dd81396cb53a32c4e26eccdc24912063cb2e3beb3bbcb1658ef451",
            "https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux_ppc64le.run",
        ),
    },
    "12.4.0": {
        "Linux-aarch64": (
            "b12bfe6c36d32ecf009a6efb0024325c5fc389fca1143f5f377ae2555936e803",
            "https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "e6a842f4eca9490575cdb68b6b1bb78d47b95a897de48dee292c431892e57d17",
            "https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux.run",
        ),
        "Linux-ppc64le": (
            "ef9a712daccf2805b4422f2301ff0eaa5c3ad41ef5d64b8626773bce7d1f41fe",
            "https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux_ppc64le.run",
        ),
    },
    "12.3.2": {
        "Linux-aarch64": (
            "761b84e292b94c4d330f445d36326dfff90a418e909fb0baf3d6f03e24106d08",
            "https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda_12.3.2_545.23.08_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "24b2afc9f770d8cf43d6fa7adc2ebfd47c4084db01bdda1ce3ce0a4d493ba65b",
            "https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda_12.3.2_545.23.08_linux.run",
        ),
        "Linux-ppc64le": (
            "b876936fc80de10653523eadd846065db346b38ba6296f2d365772259cb2f198",
            "https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda_12.3.2_545.23.08_linux_ppc64le.run",
        ),
    },
    "12.3.1": {
        "Linux-aarch64": (
            "bce6bb8b293c33c3ed0c1b65120c70587cc29e1b94ea8679ebb14c32b3858b5e",
            "https://developer.download.nvidia.com/compute/cuda/12.3.1/local_installers/cuda_12.3.1_545.23.08_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "b73d18ccd5ff85bbae32b425dfb82729612ede65b07a37cd5e2b574190614038",
            "https://developer.download.nvidia.com/compute/cuda/12.3.1/local_installers/cuda_12.3.1_545.23.08_linux.run",
        ),
        "Linux-ppc64le": (
            "9da7e6e2beadc933aab73de79a84e133ddf03226371d3d7af83502748a978568",
            "https://developer.download.nvidia.com/compute/cuda/12.3.1/local_installers/cuda_12.3.1_545.23.08_linux_ppc64le.run",
        ),
    },
    "12.3.0": {
        "Linux-aarch64": (
            "9a8fb8acf46b88faf0d711bda3149e1706efbbae02fcb40ab72addfd0e9ce5df",
            "https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda_12.3.0_545.23.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "7c13face3af64d6e1648d6e3101d31c8111e747143acb0077d973c1690820422",
            "https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda_12.3.0_545.23.06_linux.run",
        ),
        "Linux-ppc64le": (
            "de15c04380ec35b194c07503bf434837bac5b427cf77b19a63962b1653d195d5",
            "https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda_12.3.0_545.23.06_linux_ppc64le.run",
        ),
    },
    "12.2.2": {
        "Linux-aarch64": (
            "4113a15e6b27a02638c72edeb5f89de4c9ea312febba12fc4cefff2edc882268",
            "https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda_12.2.2_535.104.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "2b39aae3e7618d9f59a3c8fa1f1bc61f29c0b0e0df75fb05076badb352952ef2",
            "https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda_12.2.2_535.104.05_linux.run",
        ),
        "Linux-ppc64le": (
            "18848278e7f2bd4b4481f5665633d7e3d46e9a562d175d5ff278218188b01342",
            "https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda_12.2.2_535.104.05_linux_ppc64le.run",
        ),
    },
    "12.2.1": {
        "Linux-aarch64": (
            "a9ae6bd02684c7acfb229484368bf2691d592767ce1aed10ae9aed92c81b9f09",
            "https://developer.download.nvidia.com/compute/cuda/12.2.1/local_installers/cuda_12.2.1_535.86.10_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "c51e814eaa756160a73289b1f35880cc38c18e1ddedc87f46f7ff0d1696bdb95",
            "https://developer.download.nvidia.com/compute/cuda/12.2.1/local_installers/cuda_12.2.1_535.86.10_linux.run",
        ),
        "Linux-ppc64le": (
            "8f1aa60cc1e14fd7853eeecd53a78b7dfb2b2da0512a312cc35e4f5b79454f94",
            "https://developer.download.nvidia.com/compute/cuda/12.2.1/local_installers/cuda_12.2.1_535.86.10_linux_ppc64le.run",
        ),
    },
    "12.2.0": {
        "Linux-aarch64": (
            "9c90d79bb63952cd30f1f57f9f8fe11e7a8967bba6f824df45d3464b5d37e5d8",
            "https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "ecf3d2afadcbac029f0f4505785810d52d006e4b87ba79ff3f984336a2bbf518",
            "https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run",
        ),
        "Linux-ppc64le": (
            "f7b5fde5f727b51c380c6199200d0525e8585475944ff8ad2791d06734f54230",
            "https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux_ppc64le.run",
        ),
    },
    "12.1.1": {
        "Linux-aarch64": (
            "45ea4cd860f0a26d3db8ce032530f2ee0b55abdd587545213d395a73623b4278",
            "https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_530.30.02_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "d74022d41d80105319dfa21beea39b77a5b9919539c0487a05caaf2446d6a70e",
            "https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_530.30.02_linux.run",
        ),
        "Linux-ppc64le": (
            "c5950381f2c01fd52692372fc8e51d599e940ada2af2c82c3cc854ecff933eae",
            "https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_530.30.02_linux_ppc64le.run",
        ),
    },
    "12.1.0": {
        "Linux-aarch64": (
            "1d0dd884f5257c12471dc455dc1a4aee8d620191737c0b2e40f016d8adc9d009",
            "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_530.30.02_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "68699036c12d71adb9ad2799dce2ff070270fab4488b90920b9756ab3f52c41c",
            "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_530.30.02_linux.run",
        ),
        "Linux-ppc64le": (
            "8d75bd9da953a51062b89b8c752cffcf02b02c85cb461291d354ac2cffb2da48",
            "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_530.30.02_linux_ppc64le.run",
        ),
    },
    "12.0.1": {
        "Linux-aarch64": (
            "835270a8db419b9dbaefc1bab8fe5caf6f2caf381975c4b0d35cc0718c26074a",
            "https://developer.download.nvidia.com/compute/cuda/12.0.1/local_installers/cuda_12.0.1_525.85.12_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "1b205a06272f1463f477276fdab903f3f666917c068e520738001e69c7a1875b",
            "https://developer.download.nvidia.com/compute/cuda/12.0.1/local_installers/cuda_12.0.1_525.85.12_linux.run",
        ),
        "Linux-ppc64le": (
            "1e81040223c25fd72895a1348e32463d7d0f5a7e74b5d2ace897220cb6d4d849",
            "https://developer.download.nvidia.com/compute/cuda/12.0.1/local_installers/cuda_12.0.1_525.85.12_linux_ppc64le.run",
        ),
    },
    "12.0.0": {
        "Linux-aarch64": (
            "cd13e9c65d4c8f895a968706f46064d536be09f9706bce081cc864b7e4fa4544",
            "https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda_12.0.0_525.60.13_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "905e9b9516900839fb76064719db752439f38b8cb730b49335d8bd53ddfad392",
            "https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda_12.0.0_525.60.13_linux.run",
        ),
        "Linux-ppc64le": (
            "117fe045c71668e45d41c6119b6f27875370c78e33fc56795b6fe014c796ec60",
            "https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda_12.0.0_525.60.13_linux_ppc64le.run",
        ),
    },
    "11.8.0": {
        "Linux-aarch64": (
            "e6e9a8d31163c9776b5e313fd7590877c5684e1ecddee741154f95704d4ed27c",
            "https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "9223c4af3aebe4a7bbed9abd9b163b03a1b34b855fbc2b4a0d1b706ac09a5a16",
            "https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run",
        ),
        "Linux-ppc64le": (
            "f917fb7617033223938543ad3ae923190d99507acc08a399d752a2868e87349d",
            "https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux_ppc64le.run",
        ),
    },
    "11.7.1": {
        "Linux-aarch64": (
            "1607b98c30cb8efa52b9c8f564ec92d26ee1922cb677740aafacce313e544ecd",
            "https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "52286a29706549b7d0feeb0e7e3eca1b15287c436a69fa880ad385b1be3e04db",
            "https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux.run",
        ),
        "Linux-ppc64le": (
            "f59fc381cbd903da55bfea9f81534bd4d20e3db716c332be3d2c4804efc2ec6b",
            "https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux_ppc64le.run",
        ),
    },
    "11.7.0": {
        "Linux-aarch64": (
            "e777839a618ca9a3d5ad42ded43a1b6392af2321a7327635a4afcc986876a21b",
            "https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "087fdfcbba1f79543b1f78e43a8dfdac5f6db242d042dde820e16dc185892f26",
            "https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux.run",
        ),
        "Linux-ppc64le": (
            "74a507ac54067c258e6b7c9063c98d411116ecc5c5397b1f6e6a999e86dff08a",
            "https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux_ppc64le.run",
        ),
    },
    "11.6.2": {
        "Linux-aarch64": (
            "b20c014c6bba36b13c50da167ad42e9bd1cea24f3b6297b495ea129c0889f36e",
            "https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "99b7a73dcc52a52cef4c1fceb4a60c3015ac9b6404082c1677d9efdaba1d4593",
            "https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux.run",
        ),
        "Linux-ppc64le": (
            "869232ff8dbf295a71609738ac9e1b0079ca75597b427f1c026f42b36896afe8",
            "https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux_ppc64le.run",
        ),
    },
    "11.6.1": {
        "Linux-aarch64": (
            "80586b003d58030004d465f5331dc69ee26c95a29516fb2488ff10f034139cb2",
            "https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "ab219afce00b74200113269866fbff75ead037bcfc23551a8338c2684c984d7e",
            "https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux.run",
        ),
        "Linux-ppc64le": (
            "ef762efbc00b67d572823c6ec338cc2c0cf0c096f41e6bce18e8d4501f260956",
            "https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux_ppc64le.run",
        ),
    },
    "11.6.0": {
        "Linux-aarch64": (
            "5898579f5e59b708520883cb161089f5e4f3426158d1e9f973c49d224085d1d2",
            "https://developer.download.nvidia.com/compute/cuda/11.6.0/local_installers/cuda_11.6.0_510.39.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "1783da6d63970786040980b57fa3cb6420142159fc7d0e66f8f05c4905d98c83",
            "https://developer.download.nvidia.com/compute/cuda/11.6.0/local_installers/cuda_11.6.0_510.39.01_linux.run",
        ),
        "Linux-ppc64le": (
            "c86b866a42baf59ddc6f1f4a79e6d77213c90749e77e574f0e0d796a749ab7d0",
            "https://developer.download.nvidia.com/compute/cuda/11.6.0/local_installers/cuda_11.6.0_510.39.01_linux_ppc64le.run",
        ),
    },
    "11.5.2": {
        "Linux-aarch64": (
            "31337c8bdc224fa1bd07bc4b6a745798392428118cc8ea0fa4446ee4ad47dd30",
            "https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "74959abf02bcba526f0a3aae322c7641b25da040ccd6236d07038f81997b73a6",
            "https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux.run",
        ),
        "Linux-ppc64le": (
            "45c468f430436b3e95d5e485a6ba0ec1fa2b23dc6c551c1307b79996ecf0a7ed",
            "https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux_ppc64le.run",
        ),
    },
    "11.5.1": {
        "Linux-aarch64": (
            "73e1d0e97c7fa686efe7e00fb1e5f179372c4eec8e14d4f44ab58d5f6cf57f63",
            "https://developer.download.nvidia.com/compute/cuda/11.5.1/local_installers/cuda_11.5.1_495.29.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "60bea2fc0fac95574015f865355afbf599422ec2c85554f5f052b292711a4bca",
            "https://developer.download.nvidia.com/compute/cuda/11.5.1/local_installers/cuda_11.5.1_495.29.05_linux.run",
        ),
        "Linux-ppc64le": (
            "9e0e494d945634fe8ad3e12d7b91806aa4220ed27487bb211030d651b27c67a9",
            "https://developer.download.nvidia.com/compute/cuda/11.5.1/local_installers/cuda_11.5.1_495.29.05_linux_ppc64le.run",
        ),
    },
    "11.5.0": {
        "Linux-aarch64": (
            "6ea9d520cc956cc751a5ac54f4acc39109627f4e614dd0b1a82cc86f2aa7d8c4",
            "https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda_11.5.0_495.29.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "ae0a1693d9497cf3d81e6948943e3794636900db71c98d58eefdacaf7f1a1e4c",
            "https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda_11.5.0_495.29.05_linux.run",
        ),
        "Linux-ppc64le": (
            "95baefdc5adf165189407b119861ffb2e9800fd94d7fc81d10fb81ed36dc12db",
            "https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda_11.5.0_495.29.05_linux_ppc64le.run",
        ),
    },
    "11.4.4": {
        "Linux-aarch64": (
            "c5c08531e48e8fdc2704fa1c1f7195f2c7edd2ee10a466d0e24d05b77d109435",
            "https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "44545a7abb4b66dfc201dcad787b5e8352e5b7ddf3e3cc5b2e9177af419c25c8",
            "https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux.run",
        ),
        "Linux-ppc64le": (
            "c71cd4e6c05fde11c0485369a73e7f356080e7a18f0e3ad7244e8fc03a9dd3e2",
            "https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux_ppc64le.run",
        ),
    },
    "11.4.3": {
        "Linux-aarch64": (
            "e02db34a487ea3de3eec9db80efd09f12eb69d55aca686cecaeae96a9747b1d4",
            "https://developer.download.nvidia.com/compute/cuda/11.4.3/local_installers/cuda_11.4.3_470.82.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "749183821ffc051e123f12ebdeb171b263d55b86f0dd7c8f23611db1802d6c37",
            "https://developer.download.nvidia.com/compute/cuda/11.4.3/local_installers/cuda_11.4.3_470.82.01_linux.run",
        ),
        "Linux-ppc64le": (
            "08f29cc3ed0b3b82dd9b007186237be2352bb552f99230c450a25e768f5754ee",
            "https://developer.download.nvidia.com/compute/cuda/11.4.3/local_installers/cuda_11.4.3_470.82.01_linux_ppc64le.run",
        ),
    },
    "11.4.2": {
        "Linux-aarch64": (
            "f2c4a52e06329606c8dfb7c5ea3f4cb4c0b28f9d3fdffeeb734fcc98daf580d8",
            "https://developer.download.nvidia.com/compute/cuda/11.4.2/local_installers/cuda_11.4.2_470.57.02_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "bbd87ca0e913f837454a796367473513cddef555082e4d86ed9a38659cc81f0a",
            "https://developer.download.nvidia.com/compute/cuda/11.4.2/local_installers/cuda_11.4.2_470.57.02_linux.run",
        ),
        "Linux-ppc64le": (
            "a917c2e53dc13fdda7def71fd40920bf3809d5a2caa3e9acfe377fb9fb22f12d",
            "https://developer.download.nvidia.com/compute/cuda/11.4.2/local_installers/cuda_11.4.2_470.57.02_linux_ppc64le.run",
        ),
    },
    "11.4.1": {
        "Linux-aarch64": (
            "8efa725a41dfd3c0c0f453c2dd535d149154102bf2b791718859417b4f84f922",
            "https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "dd6c339a719989d2518f5d54eeac1ed707d0673f8664ba0c4d4b2af7c3ba0005",
            "https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux.run",
        ),
        "Linux-ppc64le": (
            "dd92ca04f76ad938da3480e2901c0e52dbff6028ada63c09071ed9e3055dc361",
            "https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux_ppc64le.run",
        ),
    },
    "11.4.0": {
        "Linux-aarch64": (
            "f0c8e80d98a601ddca031b6764459984366008c7d3847e7c7f99b36bd4438e3c",
            "https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda_11.4.0_470.42.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "d219db30f7415a115a4ea22bdbb5984b0a18f7f891cad6074c5da45d223aaa4b",
            "https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda_11.4.0_470.42.01_linux.run",
        ),
        "Linux-ppc64le": (
            "6eb2fd0d9d5bc39fb243b5e1789ff827f325d098cd1fbb828a0499552b9544cc",
            "https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda_11.4.0_470.42.01_linux_ppc64le.run",
        ),
    },
    "11.3.1": {
        "Linux-aarch64": (
            "39990d3da88b21289ac20850bc183f0b66275f32e1f562b551c05843bf506e4c",
            "https://developer.download.nvidia.com/compute/cuda/11.3.1/local_installers/cuda_11.3.1_465.19.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "ad93ea98efced35855c58d3a0fc326377c60917cb3e8c017d3e6d88819bf2934",
            "https://developer.download.nvidia.com/compute/cuda/11.3.1/local_installers/cuda_11.3.1_465.19.01_linux.run",
        ),
        "Linux-ppc64le": (
            "220f2c10a21500d62b03c6848c1659ebb3a8e10dc0915ab87b86b397058407c5",
            "https://developer.download.nvidia.com/compute/cuda/11.3.1/local_installers/cuda_11.3.1_465.19.01_linux_ppc64le.run",
        ),
    },
    "11.3.0": {
        "Linux-aarch64": (
            "f7b284cf055fcf18be9a9aa216e3c7968d3e011446eb0c7200a3353c223ce718",
            "https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "262da7f77db177b153a6b70b5812210f3f72f00eb608ab9cf2a4582328c4bf5c",
            "https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux.run",
        ),
        "Linux-ppc64le": (
            "c0010107933b575a87e27b1293e5dc32b74201486f4ae2f4c8695ea727d22857",
            "https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux_ppc64le.run",
        ),
    },
    "11.2.2": {
        "Linux-aarch64": (
            "2f915ad631331eebdafaabd971723a60290ae8bb090d771075b9e6a0b28cbae6",
            "https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "0a2e477224af7f6003b49edfd2bfee07667a8148fe3627cfd2765f6ad72fa19d",
            "https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux.run",
        ),
        "Linux-ppc64le": (
            "2304ec235fe5d1f8bf75f00dc2c2d11473759dc23428dbbd5fb5040bc8c757e3",
            "https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux_ppc64le.run",
        ),
    },
    "11.2.1": {
        "Linux-aarch64": (
            "4b322fa6477d1a2cd2f2f526fa520c0f90bef2c264ef8435cb016bebb5456c5e",
            "https://developer.download.nvidia.com/compute/cuda/11.2.1/local_installers/cuda_11.2.1_460.32.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "1da98cb897cc5f58a7445a4a66ca4f6926867706cb3af58a669cdcd8dc3d17c8",
            "https://developer.download.nvidia.com/compute/cuda/11.2.1/local_installers/cuda_11.2.1_460.32.03_linux.run",
        ),
        "Linux-ppc64le": (
            "b3e8b6cd76872deb3acd050d32e197bc1c655e142b169070f0f9753680461a3f",
            "https://developer.download.nvidia.com/compute/cuda/11.2.1/local_installers/cuda_11.2.1_460.32.03_linux_ppc64le.run",
        ),
    },
    "11.2.0": {
        "Linux-aarch64": (
            "c11dc274660e9b47b0f25ca66861a7406246a7191f1b04d0710515fcac0fa6cd",
            "https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda_11.2.0_460.27.04_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "9c50283241ac325d3085289ed9b9c170531369de41165ce271352d4a898cbdce",
            "https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda_11.2.0_460.27.04_linux.run",
        ),
        "Linux-ppc64le": (
            "adc3267df5dbfdaf51cb4c9b227ba6bfd979a39d9b4136bba0eba6b1dd2a2731",
            "https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda_11.2.0_460.27.04_linux_ppc64le.run",
        ),
    },
    "11.1.1": {
        "Linux-aarch64": (
            "9ab1dbafba205c06bea8c88e38cdadb3038af19cb56e7b3ba734d3d7a84b8f02",
            "https://developer.download.nvidia.com/compute/cuda/11.1.1/local_installers/cuda_11.1.1_455.32.00_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "3eae6727086024925ebbcef3e9a45ad379d8490768fd00f9c2d8b6fd9cd8dd8f",
            "https://developer.download.nvidia.com/compute/cuda/11.1.1/local_installers/cuda_11.1.1_455.32.00_linux.run",
        ),
        "Linux-ppc64le": (
            "023e571fe26ee829c98138dfc305a92279854aac7d184d255fd58c06c6af3c17",
            "https://developer.download.nvidia.com/compute/cuda/11.1.1/local_installers/cuda_11.1.1_455.32.00_linux_ppc64le.run",
        ),
    },
    "11.1.0": {
        "Linux-aarch64": (
            "878cbd36c5897468ef28f02da50b2f546af0434a8a89d1c724a4d2013d6aa993",
            "https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "858cbab091fde94556a249b9580fadff55a46eafbcb4d4a741d2dcd358ab94a5",
            "https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux.run",
        ),
        "Linux-ppc64le": (
            "a561e6f7f659bc4100e4713523b0b8aad6b36aa77fac847f6423e7780c750064",
            "https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux_ppc64le.run",
        ),
    },
    "11.0.3": {
        "Linux-aarch64": (
            "1e24f61f79c1043aa3d1d126ff6158daa03a62a51b5195a2ed5fbe75c3b718f3",
            "https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "b079c4e408adf88c3f1ffb8418a97dc4227c37935676b4bf4ca0beec6c328cc0",
            "https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux.run",
        ),
        "Linux-ppc64le": (
            "4775b21df004b1433bafff9b48a324075c008509f4c0fe28cd060d042d2e0794",
            "https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux_ppc64le.run",
        ),
    },
    "11.0.2": {
        "Linux-aarch64": (
            "23851e30f7c47a1baad92891abde0adbc783de5962c7480b9725198ceacda4a0",
            "https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "48247ada0e3f106051029ae8f70fbd0c238040f58b0880e55026374a959a69c1",
            "https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux.run",
        ),
        "Linux-ppc64le": (
            "db06d0f3fbf6f7aa1f106fc921ad1c86162210a26e8cb65b171c5240a3bf75da",
            "https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux_ppc64le.run",
        ),
    },
    "10.2.89": {
        "Linux-x86_64": (
            "560d07fdcf4a46717f2242948cd4f92c5f9b6fc7eae10dd996614da913d5ca11",
            "https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux.run",
        ),
        "Linux-ppc64le": (
            "5227774fcb8b10bd2d8714f0a716a75d7a2df240a9f2a49beb76710b1c0fc619",
            "https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux_ppc64le.run",
        ),
    },
    "10.1.243": {
        "Linux-x86_64": (
            "e7c22dc21278eb1b82f34a60ad7640b41ad3943d929bebda3008b72536855d31",
            "https://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux.run",
        ),
        "Linux-ppc64le": (
            "b198002eef010bab9e745ae98e47567c955d00cf34cc8f8d2f0a6feb810523bf",
            "https://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux_ppc64le.run",
        ),
    },
    "10.0.130": {
        "Linux-x86_64": (
            "92351f0e4346694d0fcb4ea1539856c9eb82060c25654463bfd8574ec35ee39a",
            "https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux",
        )
    },
    "9.2.88": {
        "Linux-x86_64": (
            "8d02cc2a82f35b456d447df463148ac4cc823891be8820948109ad6186f2667c",
            "https://developer.nvidia.com/compute/cuda/9.2/Prod/local_installers/cuda_9.2.88_396.26_linux",
        )
    },
    "9.1.85": {
        "Linux-x86_64": (
            "8496c72b16fee61889f9281449b5d633d0b358b46579175c275d85c9205fe953",
            "https://developer.nvidia.com/compute/cuda/9.1/Prod/local_installers/cuda_9.1.85_387.26_linux",
        )
    },
    "9.0.176": {
        "Linux-x86_64": (
            "96863423feaa50b5c1c5e1b9ec537ef7ba77576a3986652351ae43e66bcd080c",
            "https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run",
        )
    },
    "8.0.61": {
        "Linux-x86_64": (
            "9ceca9c2397f841024e03410bfd6eabfd72b384256fbed1c1e4834b5b0ce9dc4",
            "https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run",
        )
    },
    "8.0.44": {
        "Linux-x86_64": (
            "64dc4ab867261a0d690735c46d7cc9fc60d989da0d69dc04d1714e409cacbdf0",
            "https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_8.0.44_linux-run",
        )
    },
    "7.5.18": {
        "Linux-x86_64": (
            "08411d536741075131a1858a68615b8b73c51988e616e83b835e4632eea75eec",
            "https://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run",
        )
    },
    "6.5.14": {
        "Linux-x86_64": (
            "f3e527f34f317314fe8fcd8c85f10560729069298c0f73105ba89225db69da48",
            "https://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run",
        )
    },
    "6.0.37": {
        "Linux-x86_64": (
            "991e436c7a6c94ec67cf44204d136adfef87baa3ded270544fa211179779bc40",
            "https://developer.download.nvidia.com/compute/cuda/6_0/rel/installers/cuda_6.0.37_linux_64.run",
        )
    },
}


class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented
    by NVIDIA. It enables dramatic increases in computing performance by
    harnessing the power of the graphics processing unit (GPU).

    Note: This package does not currently install the drivers necessary
    to run CUDA. These will need to be installed manually. See:
    https://docs.nvidia.com/cuda/ for details."""

    homepage = "https://developer.nvidia.com/cuda-zone"

    maintainers("ax3l", "Rombur", "pauleonix")
    executables = ["^nvcc$"]

    skip_version_audit = ["platform=darwin", "platform=windows"]

    for ver, packages in _versions.items():
        pkg = packages.get(f"{platform.system()}-{platform.machine()}")
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    # macOS Mojave drops NVIDIA graphics card support -- official NVIDIA
    # drivers do not exist for Mojave. See
    # https://devtalk.nvidia.com/default/topic/1043070/announcements/faq-about-macos-10-14-mojave-nvidia-drivers/
    # Note that a CUDA Toolkit installer does exist for macOS Mojave at
    # https://developer.nvidia.com/compute/cuda/10.1/Prod1/local_installers/cuda_10.1.168_mac.dmg,
    # but support for Mojave is dropped in later versions, and none of the
    # macOS NVIDIA drivers at
    # https://www.nvidia.com/en-us/drivers/cuda/mac-driver-archive/ mention
    # Mojave support -- only macOS High Sierra 10.13 is supported.
    conflicts("arch=darwin-mojave-x86_64")

    variant(
        "dev", default=False, description="Enable development dependencies, i.e to use cuda-gdb"
    )
    variant(
        "allow-unsupported-compilers",
        default=False,
        sticky=True,
        description="Allow unsupported host compiler and CUDA version combinations",
    )

    depends_on("libxml2", when="@10.1.243:")
    # cuda-gdb needed libncurses.so.5 before 11.4.0
    # see https://docs.nvidia.com/cuda/archive/11.3.1/cuda-gdb/index.html#common-issues-oss
    # see https://docs.nvidia.com/cuda/archive/11.4.0/cuda-gdb/index.html#release-notes
    depends_on("ncurses abi=5", type="run", when="@:11.3.99+dev")

    provides("opencl@:1.2", when="@7:")
    provides("opencl@:1.1", when="@:6")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"Cuda compilation tools, release .*?, V(\S+)", output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        if self.spec.satisfies("@:8.0.61"):
            # Perl 5.26 removed current directory from module search path,
            # CUDA 9 has a fix for this, but CUDA 8 and lower don't.
            env.append_path("PERL5LIB", self.stage.source_path)

        if self.spec.satisfies("@10.1.243:"):
            libxml2_home = self.spec["libxml2"].prefix
            env.set("LIBXML2HOME", libxml2_home)
            env.append_path("LD_LIBRARY_PATH", libxml2_home.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("CUDAHOSTCXX", dependent_spec.package.compiler.cxx)
        env.set("CUDA_HOME", self.prefix)
        env.set("NVHPC_CUDA_HOME", self.prefix)

    @property
    def cmake_prefix_paths(self):
        cmake_prefix_paths = [self.prefix]
        if self.spec.satisfies("target=x86_64:"):
            cub_path = self.prefix.targets + "/x86_64-linux/lib/cmake"
            cmake_prefix_paths.append(cub_path)
        return cmake_prefix_paths

    def setup_run_environment(self, env):
        env.set("CUDA_HOME", self.prefix)
        env.set("NVHPC_CUDA_HOME", self.prefix)

    def install(self, spec, prefix):
        if os.path.exists("/tmp/cuda-installer.log"):
            try:
                os.remove("/tmp/cuda-installer.log")
            except OSError:
                if spec.satisfies("@10.1:"):
                    tty.die(
                        "The cuda installer will segfault due to the "
                        "presence of /tmp/cuda-installer.log "
                        "please remove the file and try again "
                    )
        runfile = glob(join_path(self.stage.source_path, "cuda*_linux*"))[0]

        # Note: NVIDIA does not officially support many newer versions of
        # compilers.  For example, on CentOS 6, you must use GCC 4.4.7 or
        # older. See:
        # http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#system-requirements
        # https://gist.github.com/ax3l/9489132
        # for details.

        # CUDA 10.1 on ppc64le fails to copy some files, the workaround is adapted from
        # https://forums.developer.nvidia.com/t/cuda-10-1-243-10-1-update-2-ppc64le-run-file-installation-issue/82433
        # See also #21170
        if spec.satisfies("@10.1.243") and platform.machine() == "ppc64le":
            includedir = "targets/ppc64le-linux/include"
            os.makedirs(os.path.join(prefix, includedir))
            os.makedirs(os.path.join(prefix, "src"))
            os.symlink(includedir, os.path.join(prefix, "include"))

        install_shell = which("sh")

        if self.spec.satisfies("@:8.0.61"):
            # Perl 5.26 removed current directory from module search path.
            # We are addressing this by exporting `PERL5LIB` earlier, but for some
            # reason, it is not enough. One more file needs to be extracted before
            # running the actual installer. This solution is one of the commonly
            # found on the Internet, when people try to install CUDA <= 8 manually.
            # For example: https://askubuntu.com/a/1087842
            arguments = [runfile, "--tar", "mxvf", "./InstallUtils.pm"]
            install_shell(*arguments)

        # CUDA 10.1+ has different cmdline options for the installer
        arguments = [
            runfile,  # the install script
            "--silent",  # disable interactive prompts
            "--override",  # override compiler version checks
            "--toolkit",  # install CUDA Toolkit
        ]

        if spec.satisfies("@7:"):
            # use stage dir instead of /tmp
            mkdir(join_path(self.stage.path, "tmp"))
            arguments.append("--tmpdir=%s" % join_path(self.stage.path, "tmp"))

        if spec.satisfies("@10.1:"):
            arguments.append("--installpath=%s" % prefix)  # Where to install
        else:
            arguments.append("--verbose")  # Verbose log file
            arguments.append("--toolkitpath=%s" % prefix)  # Where to install

        install_shell(*arguments)

        try:
            os.remove("/tmp/cuda-installer.log")
        except OSError:
            pass

    @property
    def libs(self):
        libs = find_libraries("libcudart", root=self.prefix, shared=True, recursive=True)

        filtered_libs = []
        # CUDA 10.0 provides Compatability libraries for running newer versions
        # of CUDA with older drivers. These do not work with newer drivers.
        for lib in libs:
            parts = lib.split(os.sep)
            if "compat" not in parts and "stubs" not in parts:
                filtered_libs.append(lib)
        return LibraryList(filtered_libs)

    # Avoid binding stub libraries by absolute path
    non_bindable_shared_objects = ["stubs"]
