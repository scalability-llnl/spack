# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Opencv(CMakePackage, CudaPackage):
    """OpenCV (Open Source Computer Vision Library) is an open source computer
    vision and machine learning software library."""

    homepage = "https://opencv.org/"
    url = "https://github.com/opencv/opencv/archive/4.5.0.tar.gz"
    git = "https://github.com/opencv/opencv.git"
    find_python_hints = False  # opencv uses custom OpenCVDetectPython.cmake

    maintainers("bvanessen", "adamjstewart")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("4.10.0", sha256="b2171af5be6b26f7a06b1229948bbb2bdaa74fcf5cd097e0af6378fce50a6eb9")
    version("4.9.0", sha256="ddf76f9dffd322c7c3cb1f721d0887f62d747b82059342213138dc190f28bc6c")
    version("4.8.1", sha256="62f650467a60a38794d681ae7e66e3e8cfba38f445e0bf87867e2f2cdc8be9d5")
    version("4.8.0", sha256="cbf47ecc336d2bff36b0dcd7d6c179a9bb59e805136af6b9670ca944aef889bd")
    version("4.7.0", sha256="8df0079cdbe179748a18d44731af62a245a45ebf5085223dc03133954c662973")
    version("4.6.0", sha256="1ec1cba65f9f20fe5a41fda1586e01c70ea0c9a6d7b67c9e13edf0cfe2239277")
    version("4.5.5", sha256="a1cfdcf6619387ca9e232687504da996aaa9f7b5689986b8331ec02cb61d28ad")
    version("4.5.4", sha256="c20bb83dd790fc69df9f105477e24267706715a9d3c705ca1e7f613c7b3bad3d")
    version("4.5.2", sha256="ae258ed50aa039279c3d36afdea5c6ecf762515836b27871a8957c610d0424f8")
    version("4.5.1", sha256="e27fe5b168918ab60d58d7ace2bd82dd14a4d0bd1d3ae182952c2113f5637513")
    version("4.5.0", sha256="dde4bf8d6639a5d3fe34d5515eab4a15669ded609a1d622350c7ff20dace1907")
    version("4.2.0", sha256="9ccb2192d7e8c03c58fee07051364d94ed7599363f3b0dce1c5e6cc11c1bb0ec")
    version("4.1.2", sha256="385dd0a9c25e67ef0dd60e022d2a2d7b17e2f36819cf3cb46aa8cdff5c5282c9")
    version("4.1.1", sha256="5de5d96bdfb9dad6e6061d70f47a0a91cee96bb35afb9afb9ecb3d43e243d217")
    version("4.1.0", sha256="8f6e4ab393d81d72caae6e78bd0fd6956117ec9f006fba55fcdb88caf62989b7")
    version("4.0.1", sha256="7b86a0ee804244e0c407321f895b15e4a7162e9c5c0d2efc85f1cadec4011af4")
    version("4.0.0", sha256="3787b3cc7b21bba1441819cb00c636911a846c0392ddf6211d398040a1e4886c")
    version("3.4.12", sha256="c8919dfb5ead6be67534bf794cb0925534311f1cd5c6680f8164ad1813c88d13")
    version("3.4.6", sha256="e7d311ff97f376b8ee85112e2b536dbf4bdf1233673500175ed7cf21a0089f6d")
    version("3.4.5", sha256="0c57d9dd6d30cbffe68a09b03f4bebe773ee44dc8ff5cd6eaeb7f4d5ef3b428e")
    version("3.4.4", sha256="a35b00a71d77b484f73ec485c65fe56c7a6fa48acd5ce55c197aef2e13c78746")
    version("3.4.3", sha256="4eef85759d5450b183459ff216b4c0fa43e87a4f6aa92c8af649f89336f002ec")
    version("3.4.1", sha256="f1b87684d75496a1054405ae3ee0b6573acaf3dad39eaf4f1d66fdd7e03dc852")
    version("3.4.0", sha256="678cc3d2d1b3464b512b084a8cca1fad7de207c7abdf2caa1fed636c13e916da")
    version("3.3.1", sha256="5dca3bb0d661af311e25a72b04a7e4c22c47c1aa86eb73e70063cd378a2aa6ee")
    version("3.3.0", sha256="8bb312b9d9fd17336dc1f8b3ac82f021ca50e2034afc866098866176d985adc6")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    contrib_vers = [
        "3.3.0",
        "3.3.1",
        "3.4.0",
        "3.4.1",
        "3.4.3",
        "3.4.4",
        "3.4.5",
        "3.4.6",
        "3.4.12",
        "4.0.0",
        "4.0.1",
        "4.1.0",
        "4.1.1",
        "4.1.2",
        "4.2.0",
        "4.5.0",
        "4.5.1",
        "4.5.2",
        "4.5.4",
        "4.5.5",
        "4.6.0",
        "4.7.0",
        "4.8.0",
        "4.8.1",
        "4.9.0",
        "4.10.0",
    ]
    for cv in contrib_vers:
        resource(
            name="contrib",
            git="https://github.com/opencv/opencv_contrib.git",
            tag="{0}".format(cv),
            when="@{0} +contrib".format(cv),
        )

    # Patch to fix conflict between CUDA and OpenCV (reproduced with 3.3.0
    # and 3.4.1) header file that have the same name. Problem is fixed in
    # the current development branch of OpenCV. See #8461 for more information.
    patch("dnn_cuda.patch", when="@3.3.0:3.4.1+cuda+dnn")

    patch("opencv3.2_cmake.patch", when="@3.2:3.4.1")

    # do not prepend system paths
    patch("cmake_no-system-paths.patch")

    patch("opencv4.1.1_clp_cmake.patch", when="@4.1.1:")
    patch("opencv4.0.0_clp_cmake.patch", when="@4.0.0:4.1.0")
    patch("opencv3.4.12_clp_cmake.patch", when="@3.4.12")
    patch("opencv3.3_clp_cmake.patch", when="@:3.4.6")

    patch("opencv3.4.4_cvv_cmake.patch", when="@3.4.4:4.5")
    patch("opencv3.3_cvv_cmake.patch", when="@:3.4.3")

    # OpenCV prebuilt apps (variants)
    # Defined in `apps/*/CMakeLists.txt` using
    # `ocv_add_application(...)`
    apps = [
        "annotation",
        "createsamples",
        "interactive-calibration",
        "model-diagnostics",
        "traincascade",
        "version",
        "visualisation",
    ]

    # app variants
    for app in apps:
        variant(app, default=False, description="Install {0} app".format(app))

    # app conflicts
    with when("+annotation"):
        conflicts("~highgui")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~videoio")

    with when("+createsamples"):
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~highgui")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~objdetect")
        conflicts("~videoio")

    with when("+interactive-calibration"):
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~highgui")
        conflicts("~imgproc")
        conflicts("~videoio")

    with when("+model-diagnostics"):
        conflicts("~dnn")

    with when("+traincascade"):
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~highgui")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~objdetect")

    with when("+visualisation"):
        conflicts("~highgui")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~videoio")

    # OpenCV modules (variants)
    # Defined in `modules/*/CMakeLists.txt` using
    # `ocv_add_module(...)` and `ocv_define_module(...)`
    modules = [
        "calib3d",
        "dnn",
        "features2d",
        "flann",
        "gapi",
        "highgui",
        "imgcodecs",
        "imgproc",
        "java",
        "java_bindings_generator",
        "ml",
        "objc",
        "objc_bindings_generator",
        "objdetect",
        "photo",
        "python3",
        "python_bindings_generator",
        "python_tests",
        "stitching",
        "ts",
        "video",
        "videoio",
        "world",
    ]

    # These need additional spack packages
    # js needs Emscripten
    modules_pending = ["js", "js_bindings_generator"]

    # Define the list of libraries objects that may be used
    # to find an external installation and its variants
    libraries = []

    # module variants
    for mod in modules:
        # At least one of these modules must be enabled to build OpenCV
        variant(mod, default=False, description="Include opencv_{0} module".format(mod))
        lib = "libopencv_" + mod
        libraries.append(lib)

    # module conflicts and dependencies
    with when("+calib3d"):
        conflicts("~features2d")
        conflicts("~flann")
        conflicts("~imgproc")

    with when("+dnn"):
        conflicts("~imgproc")
        conflicts("~protobuf")

    with when("+features2d"):
        conflicts("~imgproc")

    with when("+gapi"):
        conflicts("~ade")
        conflicts("~imgproc")

    with when("+highgui"):
        conflicts("~imgcodecs")
        conflicts("~imgproc")

    with when("+imgcodecs"):
        conflicts("~imgproc")

    with when("+java"):
        conflicts("~imgproc")
        conflicts("~java_bindings_generator")
        conflicts("~python3")

    with when("+java_bindings_generator"):
        depends_on("java")
        depends_on("ant")

    with when("+objc"):
        conflicts("~imgproc")
        conflicts("~objc_bindings_generator")

    with when("+objc_bindings_generator"):
        conflicts("~imgproc")

    with when("+objdetect"):
        conflicts("~calib3d")
        conflicts("~dnn")
        conflicts("~imgproc")

    with when("+photo"):
        conflicts("~imgproc")

    with when("+python3"):
        conflicts("~python_bindings_generator")
        depends_on("python@3.2:", type=("build", "link", "run"))
        depends_on("py-setuptools", type="build")
        depends_on("py-numpy", type=("build", "run"))
        # https://github.com/opencv/opencv/issues/25455
        depends_on("py-numpy@:1", when="@:4.9", type=("build", "run"))
        extends("python", when="+python3")

    with when("+stitching"):
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~flann")
        conflicts("~imgproc")

    with when("+ts"):
        conflicts("~highgui")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~videoio")

    with when("+video"):
        conflicts("~imgproc")

    with when("+videoio"):
        conflicts("~ffmpeg")
        conflicts("~imgcodecs")
        conflicts("~imgproc")

    # OpenCV contrib modules (variants)
    contrib_modules = [
        "alphamat",
        "aruco",
        "barcode",
        "bgsegm",
        "bioinspired",
        "ccalib",
        "cudaarithm",
        "cudabgsegm",
        "cudacodec",
        "cudafeatures2d",
        "cudafilters",
        "cudaimgproc",
        "cudalegacy",
        "cudaobjdetect",
        "cudaoptflow",
        "cudastereo",
        "cudawarping",
        "cudev",
        "cvv",
        "datasets",
        "dnn_objdetect",
        "dnn_superres",
        "dpm",
        "face",
        "freetype",
        "fuzzy",
        "hdf",
        "hfs",
        "img_hash",
        "intensity_transform",
        "line_descriptor",
        "matlab",
        "mcc",
        "optflow",
        "phase_unwrapping",
        "plot",
        "quality",
        "rapid",
        "reg",
        "rgbd",
        "saliency",
        "sfm",
        "shape",
        "stereo",
        "structured_light",
        "superres",
        "surface_matching",
        "text",
        "tracking",
        "videostab",
        "viz",
        "wechat_qrcode",
        "xfeatures2d",
        "ximgproc",
        "xobjdetect",
        "xphoto",
    ]

    contrib_modules_pending = [
        "julia",  # need a way to manage the installation prefix
        "ovis",  # need ogre
    ]
    for mod in contrib_modules:
        variant(
            mod,
            default=False,
            description="Include opencv_{0} contrib module".format(mod),
            when="+contrib",
        )

    # contrib module conflicts and dependencies
    with when("+alphamat"):
        conflicts("~eigen")
        conflicts("~imgproc")

    with when("+aruco"):
        conflicts("~calib3d")
        conflicts("~imgproc")

    with when("+barcode"):
        conflicts("~dnn")
        conflicts("~imgproc")

    with when("+bgsegm"):
        conflicts("~calib3d")
        conflicts("~imgproc")
        conflicts("~video")

    with when("+ccalib"):
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~highgui")
        conflicts("~imgproc")

    with when("+cublas"):
        conflicts("~cuda")
        conflicts("~cudev")

    with when("+cuda"):
        conflicts("~cudev")

    with when("+cudaarithm"):
        conflicts("~cuda")
        conflicts("~cublas")
        conflicts("~cudev")
        conflicts("~cufft")

    with when("+cudabgsegm"):
        conflicts("~cuda")
        conflicts("~cudev")
        conflicts("~video")

    with when("+cudacodec"):
        conflicts("~cudev")
        conflicts("~videoio")

    with when("+cudafeatures2d"):
        conflicts("~cuda")
        conflicts("~cudafilters")
        conflicts("~cudawarping")
        conflicts("~cudev")
        conflicts("~features2d")

    with when("+cudafilters"):
        conflicts("~cuda")
        conflicts("~cudaarithm")
        conflicts("~cudev")
        conflicts("~imgproc")

    with when("+cudaimgproc"):
        conflicts("~cuda")
        conflicts("~cudev")
        conflicts("~imgproc")

    with when("+cudalegacy"):
        conflicts("~cuda")
        conflicts("~cudev")
        conflicts("~video")

    with when("+cudaobjdetect"):
        conflicts("~cuda")
        conflicts("~cudaarithm")
        conflicts("~cudawarping")
        conflicts("~cudev")
        conflicts("~objdetect")

    with when("+cudaoptflow"):
        conflicts("~cuda")
        conflicts("~cudaarithm")
        conflicts("~cudaimgproc")
        conflicts("~cudawarping")
        conflicts("~cudev")
        conflicts("~optflow")
        conflicts("~video")

    with when("+cudastereo"):
        conflicts("~calib3d")
        conflicts("~cuda")
        conflicts("~cudev")

    with when("+cudawarping"):
        conflicts("~cuda")
        conflicts("~cudev")
        conflicts("~imgproc")

    with when("+cudev"):
        conflicts("~cuda")

    with when("+cvv"):
        conflicts("~features2d")
        conflicts("~imgproc")
        conflicts("~qt")

    with when("+datasets"):
        conflicts("~flann")
        conflicts("~imgcodecs")
        conflicts("~ml")

    with when("+dnn_objdetect"):
        conflicts("~dnn")
        conflicts("~imgproc")

    with when("+dnn_superres"):
        conflicts("~dnn")
        conflicts("~imgproc")

    with when("+dpm"):
        conflicts("~imgproc")
        conflicts("~objdetect")

    with when("+face"):
        conflicts("~calib3d")
        conflicts("~imgproc")
        conflicts("~objdetect")
        conflicts("~photo")

    with when("+fuzzy"):
        conflicts("~imgproc")

    with when("+freetype"):
        conflicts("~imgproc")
        depends_on("freetype")
        depends_on("harfbuzz")

    with when("+hdf"):
        depends_on("hdf5")
        depends_on("mpi", when="^hdf5+mpi")

    with when("+hfs"):
        with when("+cuda"):
            conflicts("~cudev")
        conflicts("~imgproc")

    with when("+img_hash"):
        conflicts("~imgproc")

    with when("+intensity_transform"):
        conflicts("~imgproc")

    with when("+line_descriptor"):
        conflicts("~imgproc")

    with when("+matlab"):
        conflicts("~python3")
        depends_on("matlab")
        depends_on("py-jinja2")

    with when("+mcc"):
        conflicts("~calib3d")
        conflicts("~dnn")
        conflicts("~imgproc")

    with when("+optflow"):
        conflicts("~calib3d")
        conflicts("~flann")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~video")
        conflicts("~ximgproc")

    with when("+phase_unwrapping"):
        conflicts("~imgproc")

    with when("+plot"):
        conflicts("~imgproc")

    with when("+quality"):
        conflicts("~imgproc")
        conflicts("~ml")

    with when("+rapid"):
        conflicts("~calib3d")
        conflicts("~imgproc")

    with when("+reg"):
        conflicts("~imgproc")

    with when("+rgbd"):
        conflicts("~calib3d")
        conflicts("~eigen")
        conflicts("~imgproc")

    with when("+saliency"):
        conflicts("%intel")
        conflicts("~features2d")
        conflicts("~imgproc")

    with when("+sfm"):
        conflicts("~calib3d")
        conflicts("~eigen")
        conflicts("~features2d")
        conflicts("~imgcodecs")
        conflicts("~xfeatures2d")
        depends_on("ceres-solver")
        depends_on("gflags")
        depends_on("glog")

    with when("+shape"):
        conflicts("~calib3d")
        conflicts("~imgproc")

    with when("+stereo"):
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~imgproc")
        conflicts("~tracking")

    with when("+structured_light"):
        conflicts("~calib3d")
        conflicts("~imgproc")
        conflicts("~phase_unwrapping")

    with when("+superres"):
        with when("+cuda"):
            conflicts("~cudev")
        conflicts("~imgproc")
        conflicts("~optflow")
        conflicts("~video")

    with when("+surface_matching"):
        conflicts("~flann")

    with when("+text"):
        conflicts("~dnn")
        conflicts("~features2d")
        conflicts("~imgproc")
        conflicts("~ml")

    with when("+tracking"):
        conflicts("~imgproc")
        conflicts("~plot")
        conflicts("~video")

    with when("+videostab"):
        with when("+cuda"):
            conflicts("~cudev")
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~imgproc")
        conflicts("~photo")
        conflicts("~video")

    with when("+viz"):
        conflicts("~vtk")

    with when("+wechat_qrcode"):
        conflicts("~dnn")
        conflicts("~imgproc")
        depends_on("iconv")

    with when("+xfeatures2d"):
        with when("+cuda"):
            conflicts("~cudev")
        conflicts("~calib3d")
        conflicts("~features2d")
        conflicts("~imgproc")

    with when("+ximgproc"):
        conflicts("~calib3d")
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~video")

    with when("+xobjdetect"):
        conflicts("~imgcodecs")
        conflicts("~imgproc")
        conflicts("~objdetect")

    with when("+xphoto"):
        conflicts("~imgproc")
        conflicts("~photo")

    # Optional 3rd party components (variants)
    # Defined in `CMakeLists.txt` and `modules/gapi/cmake/init.cmake`
    # using `OCV_OPTION(WITH_* ...)`
    components = [
        "1394",
        "ade",
        "android_mediandk",
        "android_native_camera",
        "avfoundation",
        "cap_ios",
        "carotene",
        "clp",
        "cpufeatures",
        "cublas",
        "cuda",
        "cudnn",
        "cufft",
        "directx",
        "dshow",
        "eigen",
        "ffmpeg",
        "gdal",
        "gtk",
        "hpx",
        "imgcodec_hdr",
        "imgcodec_pfm",
        "imgcodec_pxm",
        "imgcodec_sunraster",
        "ipp",
        "itt",
        "jasper",
        "jpeg",
        "lapack",
        "msmf",
        "msmf_dxva",
        "onnx",
        "opencl",
        "opencl_d3d11_nv",
        "openexr",
        "opengl",
        "openjpeg",
        "openmp",
        "plaidml",
        "png",
        "protobuf",
        "pthreads_pf",
        "qt",
        "quirc",
        "tbb",
        "tengine",
        "tesseract",
        "tiff",
        "v4l",
        "vtk",
        "vulcan",
        "webp",
        "win32ui",
    ]

    # These likely need additional spack packages
    components_pending = [
        "aravis",
        "gdcm",
        "gphoto2",
        "gstreamer",
        "gtk_2_x",  # deprecated in spack
        "halide",
        "inf_engine",
        "librealsense",
        "mfx",
        "ngraph",
        "nvcuvid",  # disabled, details: https://github.com/opencv/opencv/issues/14850
        "nvcuvenc",  # disabled, depends on nvcuvid being enabled
        "opencl_svm",
        "openclamdblas",
        "openclamdfft",
        "openni",
        "openni2",
        "openvx",
        "pvapi",
        "ueye",
        "va",
        "va_intel",
        "ximea",
        "xine",
    ]

    # components and modules with the same name
    # used in `def cmake_args(self)`
    component_and_module = ["freetype", "julia", "matlab"]

    for component in components:
        variant(component, default=False, description="Include {0} support".format(component))

    # Other (variants)
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("powerpc", default=False, description="Enable PowerPC for GCC")
    variant(
        "fast-math",
        default=False,
        description="Enable -ffast-math (not recommended for GCC 4.6.x)",
    )
    variant("nonfree", default=False, description="Enable non-free algorithms")
    variant("contrib", default=True, description="Enable OpenCV contrib modules")

    # Required (dependencies)
    depends_on("cmake@3.5.1:", type="build")
    depends_on("python@2.7:2.8,3.2:", type="build")
    depends_on("java", type="build")
    depends_on("zlib-api")

    # Optional 3rd party components (dependencies)
    depends_on("clp", when="+clp")
    depends_on("cuda@6.5:", when="+cuda")
    depends_on("cuda@:10.2", when="@4.0:4.2+cuda")
    depends_on("cuda@:9.0", when="@3.3.1:3.4+cuda")
    depends_on("cuda@:8", when="@:3.3.0+cuda")
    depends_on("cudnn", when="+cudnn")
    depends_on("cudnn@:7.6", when="@4.0:4.2+cudnn")
    depends_on("cudnn@:7.3", when="@3.3.1:3.4+cudnn")
    depends_on("cudnn@:6", when="@:3.3.0+cudnn")
    depends_on("eigen", when="+eigen")
    depends_on("ffmpeg", when="+ffmpeg")
    depends_on("ffmpeg@:5", when="@:4.7+ffmpeg")
    depends_on("ffmpeg@:4+avresample", when="@:4.6+ffmpeg")
    depends_on("gdal", when="+gdal")
    depends_on("gtkplus", when="+gtk")
    depends_on("hpx", when="+hpx")
    depends_on("ipp", when="+ipp")
    depends_on("jasper", when="+jasper")
    depends_on("jpeg", when="+jpeg")
    depends_on("lapack", when="+lapack")
    depends_on("onnx", when="+onnx")
    depends_on("opencl", when="+opencl")
    depends_on("openexr", when="+openexr")
    depends_on("gl", when="+opengl")
    depends_on("openjpeg@2:", when="+openjpeg")
    depends_on("libpng", when="+png")
    depends_on("protobuf@3.5.0:", when="@3.4.1: +protobuf")
    depends_on("protobuf@3.1.0", when="@3.3.0:3.4.0 +protobuf")
    depends_on("qt@5:", when="+qt")
    depends_on("qt@5:+opengl", when="+qt+opengl")
    depends_on("tbb", when="+tbb")
    depends_on("libtiff+jpeg+libdeflate+lzma+zlib", when="+tiff")
    depends_on("vtk", when="+vtk")
    depends_on("libwebp", when="+webp")
    depends_on("tesseract", when="+tesseract")
    depends_on("leptonica", when="+tesseract")
    depends_on("libdc1394", when="+1394")

    # Optional 3rd party components (conflicts)
    # Defined in `CMakeLists.txt` and `modules/gapi/cmake/init.cmake`
    # using `OCV_OPTION(WITH_* ...)`
    conflicts("+android_mediandk", when="platform=darwin", msg="Android only")
    conflicts("+android_mediandk", when="platform=linux", msg="Android only")
    conflicts("+android_native_camera", when="platform=darwin", msg="Android only")
    conflicts("+android_native_camera", when="platform=linux", msg="Android only")
    conflicts("+avfoundation", when="platform=linux", msg="iOS/macOS only")
    conflicts("+cap_ios", when="platform=darwin", msg="iOS only")
    conflicts("+cap_ios", when="platform=linux", msg="iOS only")
    conflicts("+carotene", when="target=x86:", msg="ARM/AARCH64 only")
    conflicts("+carotene", when="target=x86_64:", msg="ARM/AARCH64 only")
    conflicts("+cpufeatures", when="platform=darwin", msg="Android only")
    conflicts("+cpufeatures", when="platform=linux", msg="Android only")
    conflicts("+cublas", when="~cuda")
    conflicts("+cudnn", when="~cuda")
    conflicts("+cufft", when="~cuda")
    conflicts("+directx", when="platform=darwin", msg="Windows only")
    conflicts("+directx", when="platform=linux", msg="Windows only")
    conflicts("+dshow", when="platform=darwin", msg="Windows only")
    conflicts("+dshow", when="platform=linux", msg="Windows only")
    conflicts("+gtk", when="platform=darwin", msg="Linux only")
    conflicts("+ipp", when="target=aarch64:", msg="x86 or x86_64 only")
    conflicts("+jasper", when="+openjpeg")
    conflicts("+msmf", when="platform=darwin", msg="Windows only")
    conflicts("+msmf", when="platform=linux", msg="Windows only")
    conflicts("+msmf_dxva", when="platform=darwin", msg="Windows only")
    conflicts("+msmf_dxva", when="platform=linux", msg="Windows only")
    conflicts("+opencl_d3d11_nv", when="platform=darwin", msg="Windows only")
    conflicts("+opencl_d3d11_nv", when="platform=linux", msg="Windows only")
    conflicts("+opengl", when="~qt")
    conflicts("+tengine", when="platform=darwin", msg="Linux only")
    conflicts("+tengine", when="target=x86:", msg="ARM/AARCH64 only")
    conflicts("+tengine", when="target=x86_64:", msg="ARM/AARCH64 only")
    conflicts("+v4l", when="platform=darwin", msg="Linux only")
    conflicts("+win32ui", when="platform=darwin", msg="Windows only")
    conflicts("+win32ui", when="platform=linux", msg="Windows only")

    # https://github.com/opencv/opencv/wiki/ChangeLog#version460
    conflicts("%gcc@12:", when="@:4.5")
    conflicts("%clang@15:", when="@:4.5")

    @classmethod
    def determine_version(cls, lib):
        for ext in library_extensions:
            if ext == "dylib":
                # Darwin switches the order of the version compared to Linux
                pattern = re.compile(r"libopencv_(\S*?)\.(\d+\.\d+\.\d+)\.%s" % ext)
            else:
                pattern = re.compile(r"libopencv_(\S*?)\.%s\.(\d+\.\d+\.\d+)" % ext)
            match = pattern.search(lib)
            if match:
                return match.group(2)

    @classmethod
    def determine_variants(cls, libs, version_str):
        variants = []
        remaining_modules = set(cls.modules + cls.contrib_modules)
        contrib_module_set = set(cls.contrib_modules)
        has_contrib = False
        for lib in libs:
            for ext in library_extensions:
                pattern = None
                if ext == "dylib":
                    # Darwin switches the order of the version compared to Linux
                    pattern = re.compile(r"libopencv_(\S*)\.(\d+\.\d+\.\d+)\.%s" % ext)
                else:
                    pattern = re.compile(r"libopencv_(\S*)\.%s\.(\d+\.\d+\.\d+)" % ext)
                match = pattern.search(lib)
                if match:
                    name = match.group(1)
                    if name in contrib_module_set:
                        has_contrib = True
                    if name in remaining_modules:
                        variants.append("+" + name)
                        remaining_modules.remove(name)
        if has_contrib:
            variants.append("+contrib")

        # If libraries are not found, mark those variants as disabled
        for mod in remaining_modules:
            variants.append("~" + mod)

        return " ".join(variants)

    def cmake_args(self):
        spec = self.spec
        args = [self.define("BUILD_opencv_core", "on")]

        if self.spec.satisfies("+contrib"):
            args.append(
                self.define(
                    "OPENCV_EXTRA_MODULES_PATH",
                    join_path(self.stage.source_path, "opencv_contrib", "modules"),
                )
            )

        # OpenCV pre-built apps
        apps_list = []
        for app in self.apps:
            if "+{0}".format(app) in spec:
                apps_list.append(app)
        if apps_list:
            args.append(self.define("BUILD_opencv_apps", "on"))
            args.append(self.define("OPENCV_INSTALL_APPS_LIST", ",".join(apps_list)))
        else:
            args.append(self.define("BUILD_opencv_apps", "off"))

        # OpenCV modules
        for mod in self.modules:
            args.append(self.define_from_variant("BUILD_opencv_" + mod, mod))
            if mod in self.component_and_module:
                args.append(self.define_from_variant("WITH_" + mod.upper(), mod))

        for mod in self.modules_pending:
            args.append(self.define("BUILD_opencv_" + mod, "off"))
            if mod in self.component_and_module:
                args.append(self.define("WITH_" + mod.upper(), "off"))

        # OpenCV contrib modules
        for mod in self.contrib_modules:
            args.append(self.define_from_variant("BUILD_opencv_" + mod, mod))
            if mod in self.component_and_module:
                args.append(self.define_from_variant("WITH_" + mod.upper(), mod))

        for mod in self.contrib_modules_pending:
            args.append(self.define("BUILD_opencv_" + mod, "off"))
            if mod in self.component_and_module:
                args.append(self.define("WITH_" + mod.upper(), "off"))

        # Optional 3rd party components
        for component in self.components:
            args.append(self.define_from_variant("WITH_" + component.upper(), component))
        for component in self.components_pending:
            args.append(self.define("WITH_" + component.upper(), "off"))

        # Other
        args.extend(
            [
                self.define("ENABLE_CONFIG_VERIFICATION", True),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define("ENABLE_PRECOMPILED_HEADERS", False),
                self.define_from_variant("WITH_LAPACK", "lapack"),
                self.define_from_variant("ENABLE_POWERPC", "powerpc"),
                self.define_from_variant("ENABLE_FAST_MATH", "fast-math"),
                self.define_from_variant("OPENCV_ENABLE_NONFREE", "nonfree"),
            ]
        )

        if "+cuda" in spec:
            if spec.variants["cuda_arch"].value[0] != "none":
                cuda_arch = spec.variants["cuda_arch"].value
                args.append(self.define("CUDA_ARCH_BIN", " ".join(cuda_arch)))

        # TODO: this CMake flag is deprecated
        if spec.target.family == "ppc64le":
            args.append(self.define("ENABLE_VSX", True))

        # Media I/O
        zlib = spec["zlib-api"]
        args.extend(
            [
                self.define("BUILD_ZLIB", False),
                self.define("ZLIB_LIBRARY", zlib.libs[0]),
                self.define("ZLIB_INCLUDE_DIR", zlib.headers.directories[0]),
            ]
        )

        if "+png" in spec:
            libpng = spec["libpng"]
            args.extend(
                [
                    self.define("BUILD_PNG", False),
                    self.define("PNG_LIBRARY", libpng.libs[0]),
                    self.define("PNG_INCLUDE_DIR", libpng.headers.directories[0]),
                ]
            )

        if "+jpeg" in spec:
            libjpeg = spec["jpeg"]
            args.extend(
                [
                    self.define("BUILD_JPEG", False),
                    self.define("JPEG_LIBRARY", libjpeg.libs[0]),
                    self.define("JPEG_INCLUDE_DIR", libjpeg.headers.directories[0]),
                ]
            )

        if "+tiff" in spec:
            libtiff = spec["libtiff"]
            args.extend(
                [
                    self.define("BUILD_TIFF", False),
                    self.define("TIFF_LIBRARY", libtiff.libs[0]),
                    self.define("TIFF_INCLUDE_DIR", libtiff.headers.directories[0]),
                ]
            )

        if "+jasper" in spec:
            jasper = spec["jasper"]
            args.extend(
                [
                    self.define("BUILD_JASPER", False),
                    self.define("JASPER_LIBRARY", jasper.libs[0]),
                    self.define("JASPER_INCLUDE_DIR", jasper.headers.directories[0]),
                ]
            )

        if "+clp" in spec:
            clp = spec["clp"]
            args.extend(
                [
                    self.define("BUILD_CLP", False),
                    self.define("CLP_LIBRARIES", clp.prefix.lib),
                    self.define("CLP_INCLUDE_DIR", clp.headers.directories[0]),
                ]
            )

        if "+onnx" in spec:
            onnx = spec["onnx"]
            args.extend(
                [
                    self.define("BUILD_ONNX", False),
                    self.define("ORT_LIB", onnx.libs[0]),
                    self.define("ORT_INCLUDE", onnx.headers.directories[0]),
                ]
            )

        if "+tesseract" in spec:
            tesseract = spec["tesseract"]
            leptonica = spec["leptonica"]
            args.extend(
                [
                    self.define("Lept_LIBRARY", leptonica.libs[0]),
                    self.define("Tesseract_LIBRARY", tesseract.libs[0]),
                    self.define("Tesseract_INCLUDE_DIR", tesseract.headers.directories[0]),
                ]
            )

        # Python
        python_lib = spec["python"].libs[0]
        python_include_dir = spec["python"].headers.directories[0]

        if "+python3" in spec:
            args.extend(
                [
                    self.define("PYTHON3_EXECUTABLE", python.path),
                    self.define("PYTHON3_LIBRARY", python_lib),
                    self.define("PYTHON3_INCLUDE_DIR", python_include_dir),
                    self.define("PYTHON2_EXECUTABLE", ""),
                ]
            )
        else:
            args.extend(
                [self.define("PYTHON2_EXECUTABLE", ""), self.define("PYTHON3_EXECUTABLE", "")]
            )

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libopencv_*", root=self.prefix, shared=shared, recursive=True)
