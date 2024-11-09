# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCryptography(PythonPackage):
    """cryptography is a package which provides cryptographic recipes
    and primitives to Python developers"""

    homepage = "https://github.com/pyca/cryptography"
    pypi = "cryptography/cryptography-1.8.1.tar.gz"

    license("Apache-2.0")

    version("42.0.8", sha256="8d09d05439ce7baa8e9e95b07ec5b6c886f548deb7e0f69ef25f64b3bce842f2")
    version("41.0.7", sha256="13f93ce9bea8016c253b34afc6bd6a75993e5c40672ed5405a9c832f0d4a00bc")
    version("41.0.3", sha256="6d192741113ef5e30d89dcb5b956ef4e1578f304708701b8b73d38e3e1461f34")
    version("40.0.2", sha256="c33c0d32b8594fa647d2e01dbccc303478e16fdd7cf98652d5b3ed11aa5e5c99")
    version("38.0.1", sha256="1db3d807a14931fa317f96435695d9ec386be7b84b618cc61cfa5d08b0ae33d7")
    version("37.0.4", sha256="63f9c17c0e2474ccbebc9302ce2f07b55b3b3fcb211ded18a42d5764f5c10a82")
    version("36.0.1", sha256="53e5c1dc3d7a953de055d77bef2ff607ceef7a2aac0353b5d630ab67f7423638")
    version("35.0.0", sha256="9933f28f70d0517686bd7de36166dda42094eac49415459d9bdf5e7df3e0086d")
    version("3.4.8", sha256="94cc5ed4ceaefcbe5bf38c8fba6a21fc1d365bb8fb826ea1688e3370b2e24a1c")
    version("3.4.7", sha256="3d10de8116d25649631977cb37da6cbdd2d6fa0e0281d014a5b7d337255ca713")
    version("3.3.2", sha256="5a60d3780149e13b7a6ff7ad6526b38846354d11a15e21068e57073e29e19bed")
    version("3.2.1", sha256="d3d5e10be0cf2a12214ddee45c6bd203dab435e3d83b4560c03066eda600bfe3")
    version("2.8", sha256="3cda1f0ed8747339bbdf71b9f38ca74c7b592f24f65cdb3ab3765e4b02871651")
    version("2.7", sha256="e6347742ac8f35ded4a46ff835c60e68c22a536a8ae5c4422966d06946b6d4c6")
    version("2.3.1", sha256="8d10113ca826a4c29d5b85b2c4e045ffa8bad74fb525ee0eceb1d38d4c70dfd6")
    version("1.8.1", sha256="323524312bb467565ebca7e50c8ae5e9674e544951d28a2904a50012a8828190")

    variant("idna", default=False, when="@2.5:3.0", description="Deprecated U-label support")

    # distutils required in version <= 40
    depends_on("python@:3.11", when="@:40", type=("build", "run"))
    depends_on("py-setuptools@61.0:", when="@41:", type="build")
    depends_on("py-setuptools@40.6:60.8,60.9.1:", when="@37:", type="build")
    depends_on("py-setuptools@40.6:", when="@2.7:36", type="build")
    depends_on("py-setuptools@18.5:", when="@2.2:2.6", type="build")
    depends_on("py-setuptools@11.3:", when="@:2.1", type="build")
    depends_on("py-setuptools-rust@1.7.0:", when="@42:", type=("build", "run"))
    depends_on("py-setuptools-rust@0.11.4:", when="@3.4.2:", type="build")
    depends_on("py-setuptools-rust@0.11.4:", when="@3.4:3.4.1", type=("build", "run"))
    depends_on("rust@1.56:", when="@41:", type="build")
    depends_on("rust@1.48:", when="@38:", type="build")
    depends_on("rust@1.41:", when="@3.4.5:", type="build")
    depends_on("rust@1.45:", when="@3.4.3:3.4.4", type="build")
    depends_on("pkgconfig", when="@40:", type="build")

    depends_on("py-cffi@1.12:", when="@3.3:", type=("build", "run"))
    depends_on("py-cffi@1.8:1.11.2,1.11.4:", when="@2.5:3.2", type=("build", "run"))
    depends_on("py-cffi@1.7:1.11.2,1.11.4:", when="@1.9:2.4.2", type=("build", "run"))
    depends_on("py-cffi@1.4.1:", type=("build", "run"))

    depends_on("py-asn1crypto@0.21.0:", type=("build", "run"), when="@:2.7")
    depends_on("py-six@1.4.1:", type=("build", "run"), when="@:3.3")
    depends_on("py-idna@2.1:", type=("build", "run"), when="@:2.4")  # deprecated
    depends_on("py-idna@2.1:", type=("build", "run"), when="@2.5: +idna")  # deprecated

    depends_on("openssl")
    depends_on("openssl@:1.0", when="@:1.8.1")
    depends_on("openssl@:1.1", when="@:3.4")
    depends_on("openssl@1.1.1:", when="@39:")

    # To fix https://github.com/spack/spack/issues/29669
    # https://community.home-assistant.io/t/error-failed-building-wheel-for-cryptography/352020/14
    # We use CLI git instead of Cargo's internal git library
    # See reference: https://doc.rust-lang.org/cargo/reference/config.html#netgit-fetch-with-cli
    depends_on("git", type="build", when="@35:")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@35:"):
            env.set("CARGO_NET_GIT_FETCH_WITH_CLI", "true")
