# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class Rpp(CMakePackage):
    """Radeon Performance Primitives (RPP) library is a comprehensive high-
    performance computer vision library for AMD (CPU and GPU) with HIP
    and OPENCL back-ends"""

    homepage = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/rpp"
    git = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/rpp.git"
    url = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/rpp/archive/refs/tags/rocm-6.1.2.tar.gz"

    def url_for_version(self, version):
        if version >= Version("5.7.0"):
            url = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/rpp/archive/refs/tags/rocm-{0}.tar.gz"
        else:
            url = "https://github.com/GPUOpen-ProfessionalCompute-Libraries/rpp/archive/{0}.tar.gz"
        return url.format(version)

    tags = ["rocm"]

    maintainers("srekolam", "afzpatel")
    license("MIT")
    version("6.2.1", sha256="5ae9d0c6733ba0e00be1cda13003e98acebd3f86de59e6f1969e297d673f124e")
    version("6.2.0", sha256="69fbebf50b734e055258ea3c5b0399a51babab8f66074166d2b0fc4f1904c09c")
    version("6.1.2", sha256="3a529bdd17b448a9e05a6aac1b5e173a077f4a4a1fd2ed759bcea331acd2829f")
    version("6.1.1", sha256="9ca385c6f208a0bbf2be60ad15697d35371992d49ed30077b69e22090cef657c")
    version("6.1.0", sha256="026c5ac7a92e14e35b9e7630a2ebfff3f4b3544b988eb9aa8af9991d4beea242")
    version("6.0.2", sha256="2686eb4099233db4444fcd2f77af9b00d38d829f05de2403bed37b1b28f2653c")
    version("6.0.0", sha256="3626a648bc773520f5cd5ca15f494de6e74b422baf32491750ce0737c3367f15")
    version("5.7.1", sha256="36fff5f1c52d969c3e2e0c75b879471f731770f193c9644aa6ab993fb8fa4bbf")
    version("5.7.0", sha256="1c612cde3c3d3840ae75ee5c1ee59bd8d61b1fdbf84421ae535cda863470fc06")
    version("1.2.0", sha256="660a11e1bd8706967835597b26daa874fd1507459bfebe22818149444bec540c")
    with default_args(deprecated=True):
        version("1.1.0", sha256="9b1b9e721df27ee577819710b261071c68b2dccba96d9daf5d0535ee5f0e045f")
        version("1.0.0", sha256="040601e356b0a06c4ffb2043320ae822ab0da78af867392002c7b68dbd85989c")
        version("0.99", sha256="f1d7ec65d0148ddb7b3ce836a7e058727036df940d72d1683dee590a913fd44a")
        version("0.98", sha256="191b5d89bf990ae22b5ef73675b89ed4371c3ce342ab9cc65383fa12ef13086e")
        version("0.97", sha256="8ce1a869ff67a29579d87d399d8b0bd97bf12ae1b6b1ca1f161cb8a262fb9939")

    depends_on("cxx", type="build")  # generated
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    # Adding 3 variants OPENCL ,HIP , CPU with HIP as default.

    variant("opencl", default=False, description="Use OPENCL as the backend")
    variant("hip", default=True, description="Use HIP as backend")
    variant("cpu", default=False, description="Use CPU as backend")
    variant(
        "add_tests",
        default=False,
        description="add utilities folder which contains rpp unit tests",
    )
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    patch("0001-include-half-openmp-through-spack-package.patch", when="@:5.7")
    patch("0002-declare-handle-in-header.patch")
    patch("0003-include-half-through-spack-package.patch", when="@6.0:")

    # adds half.hpp include directory and modifies how the libjpegturbo
    # library is linked for the rpp unit test
    patch("0003-changes-to-rpp-unit-tests.patch", when="@5.7:6.0 +add_tests")
    patch("0003-changes-to-rpp-unit-tests-6.1.patch", when="@6.1 +add_tests")

    def patch(self):
        if self.spec.satisfies("+hip"):
            filter_file(
                "${ROCM_PATH}/llvm", self.spec["llvm-amdgpu"].prefix, "CMakeLists.txt", string=True
            )
            if self.spec.satisfies("+asan"):
                filter_file(
                    "CMAKE_CXX_COMPILER clang++",
                    "CMAKE_CXX_COMPILER {0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
                    "CMakeLists.txt",
                    string=True,
                )
        if self.spec.satisfies("+opencl"):
            filter_file(
                "${ROCM_PATH}",
                self.spec["rocm-opencl"].prefix,
                "cmake/FindOpenCL.cmake",
                string=True,
            )
        if self.spec.satisfies("+add_tests"):
            filter_file(
                "${ROCM_PATH}/include/rpp",
                self.spec.prefix.include.rpp,
                "utilities/test_suite/HOST/CMakeLists.txt",
                string=True,
            )
            filter_file(
                "${ROCM_PATH}/lib",
                self.spec.prefix.lib,
                "utilities/test_suite/HOST/CMakeLists.txt",
                string=True,
            )
            filter_file(
                "${ROCM_PATH}/include/rpp",
                self.spec.prefix.include.rpp,
                "utilities/test_suite/HIP/CMakeLists.txt",
                string=True,
            )
            filter_file(
                "${ROCM_PATH}/lib",
                self.spec.prefix.lib,
                "utilities/test_suite/HIP/CMakeLists.txt",
                string=True,
            )
            filter_file(
                "${ROCM_PATH}/share/rpp/test/cmake",
                self.spec.prefix.share.rpp.test.cmake,
                "utilities/test_suite/HOST/CMakeLists.txt",
                string=True,
            )
            filter_file(
                "${ROCM_PATH}/share/rpp/test/cmake",
                self.spec.prefix.share.rpp.test.cmake,
                "utilities/test_suite/HIP/CMakeLists.txt",
                string=True,
            )

    depends_on("cmake@3.5:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on(Boost.with_default_variants)
    depends_on("boost@1.72.0:1.85.0")
    depends_on("bzip2")
    depends_on("half")
    depends_on("hwloc")
    depends_on(
        "opencv@4.5:"
        "+calib3d+features2d+highgui+imgcodecs+imgproc"
        "+video+videoio+flann+photo+objdetect",
        type=("build", "link"),
        when="@1.0:",
    )
    depends_on("libjpeg-turbo", type=("build", "link"))
    depends_on("rocm-openmp-extras")
    conflicts("+opencl+hip")

    with when("+hip"):
        with when("@5.7:"):
            for ver in [
                "5.7.0",
                "5.7.1",
                "6.0.0",
                "6.0.2",
                "6.1.0",
                "6.1.1",
                "6.1.2",
                "6.2.0",
                "6.2.1",
            ]:
                depends_on("hip@" + ver, when="@" + ver)
        with when("@:1.2"):
            depends_on("hip@5:")
    with when("~hip"):
        depends_on("rocm-opencl@5:")

    def setup_run_environment(self, env):
        if self.spec.satisfies("+add_tests"):
            env.set("TURBO_JPEG_PATH", self.spec["libjpeg-turbo"].prefix)
        if self.spec.satisfies("@6.1:"):
            env.prepend_path("LD_LIBRARY_PATH", self.spec["hsa-rocr-dev"].prefix.lib)

    def setup_build_environment(self, env):
        if self.spec.satisfies("+asan"):
            env.set("CC", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("CXX", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define("ROCM_OPENMP_EXTRAS_DIR", spec["rocm-openmp-extras"].prefix))
        if self.spec.satisfies("+opencl"):
            args.append(self.define("BACKEND", "OPENCL"))
        if self.spec.satisfies("+cpu"):
            args.append(self.define("BACKEND", "CPU"))
        if self.spec.satisfies("+hip"):
            args.append(self.define("BACKEND", "HIP"))
            args.append(self.define("HIP_PATH", spec["hip"].prefix))
            args.append(
                self.define(
                    "COMPILER_FOR_HIP", "{0}/bin/clang++".format(spec["llvm-amdgpu"].prefix)
                )
            )
        return args
