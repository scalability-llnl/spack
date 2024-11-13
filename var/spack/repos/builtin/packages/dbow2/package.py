# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


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
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("opencv+calib3d+features2d+highgui+imgproc")
    depends_on("dorian3d-dlib")
    depends_on("eigen", type="link")
