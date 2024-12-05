# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenv(PythonPackage):
    """virtualenv is a tool to create isolated Python environments."""

    homepage = "https://virtualenv.pypa.io/"
    pypi = "virtualenv/virtualenv-16.7.6.tar.gz"
    git = "https://github.com/pypa/virtualenv.git"

    license("MIT")
    version("20.26.5", sha256="ce489cac131aa58f4b25e321d6d186171f78e6cb13fafbf32a840cee67733ff4")
    version("20.26.4", sha256="c17f4e0f3e6036e9f26700446f85c76ab11df65ff6d8a9cbfad9f71aabfcf23c")
    version("20.26.3", sha256="4c43a2a236279d9ea36a0d76f98d84bd6ca94ac4e0f4a3b9d46d05e10fea542a")
    version("20.26.2", sha256="82bf0f4eebbb78d36ddaee0283d43fe5736b53880b8a8cdcd37390a07ac3741c")
    version("20.26.1", sha256="604bfdceaeece392802e6ae48e69cec49168b9c5f4a44e483963f9242eb0e78b")
    version("20.26.0", sha256="ec25a9671a5102c8d2657f62792a27b48f016664c6873f6beed3800008577210")
    version("20.25.3", sha256="7bb554bbdfeaacc3349fa614ea5bff6ac300fc7c335e9facf3a3bcfc703f45be")
    version("20.25.2", sha256="fa7edb8428620518010928242ec17aa7132ae435319c29c1651d1cf4c4173aad")
    version("20.25.1", sha256="e08e13ecdca7a0bd53798f356d5831434afa5b07b93f0abdf0797b7a06ffe197")
    version("20.25.0", sha256="bf51c0d9c7dd63ea8e44086fa1e4fb1093a31e963b86959257378aef020e1f1b")
    version("20.24.5", sha256="e8361967f6da6fbdf1426483bfe9fca8287c242ac0bc30429905721cefbff752")
    version("20.22.0", sha256="278753c47aaef1a0f14e6db8a4c5e1e040e90aea654d0fc1dc7e0d8a42616cc3")
    version("20.17.1", sha256="f8b927684efc6f1cc206c9db297a570ab9ad0e51c16fa9e45487d36d1905c058")
    version("20.16.4", sha256="014f766e4134d0008dcaa1f95bafa0fb0f575795d07cae50b1bee514185d6782")
    version("20.10.0", sha256="576d05b46eace16a9c348085f7d0dc8ef28713a2cabaa1cf0aea41e8f12c9218")
    version("16.7.6", sha256="5d370508bf32e522d79096e8cbea3499d47e624ac7e11e9089f9397a0b3318df")
    version("16.4.1", sha256="5a3ecdfbde67a4a3b3111301c4d64a5b71cf862c8c42958d30cf3253df1f29dd")
    version("16.0.0", sha256="ca07b4c0b54e14a91af9f34d0919790b016923d157afda5efdde55c96718f752")
    version("15.1.0", sha256="02f8102c2436bb03b3ee6dede1919d1dac8a427541652e5ec95171ec8adbc93a")
    version("15.0.1", sha256="1a74278b8adb383ce4c7619e33c753b1eb7b58dc1e449601c096ca4b76125f84")
    version("13.0.1", sha256="36c2cfae0f9c6462264bb19c478fc6bab3478cf0575f1027452e975a1ed84dbd")
    version("1.11.6", sha256="3e7a4c151e2ee97f51db0215bfd2a073b04a91e9786df6cb67c916f16abe04f7")

    depends_on("c", type="build")  # generated

    depends_on("py-hatch-vcs@0.3:", when="@20.18:", type="build")
    depends_on("py-hatchling@1.17.1:", when="@20.23.1:", type="build")
    depends_on("py-hatchling@1.14:", when="@20.22:", type="build")
    depends_on("py-hatchling@1.12.2:", when="@20.18:", type="build")

    depends_on("py-distlib@0.3.7:0", when="@20.24.2:", type=("build", "run"))
    depends_on("py-distlib@0.3.6:0", when="@20.16.6:20.24.1", type=("build", "run"))
    depends_on("py-distlib@0.3.5:0", when="@20.16.3:20.16.5", type=("build", "run"))
    depends_on("py-distlib@0.3.1:0", when="@20.0.26:20.16.2", type=("build", "run"))
    depends_on("py-distlib@0.3.0:0", when="@20.0.0:20.0.25", type=("build", "run"))
    depends_on("py-filelock@3.12.2:3", when="@20.24.2:", type=("build", "run"))
    depends_on("py-filelock@3.11:3", when="@20.22:20.23.0", type=("build", "run"))
    depends_on("py-filelock@3.4.1:3", when="@20.16.3:20.21", type=("build", "run"))
    depends_on("py-filelock@3.2:3", when="@20.9:20.16.2", type=("build", "run"))
    depends_on("py-filelock@3.0.0:3", when="@20.0:20.8", type=("build", "run"))
    depends_on("py-importlib-metadata@6.6:", when="@20.23.1: ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@6.4.1:", when="@20.22: ^python@:3.7", type=("build", "run"))
    depends_on(
        "py-importlib-metadata@4.8.3:", when="@20.16.3: ^python@:3.7", type=("build", "run")
    )
    depends_on("py-importlib-metadata@0.12:", when="@20.2.1: ^python@:3.7", type=("build", "run"))
    depends_on(
        "py-importlib-metadata@0.12:3", when="@20.0.0:20.2.0 ^python@:3.7", type=("build", "run")
    )
    depends_on("py-platformdirs@3.9.1:3", when="@20.24.1:", type=("build", "run"))
    depends_on("py-platformdirs@3.2:3", when="@20.22:20.23.0", type=("build", "run"))
    depends_on("py-platformdirs@2.4:2", when="@20.16.3:20.21", type=("build", "run"))
    depends_on("py-platformdirs@2:2", when="@20.5:20.16.2", type=("build", "run"))

    # Historical dependencies
    with when("@:20.17"):
        # not just build-time, requires pkg_resources
        depends_on("py-setuptools@59.6:", when="@20.16.3:", type=("build", "run"))
        depends_on("py-setuptools@41.0.0:", when="@20.0.0:20.16.2", type=("build", "run"))
        depends_on("py-setuptools@40.6.3:", when="@16.1.2:16", type=("build", "run"))
        depends_on("py-setuptools@40.0.4:", when="@16.1.0", type=("build", "run"))
        depends_on("py-setuptools", type=("build", "run"))
        depends_on("py-setuptools-scm@6.4.2:", when="@20.16.3:", type="build")
        depends_on("py-setuptools-scm@2:", when="@20.0.5:20.16.2", type="build")
        depends_on("py-setuptools-scm+toml@3.4:", when="@20.0.0:20.0.4", type="build")
        depends_on("py-wheel@0.30:", when="@20.0.0:20.16.2", type="build")
        depends_on("py-wheel@0.29:", when="@16.1:16", type="build")

    depends_on(
        "py-backports-entry-points-selectable @1.0.4:", when="@20.5:20.10", type=("build", "run")
    )
    depends_on("py-six@1.9.0:1", when="@20.0.4:20.15", type=("build", "run"))
    depends_on("py-six@1.12.0:1", when="@20.0.0:20.0.3", type=("build", "run"))
    depends_on("py-appdirs@1.4.3:1", when="@20.0.0:20.4", type=("build", "run"))

    skip_modules = ["virtualenv.discovery.windows"]
