# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ospray(CMakePackage):
    """Intel OSPRay is an open source, scalable, and portable ray tracing engine for
    high-performance, high-fidelity visualization on Intel Architecture CPUs."""

    homepage = "https://www.ospray.org/"
    url = "https://github.com/RenderKit/ospray/archive/v2.10.0.tar.gz"
    git = "https://github.com/RenderKit/ospray.git"

    # maintainers("aumuell")

    version("3.2.0", sha256="2c8108df2950bc5d1bc2a62f74629233dbe4f36e3f6a8ea032907d4a3fdc6750")
    version("3.1.0", sha256="0b9d7df900fe0474b12e5a2641bb9c3f5a1561217b2789834ebf994a15288a82")
    version("3.0.0", sha256="d8d8e632d77171c810c0f38f8d5c8387470ca19b75f5b80ad4d3d12007280288")
    version("2.12.0", sha256="268b16952b2dd44da2a1e40d2065c960bc2442dd09b63ace8b65d3408f596301")
    version("2.11.0", sha256="55974e650d9b78989ee55adb81cffd8c6e39ce5d3cf0a3b3198c522bf36f6e81")
    version("2.10.0", sha256="bd478284f48d2cb775fc41a2855a9d9f5ea16c861abda0f8dc94e02ea7189cb8")
    version("2.9.0", sha256="0145e09c3618fb8152a32d5f5cff819eb065d90975ee4e35400d2db9eb9f6398")
    version("2.8.0", sha256="2dabc75446a0e2e970952d325f930853a51a9b4d1868c8135f05552a4ae04d39")
    version("2.7.1", sha256="4e7bd8145e19541c04f5d949305f19a894d85a827f567d66ae2eb11a760a5ace")
    version("2.7.0", sha256="bcaeb221b5dd383d27587ffaca7f75d7e0064f64017a0d73df90862b14b5704b")
    version("2.6.0", sha256="5efccd7eff5774b77f8894e68a6b803b535a0d12f32ab49edf13b954e2848f2e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("apps", default=False, description="Enable building OSPRay Apps")
    variant("denoiser", default=True, description="Enable denoiser image operation")
    variant("glm", default=False, description="Build ospray_cpp GLM tests/tutorial")
    variant("mpi", default=True, description="Enable MPI support")
    variant("volumes", default=True, description="Enable volumetric rendering with Open VKL")

    conflicts("~volumes", when="@:2.10")

    depends_on("rkcommon@1.5:")
    depends_on("rkcommon@1.7:1.9", when="@2.7.0:2.8")
    depends_on("rkcommon@1.9", when="@2.9.0")
    depends_on("rkcommon@1.10:", when="@2.10.0:")
    depends_on("rkcommon@1.11.0", when="@2.11:2.12")
    depends_on("rkcommon@1.12.0", when="@3.0")
    depends_on("rkcommon@1.13.0", when="@3.1")
    depends_on("rkcommon@1.14.0", when="@3.2")
    depends_on("embree@3.12: +ispc")
    depends_on("embree@3.13.1:", when="@2.7.0:")
    depends_on("embree@:3", when="@:2.10")
    depends_on("embree@4:", when="@2.11:")
    depends_on("embree@4.3:", when="@3:")
    depends_on("embree@4.3.3:", when="@3.2:")
    with when("+volumes"):
        depends_on("openvkl@0.13.0:1", when="@2")
        depends_on("openvkl@1.0.1:", when="@2.7.0:")
        depends_on("openvkl@1.2.0:", when="@2.9.0:")
        depends_on("openvkl@1.3.0:", when="@2.10.0:")
        depends_on("openvkl@1.3.2:", when="@2.11:2")
        depends_on("openvkl@2:", when="@3:")
        depends_on("openvkl@2.0.1:", when="@3.2:")
    with when("+denoiser"):
        depends_on("openimagedenoise@1.2.3:")
        depends_on("openimagedenoise@1.3:", when="@2.5:")
        depends_on("openimagedenoise@:1", when="@:2.11")
        depends_on("openimagedenoise@2:", when="@2.12:")
        depends_on("openimagedenoise@2.1:", when="@3:")
        depends_on("openimagedenoise@2.3:", when="@3.2:")
    depends_on("ispc@1.14.1:", type=("build"))
    depends_on("ispc@1.16.0:", when="@2.7.0:", type=("build"))
    depends_on("ispc@1.18.0:", when="@2.10.0:", type=("build"))
    depends_on("ispc@1.19.0:", when="@2.11.0:", type=("build"))
    depends_on("ispc@1.20.0:", when="@2.12.0:", type=("build"))
    depends_on("ispc@1.21.1:", when="@3:", type=("build"))
    depends_on("ispc@1.23.0:", when="@3.2:", type=("build"))
    depends_on("tbb")

    with when("+mpi"):
        depends_on("mpi")
        depends_on("snappy@1.1.8:")
        depends_on("snappy@1.2.1:", when="@3.2:")

    def cmake_args(self):
        args = [
            self.define_from_variant("OSPRAY_MODULE_DENOISER", "denoiser"),
            self.define("OSPRAY_ENABLE_MODULES", True),
            self.define("OSPRAY_ENABLE_APPS", False),
            self.define_from_variant("OSPRAY_MODULE_MPI", "mpi"),
            self.define("OSPRAY_MPI_BUILD_TUTORIALS", False),
            self.define("OSPRAY_ISPC_DIRECTORY", self.spec["ispc"].prefix.bin),
            self.define_from_variant("OSPRAY_APPS_ENABLE_GLM", "glm"),
        ]

        # support for volumetric data
        if self.spec.satisfies("@2.11:"):
            args.append(self.define_from_variant("OSPRAY_ENABLE_VOLUMES", "volumes"))

        # Apps
        enable_apps_arg = "" if self.spec.satisfies("@2.9:") else "ENABLE_"
        args.extend(
            [
                self.define("OSPRAY_{0}APPS_TESTING".format(enable_apps_arg), False),
                self.define("OSPRAY_{0}APPS_EXAMPLES".format(enable_apps_arg), False),
                self.define("OSPRAY_{0}APPS_TUTORIALS".format(enable_apps_arg), False),
                self.define("OSPRAY_{0}APPS_BENCHMARK".format(enable_apps_arg), False),
            ]
        )

        return args
