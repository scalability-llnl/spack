# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dbow2(CMakePackage):
    """DBoW2 is an improved version of the DBow library, an open source C++
    library for indexing and converting images into a bag-of-word
    representation."""

    homepage = "https://github.com/dorian3d/DBoW2"
    git = "https://github.com/dorian3d/DBoW2.git"

    version("master", branch="master")
    version("shinsumicco", git="https://github.com/shinsumicco/DBoW2.git", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.0:", type="build")
    depends_on("opencv+calib3d+features2d+highgui+imgproc")
    depends_on("dorian3d-dlib")
    depends_on("eigen", type="link")
