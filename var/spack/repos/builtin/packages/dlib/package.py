# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Dlib(CMakePackage):
    """DLib is a collection of C++ classes to solve common tasks in C++
    programs, as well as to offer additional functionality to use OpenCV
    data and to solve computer vision problems."""

    homepage = "https://github.com/dorian3d/DLib"
    git      = "https://github.com/dorian3d/DLib.git"

    version('master', branch='master')

    depends_on('cmake@3.0:', type='build')
    depends_on('opencv+calib3d+core+features2d+highgui+imgproc+imgcodecs')
    # Because concretizer is broken...
    # TODO: remove when original concretizer is obsolete
    depends_on('opencv+flann')
