# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class _3dtk(CMakePackage):
    """The 3D Toolkit provides algorithms and methods to process 3D point
    clouds.

    It includes automatic high-accurate registration (6D simultaneous
    localization and mapping, 6D SLAM) and other tools, e.g., a fast 3D viewer,
    plane extraction software, etc. Several file formats for the point clouds
    are natively supported, new formats can be implemented easily."""

    homepage = "https://slam6d.sourceforge.net/"
    # Repo seems to be in the process of switching to git:
    # https://github.com/3DTK/3DTK

    version("trunk", svn="https://svn.code.sf.net/p/slam6d/code/trunk", preferred=True)
    version("1.2", svn="https://svn.code.sf.net/p/slam6d/code/branches/3dtk-release-1.2")

    variant("cgal", default=False, description="Compile with CGAL support")
    variant("opengl", default=True, description="Compile with OpenGL support")
    variant("opencv", default=True, description="Compile with OpenCV support")
    variant(
        "compact_octree", default=False, description="Whether to use the compact octree display"
    )
    variant(
        "cuda",
        default=False,
        description="Whether to build CUDA accelerated collision detection tools",
    )
    variant(
        "openmp",
        default=False,
        description="Whether to use parallel processing capabilities of OPENMP",
    )

    conflicts("~opencv", when="platform=darwin")
    conflicts("+compact_octree", when="~opengl")

    generator("ninja")

    depends_on("cmake@3.5:", when="@trunk", type="build")
    depends_on("cmake@2.6.1:2", when="@1.2", type="build")
    depends_on(
        "boost@:1.75+serialization+graph+regex+filesystem+system+thread+date_time+program_options"
    )
    depends_on("suite-sparse")
    depends_on("zlib-api")
    depends_on("libpng")
    depends_on("eigen")
    depends_on("cgal", when="+cgal")
    depends_on("gl", when="+opengl")
    depends_on("glew", when="+opengl")
    depends_on("freeglut", when="+opengl")
    depends_on(
        "opencv+aruco+calib3d+features2d+ffmpeg+highgui+imgcodecs+imgproc+ml+videoio+flann",
        when="+opencv",
    )
    depends_on("cuda", when="+cuda")

    # TODO: add Spack packages for these instead of using vendored copies
    # depends_on('ann')
    # depends_on('newmat')

    patch("homebrew.patch", when="platform=darwin")

    def setup_build_environment(self, env):
        env.prepend_path("CPATH", self.spec["eigen"].prefix.include)

    def cmake_args(self):
        return [
            self.define_from_variant("WITH_CGAL", "cgal"),
            self.define("WITH_GMP", False),
            self.define("WITH_LIBZIP", False),
            self.define_from_variant("WITH_OPENGL", "opengl"),
            self.define_from_variant("WITH_OPENCV", "opencv"),
            self.define("WITH_QT", False),
            self.define("WITH_GLFW", False),
            self.define("WITH_FTGL", False),
            self.define("WITH_XMLRPC", False),
            self.define("WITH_LIBCONFIG", False),
            self.define("WITH_ROS", False),
            self.define("WITH_PYTHON", False),
            self.define("WITH_WXWIDGETS", False),
            self.define_from_variant("WITH_COMPACT_OCTREE", "compact_octree"),
            self.define("WITH_GLEE", False),
            self.define("WITH_LASLIB", False),
            self.define("WITH_E57", False),
            self.define("WITH_3DMOUSE", False),
            self.define_from_variant("WITH_CUDA", "cuda"),
            self.define("WITH_RIVLIB", False),
            self.define("WITH_MICROEPSILONLIB", False),
            self.define_from_variant("WITH_OPENMP", "openmp"),
            self.define("WITH_METRICS", False),
            self.define("WITH_ADDONS", False),
        ]

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
