# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyarrow(PythonPackage):
    """A cross-language development platform for in-memory data.

    This package contains the Python bindings.
    """

    homepage = "https://arrow.apache.org"
    pypi = "pyarrow/pyarrow-0.17.1.tar.gz"
    git = "https://github.com/apache/arrow"

    maintainers("thomas-bouvier")

    license("Apache-2.0")

    version("19.0.1", sha256="3bf266b485df66a400f282ac0b6d1b500b9d2ae73314a153dbe97d6d5cc8a99e")
    version("16.1.0", sha256="15fbb22ea96d11f0b5768504a3f961edab25eaf4197c341720c4a387f6c60315")
    version("15.0.2", sha256="9c9bc803cb3b7bfacc1e96ffbfd923601065d9d3f911179d81e72d99fd74a3d9")
    version("14.0.2", sha256="36cef6ba12b499d864d1def3e990f97949e0b79400d08b7cf74504ffbd3eb025")
    version("13.0.0", sha256="83333726e83ed44b0ac94d8d7a21bbdee4a05029c3b1e8db58a863eec8fd8a33")
    version("12.0.1", sha256="cce317fc96e5b71107bf1f9f184d5e54e2bd14bbf3f9a3d62819961f0af86fec")
    version("11.0.0", sha256="5461c57dbdb211a632a48facb9b39bbeb8a7905ec95d768078525283caef5f6d")
    version("10.0.1", sha256="1a14f57a5f472ce8234f2964cd5184cccaa8df7e04568c64edc33b23eb285dd5")
    version("8.0.0", sha256="4a18a211ed888f1ac0b0ebcb99e2d9a3e913a481120ee9b1fe33d3fedb945d4e")
    version("7.0.0", sha256="da656cad3c23a2ebb6a307ab01d35fce22f7850059cffafcb90d12590f8f4f38")
    version("4.0.1", sha256="11517f0b4f4acbab0c37c674b4d1aad3c3dfea0f6b1bb322e921555258101ab3")
    version("3.0.0", sha256="4bf8cc43e1db1e0517466209ee8e8f459d9b5e1b4074863317f2a965cf59889e")
    version("0.17.1", sha256="278d11800c2e0f9bea6314ef718b2368b4046ba24b6c631c14edad5a1d351e49")
    version("0.15.1", sha256="7ad074690ba38313067bf3bbda1258966d38e2037c035d08b9ffe3cce07747a5")
    version("0.12.1", sha256="10db6e486c918c3af999d0114a22d92770687e3a6607ea3f14e6748854824c2a")
    version("0.11.0", sha256="07a6fd71c5d7440f2c42383dd2c5daa12d7f0a012f1e88288ed08a247032aead")
    version("0.9.0", sha256="7db8ce2f0eff5a00d6da918ce9f9cfec265e13f8a119b4adb1595e5b19fd6242")

    depends_on("cxx", type="build")

    with default_args(type="build"):
        # CMakeLists.txt
        depends_on("cmake@3.16:", when="@13:")
        depends_on("cmake@3.5:", when="@11:")
        depends_on("cmake@3.2:", when="@0.17:")
        depends_on("cmake@2.7:")

        # cmake_modules and pyarrow/__init__.py
        depends_on("pkgconfig")

        # pyproject.toml, setup.py
        depends_on("py-cython@0.29.31:", when="@14:")
        depends_on("py-cython@0.29.31:2", when="@12:13")
        depends_on("py-cython@0.29.22:2", when="@8:11")
        depends_on("py-cython@0.29:2", when="@0.15:7")
        depends_on("py-cython@:2", when="@:0.14")
        depends_on("py-setuptools-scm@8:+toml", when="@17:")
        depends_on("py-setuptools-scm", when="@16")
        depends_on("py-setuptools-scm@:7", when="@0.15:15")
        depends_on("py-setuptools@64:", when="@17:")
        depends_on("py-setuptools@40.1:", when="@10.0.1:")
        depends_on("py-setuptools@38.6:", when="@7:")
        depends_on("py-setuptools")

    arrow_versions = (
        "@0.9.0",
        "@0.11.0",
        "@0.12.1",
        "@0.15.1",
        "@0.17.1",
        "@3.0.0",
        "@4.0.1",
        "@7.0.0",
        "@8.0.0",
        "@10.0.1",
        "@11.0.0",
        "@12.0.1",
        "@13.0.0",
        "@14.0.2",
        "@15.0.2",
        "@16.1.0",
        "@19.0.1",
    )
    for v in arrow_versions:
        depends_on("arrow+python" + v, when=v)

    # Historical dependencies
    # In newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", when="@:16", type="build")

    with default_args(type=("build", "run")):
        # pyproject.toml, setup.py
        depends_on("py-numpy@1.16.6:", when="@3:17")
        depends_on("py-numpy@1.14:", when="@0.11:")
        depends_on("py-numpy@1.10:")
        depends_on("py-numpy@:1", when="@:15")

    patch("for_aarch64.patch", when="@0 target=aarch64:")

    # Starting with pyarrow 17+, backend support is built if arrow was built with it
    @when("@:16")
    def setup_build_environment(self, env):
        env.set("PYARROW_WITH_PARQUET", self.spec.satisfies("^arrow+parquet"))
        env.set("PYARROW_WITH_CUDA", self.spec.satisfies("^arrow+cuda"))
        env.set("PYARROW_WITH_ORC", self.spec.satisfies("^arrow+orc"))
        env.set("PYARROW_WITH_DATASET", self.spec.satisfies("^arrow+dataset"))

    @when("@:16")
    def install_options(self, spec, prefix):
        args = []
        if spec.satisfies("^arrow+parquet"):
            args.append("--with-parquet")
        if spec.satisfies("^arrow+cuda"):
            args.append("--with-cuda")
        if spec.satisfies("^arrow+orc"):
            args.append("--with-orc")
        if spec.satisfies("^arrow+dataset"):
            args.append("--with-dataset")
        return args
