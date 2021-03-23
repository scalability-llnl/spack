# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Dbow2(CMakePackage):
    """DBoW2 is an improved version of the DBow library, an open source C++
    library for indexing and converting images into a bag-of-word
    representation."""

    homepage = "https://github.com/dorian3d/DBoW2"
    git      = "https://github.com/dorian3d/DBoW2.git"

    version('master', branch='master')
    version('shinsumicco', git='https://github.com/shinsumicco/DBoW2.git', branch='master')

    depends_on('cmake@3.0:', type='build')
    depends_on('opencv+calib3d+core+features2d+highgui+imgproc')
    depends_on('boost')
    depends_on('dlib')
    depends_on('eigen', type='link')
