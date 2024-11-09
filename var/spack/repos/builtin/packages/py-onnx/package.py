# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOnnx(PythonPackage):
    """Open Neural Network Exchange (ONNX) is an open ecosystem that
    empowers AI developers to choose the right tools as their
    project evolves. ONNX provides an open source format for AI
    models, both deep learning and traditional ML. It defines an
    extensible computation graph model, as well as definitions of
    built-in operators and standard data types. Currently we focus
    on the capabilities needed for inferencing (scoring)."""

    homepage = "https://github.com/onnx/onnx"
    pypi = "Onnx/onnx-1.6.0.tar.gz"

    license("Apache-2.0", checked_by="wdconinc")

    version("1.16.2", sha256="b33a282b038813c4b69e73ea65c2909768e8dd6cc10619b70632335daf094646")
    version("1.16.1", sha256="8299193f0f2a3849bfc069641aa8e4f93696602da8d165632af8ee48ec7556b6")
    version("1.16.0", sha256="237c6987c6c59d9f44b6136f5819af79574f8d96a760a1fa843bede11f3822f7")
    version("1.15.0", sha256="b18461a7d38f286618ca2a6e78062a2a9c634ce498e631e708a8041b00094825")
    version("1.14.1", sha256="70903afe163643bd71195c78cedcc3f4fa05a2af651fd950ef3acbb15175b2d1")
    version("1.14.0", sha256="43b85087c6b919de66872a043c7f4899fe6f840e11ffca7e662b2ce9e4cc2927")
    version("1.13.1", sha256="0bdcc25c2c1ce4a8750e4ffbd93ae945442e7fac6e51176f38e366b74a97dfd9")
    version("1.13.0", sha256="410b39950367857f97b65093681fe2495a2e23d63777a8aceaf96c56a16d166e")
    version("1.12.0", sha256="13b3e77d27523b9dbf4f30dfc9c959455859d5e34e921c44f712d69b8369eff9")
    version("1.11.0", sha256="eca224c7c2c8ee4072a0743e4898a84a9bdf8297b5e5910a2632e4c4182ffb2a")
    version("1.10.1", sha256="9d941ba76cab55db8913ecad9dc50cefeb368460f6338a91783a5d7643f3a044")
    version("1.8.1", sha256="9d65c52009a90499f8c25fdfe5acda3ac88efe0788eb1d5f2575a989277145fb")
    version("1.6.0", sha256="3b88c3fe521151651a0403c4d131cb2e0311bd28b753ef692020a432a81ce345")
    version("1.5.0", sha256="1a584a4ef62a6db178c257fffb06a9d8e61b41c0a80bfd8bcd8a253d72c4b0b4")

    depends_on("cxx", type="build")  # generated

    # CMakeLists.txt
    depends_on("cmake@3.1:", type="build")
    depends_on("py-pybind11@2.2:", type=("build", "link"))

    # requirements.txt
    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("protobuf")
    depends_on("py-protobuf@3.20.2:", type=("build", "run"), when="@1.15:")
    depends_on("py-protobuf@3.20.2:3", type=("build", "run"), when="@1.13")
    depends_on("py-protobuf@3.12.2:3.20.1", type=("build", "run"), when="@1.12")
    depends_on("py-protobuf@3.12.2:", type=("build", "run"), when="@1.11")
    # https://github.com/protocolbuffers/protobuf/issues/10051
    # https://github.com/onnx/onnx/issues/4222
    depends_on("py-protobuf@:3", type=("build", "run"), when="@1.10")
    # Protobuf version limit is due to removal of SetTotalBytesLimit in
    # https://github.com/protocolbuffers/protobuf/pull/8794, fixed in
    # https://github.com/onnx/onnx/pull/3112
    depends_on("py-protobuf@:3.17", type=("build", "run"), when="@:1.8")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-numpy@1.16.6:", type=("build", "run"), when="@1.8.1:1.13")
    depends_on("py-numpy@1.20:", type=("build", "run"), when="@1.16.0:")
    depends_on("py-numpy@1.21:", type=("build", "run"), when="@1.16.2:")
    depends_on("py-numpy@:1", type=("build", "run"), when="@:1.16")

    # Historical dependencies
    depends_on("py-six", type=("build", "run"), when="@:1.8.1")
    depends_on("py-typing-extensions@3.6.2.1:", type=("build", "run"), when="@:1.14")
    depends_on("py-pytest-runner", type="build", when="@:1.14")

    # 'python_out' does not recognize dllexport_decl.
    patch("remove_dllexport_decl.patch", when="@:1.6.0")

    # Switch the CMAKE_CXX_STANDARD to 17 if abseil-cpp has been built with
    # either of those. (abseil-cpp is pulled in via protobuf)
    patch(
        "https://github.com/onnx/onnx/commit/1f6e43cb4d7366b2dffa7f70ae88198306e12c6c.patch?full_index=1",
        sha256="be12f589bc4113982e4162efcdbd95835a6c161a9a7e10cd1dde026cadedf8aa",
        when="@1.15.0 ^abseil-cpp cxxstd=17",
    )
    patch(
        "https://github.com/onnx/onnx/commit/1f6e43cb4d7366b2dffa7f70ae88198306e12c6c.patch?full_index=1",
        sha256="be12f589bc4113982e4162efcdbd95835a6c161a9a7e10cd1dde026cadedf8aa",
        when="@1.15.0 ^abseil-cpp cxxstd=20",
    )

    # By default, ONNX always uses .setuptools-cmake-build/ under the source path,
    # so we allow overriding with a build environment variable
    def patch(self):
        filter_file(
            r"^CMAKE_BUILD_DIR = (.*)$",
            r"CMAKE_BUILD_DIR = os.getenv('CMAKE_BUILD_DIR', default=\1)",
            "setup.py",
        )

    def setup_build_environment(self, env):
        # Build in a similar directory as the CMake packages
        env.set(
            "CMAKE_BUILD_DIR", join_path(self.stage.path, f"spack-build-{self.spec.dag_hash(7)}")
        )
