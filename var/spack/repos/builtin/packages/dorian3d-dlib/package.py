# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Dorian3dDlib(CMakePackage):
    """DLib is a collection of C++ classes to solve common tasks in C++
    programs, as well as to offer additional functionality to use OpenCV
    data and to solve computer vision problems."""

    homepage = "https://github.com/dorian3d/DLib"
    git = "https://github.com/dorian3d/DLib.git"

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.0:", type="build")
    depends_on("opencv+calib3d+features2d+highgui+imgproc+imgcodecs+flann")
