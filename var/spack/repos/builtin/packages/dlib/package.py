# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Dlib(CMakePackage, CudaPackage):
    """toolkit containing machine learning algorithms and tools
    for creating complex software in C++ to solve real world problems"""

    homepage = "http://dlib.net/"
    url = "https://github.com/davisking/dlib/archive/v19.19.tar.gz"
    git = "https://github.com/davisking/dlib"

    maintainers("robertu94")

    license("BSL-1.0")

    version("master", branch="master")
    version("19.24.4", sha256="d881911d68972d11563bb9db692b8fcea0ac1b3fd2e3f03fa0b94fde6c739e43")
    version("19.22", sha256="5f44b67f762691b92f3e41dcf9c95dd0f4525b59cacb478094e511fdacb5c096")
    version("19.21", sha256="116f52e58be04b47dab52057eaad4b5c4d5c3032d927fe23d55b0741fc4107a0")
    version("19.20", sha256="fc3f0986350e8e53aceadf95a71d2f413f1eedc469abda99a462cb528741d411")
    version("19.19", sha256="7af455bb422d3ae5ef369c51ee64e98fa68c39435b0fa23be2e5d593a3d45b87")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("ffmpeg", default=False, description="build ffmpeg image support")
    variant("gif", default=False, description="build gif image support")
    variant("gui", default=False, description="build dlib graphical support")
    variant("jpeg", default=False, description="build jpeg image support")
    variant("jxl", default=False, description="build jxl image support")
    variant("png", default=False, description="build png image support")
    variant("shared", default=True, description="build the shared libraries")
    variant("sqlite", default=False, description="build sqlite3 support")
    variant("webp", default=False, description="build webp image support")
    variant("blas", default=True, description="build blas image support")
    variant("lapack", default=True, description="build lapack image support")

    depends_on("zlib-api")
    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("libjxl@0.10.2:", when="+jxl")
    depends_on("giflib", when="+gif")
    depends_on("libpng", when="+png")
    depends_on("libwebp", when="+webp")
    depends_on("libjpeg", when="+jpeg")
    depends_on("sqlite", when="+sqlite")
    depends_on("blas", when="+blas")
    depends_on("lapack", when="+lapack")
    depends_on("libsm", when="+gui")
    depends_on("libx11", when="+gui")
    depends_on("cuda@7.5:", when="+cuda")
    depends_on("cudnn", when="+cuda")
    # depends on the deprecated FindCUDA module dependency as of 19.24.4
    # when cuda is enabled
    depends_on("cmake@:3.26", when="+cuda")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("DLIB_USE_BLAS", "blas"),
            self.define_from_variant("DLIB_USE_LAPACK", "lapack"),
            self.define_from_variant("DLIB_USE_FFMPEG", "ffmpeg"),
            self.define_from_variant("DLIB_GIF_SUPPORT", "gif"),
            self.define("DLIB_NO_GUI_SUPPORT", spec.satisfies("~gui")),
            self.define_from_variant("DLIB_JPEG_SUPPORT", "jpeg"),
            self.define_from_variant("DLIB_JXL_SUPPORT", "jxl"),
            self.define_from_variant("DLIB_PNG_SUPPORT", "png"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("DLIB_LINK_WITH_SQLITE3", "sqlite"),
            self.define_from_variant("DLIB_WEBP_SUPPORT", "webp"),
            self.define_from_variant("DLIB_USE_CUDA", "cuda"),
        ]
        if spec.satisfies("+cuda"):
            args.append(
                self.define(
                    "DLIB_USE_CUDA_COMPUTE_CAPABILITIES", self.spec.variants["cuda_arch"].value
                )
            )

        return args
