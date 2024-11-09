# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ConsoleBridge(CMakePackage):
    """console_bridge is a ROS-independent, pure CMake (i.e.
    non-catkin and non-rosbuild package) that provides logging calls
    that mirror those found in rosconsole, but for applications
    that are not necessarily using ROS."""

    homepage = "https://github.com/ros/console_bridge/"
    url = "https://github.com/ros/console_bridge/archive/1.0.1.tar.gz"

    license("BSD-3-Clause")

    version("1.0.2", sha256="303a619c01a9e14a3c82eb9762b8a428ef5311a6d46353872ab9a904358be4a4")
    version("1.0.1", sha256="2ff175a9bb2b1849f12a6bf972ce7e4313d543a2bbc83b60fdae7db6e0ba353f")
    version("1.0.0", sha256="880bbded7fcdc71479e9b1efc3ba5353f08eed23f0009c93d6bea8ba3974d078")
    version("0.5.1", sha256="c4ad60c82cd510d4078273a9e210faed572bef6014322456afd14999d2daf130")
    version("0.5.0", sha256="1cecdf232b1eb883b41cc50d1d38443b2163fdc0497072dc1aa6e7ba30696060")
    version("0.4.4", sha256="1147af6ad6477fcfd640c543684e17ee540e434aa70d6f31c1d137bc86fb937c")
    version("0.4.3", sha256="9f024a38f0947ed9fa67f58829980c2d90d84740e6de20d75cb00866f07a7a0b")

    depends_on("cxx", type="build")  # generated
