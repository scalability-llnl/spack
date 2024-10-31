# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyScikitLearn(PythonPackage):
    """A set of python modules for machine learning and data mining."""

    homepage = "https://scikit-learn.org/"
    pypi = "scikit-learn/scikit_learn-1.5.0.tar.gz"
    git = "https://github.com/scikit-learn/scikit-learn.git"

    license("BSD-3-Clause")
    maintainers("adamjstewart", "rgommers")

    version("main", branch="main")
    version("master", branch="main", deprecated=True)
    version("1.5.2", sha256="b4237ed7b3fdd0a4882792e68ef2545d5baa50aca3bb45aa7df468138ad8f94d")
    version("1.5.1", sha256="0ea5d40c0e3951df445721927448755d3fe1d80833b0b7308ebff5d2a45e6414")
    version("1.5.0", sha256="789e3db01c750ed6d496fa2db7d50637857b451e57bcae863bff707c1247bef7")
    version("1.4.2", sha256="daa1c471d95bad080c6e44b4946c9390a4842adc3082572c20e4f8884e39e959")
    version("1.4.0", sha256="d4373c984eba20e393216edd51a3e3eede56cbe93d4247516d205643c3b93121")
    version("1.3.2", sha256="a2f54c76accc15a34bfb9066e6c7a56c1e7235dda5762b990792330b52ccfb05")
    version("1.3.1", sha256="1a231cced3ee3fa04756b4a7ab532dc9417acd581a330adff5f2c01ac2831fcf")
    version("1.3.0", sha256="8be549886f5eda46436b6e555b0e4873b4f10aa21c07df45c4bc1735afbccd7a")
    version("1.2.2", sha256="8429aea30ec24e7a8c7ed8a3fa6213adf3814a6efbea09e16e0a0c71e1a1a3d7")
    version("1.2.1", sha256="fbf8a5c893c9b4b99bcc7ed8fb3e8500957a113f4101860386d06635520f7cfb")
    version("1.2.0", sha256="680b65b3caee469541385d2ca5b03ff70408f6c618c583948312f0d2125df680")
    version("1.1.3", sha256="bef51978a51ec19977700fe7b86aecea49c825884f3811756b74a3b152bb4e35")
    version("1.1.2", sha256="7c22d1305b16f08d57751a4ea36071e2215efb4c09cb79183faa4e8e82a3dbf8")
    version("1.1.1", sha256="3e77b71e8e644f86c8b5be7f1c285ef597de4c384961389ee3e9ca36c445b256")
    version("1.1.0", sha256="80f9904f5b1356adfc32406725dd94c8cc9c8d265047d98390033a6c238cbb29")
    version("1.0.2", sha256="b5870959a5484b614f26d31ca4c17524b1b0317522199dc985c3b4256e030767")
    version("1.0.1", sha256="ac2ca9dbb754d61cfe1c83ba8483498ef951d29b93ec09d6f002847f210a99da")
    version("1.0", sha256="776800194e757cd212b47cd05907e0eb67a554ad333fe76776060dbb729e3427")
    version("0.24.2", sha256="d14701a12417930392cd3898e9646cf5670c190b933625ebe7511b1f7d7b8736")
    version("0.24.1", sha256="a0334a1802e64d656022c3bfab56a73fbd6bf4b1298343f3688af2151810bbdf")
    version("0.24.0", sha256="076369634ee72b5a5941440661e2f306ff4ac30903802dc52031c7e9199ac640")
    version("0.23.2", sha256="20766f515e6cd6f954554387dfae705d93c7b544ec0e6c6a5d8e006f6f7ef480")
    version("0.23.1", sha256="e3fec1c8831f8f93ad85581ca29ca1bb88e2da377fb097cf8322aa89c21bc9b8")
    version("0.23.0", sha256="639a53df6273acc6a7510fb0c658b94e0c70bb13dafff9d14932c981ff9baff4")
    version(
        "0.22.2.post1", sha256="57538d138ba54407d21e27c306735cbd42a6aae0df6a5a30c7a6edde46b0017d"
    )
    version("0.22.1", sha256="51ee25330fc244107588545c70e2f3570cfc4017cff09eed69d6e1d82a212b7d")
    version("0.22", sha256="314abf60c073c48a1e95feaae9f3ca47a2139bd77cebb5b877c23a45c9e03012")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Based on PyPI wheel availability
    with default_args(type=("build", "link", "run")):
        depends_on("python@3.9:3.12", when="@1.4:")
        depends_on("python@3.8:3.12", when="@1.3.1:1.3")
        depends_on("python@3.8:3.11", when="@1.1.3:1.3.0")
        depends_on("python@3.8:3.10", when="@1.1.0:1.1.2")
        depends_on("python@:3.10", when="@1.0.2")
        depends_on("python@:3.9", when="@0.24:1.0.1")
        depends_on("python@:3.8", when="@0.22:0.23")

    with default_args(type="build"):
        depends_on("py-meson-python@0.16:", when="@1.5.1:")
        depends_on("py-meson-python@0.15:", when="@1.5:")
        depends_on("py-cython@3.0.10:", when="@1.5:")
        depends_on("py-cython@3.0.8:", when="@1.4.2:")
        depends_on("py-cython@0.29.33:", when="@1.4.0:1.4.1")
        depends_on("py-cython@0.29.33:2", when="@1.3")
        depends_on("py-cython@0.29.24:2", when="@1.0.2:1.2")
        depends_on("py-cython@0.28.5:2", when="@0.21:1.0.1")

    with default_args(type=("build", "link", "run")):
        depends_on("py-numpy@1.19.5:", when="@1.4:")
        depends_on("py-numpy@1.17.3:", when="@1.1:1.3")
        depends_on("py-numpy@1.14.6:", when="@1.0")
        depends_on("py-numpy@1.13.3:", when="@0.23:0.24")
        depends_on("py-numpy@1.11.0:", when="@0.21:0.22")
        # https://github.com/scikit-learn/scikit-learn/issues/27075
        depends_on("py-numpy@:1", when="@:1.4.1")

    with default_args(type=("build", "run")):
        depends_on("py-scipy@1.6:", when="@1.4:")
        depends_on("py-scipy@1.5:", when="@1.3:")
        depends_on("py-scipy@1.3.2:", when="@1.1:")
        depends_on("py-scipy@1.1.0:", when="@1.0:")
        depends_on("py-scipy@0.19.1:", when="@0.23:")
        depends_on("py-scipy@0.17.0:", when="@0.21:")
        depends_on("py-joblib@1.2:", when="@1.4:")
        depends_on("py-joblib@1.1.1:", when="@1.2:")
        depends_on("py-joblib@1:", when="@1.1:")
        depends_on("py-joblib@0.11:")
        depends_on("py-threadpoolctl@3.1:", when="@1.5:")
        depends_on("py-threadpoolctl@2.0:", when="@0.23:")

    depends_on("llvm-openmp", when="%apple-clang")

    # Historical dependencies
    with default_args(type="build"):
        depends_on("py-setuptools", when="@:1.4")
        depends_on("py-setuptools@:59", when="@:1.2.1")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/s/scikit-learn/{}-{}.tar.gz"
        if version >= Version("1.5"):
            name = "scikit_learn"
        else:
            name = "scikit-learn"
        return url.format(name, version)

    def setup_build_environment(self, env):
        # Enable parallel builds of the sklearn backend
        env.append_flags("SKLEARN_BUILD_PARALLEL", str(make_jobs))

        # https://scikit-learn.org/stable/developers/advanced_installation.html#macos
        if self.spec.satisfies("%apple-clang"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)
