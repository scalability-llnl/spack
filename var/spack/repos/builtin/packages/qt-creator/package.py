# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class QtCreator(QMakePackage):
    """The Qt Creator IDE."""

    homepage = "https://www.qt.io/ide/"
    url = "https://download.qt.io/official_releases/qtcreator/4.8/4.8.0/qt-creator-opensource-src-4.8.0.tar.gz"

    list_url = "https://download.qt.io/official_releases/qtcreator/"
    list_depth = 2

    version("5.0.3", sha256="797fe2518b0b9d187b34215a7d08d2911bb0a2fb07b556c6e3762b334d107cc0")
    version("4.8.0", sha256="4c4813454637141a45aa8f18be5733e4ba993335d95940aadf12fda66cf6f849")

    depends_on("qt@5.6.0:+opengl")
    # Qt Creator comes bundled with its own copy of sqlite. Qt has a build
    # dependency on Python, which has a dependency on sqlite. If Python is
    # built with a different version of sqlite than the bundled copy, it will
    # cause symbol conflict. Force Spack to build with the same version of
    # sqlite as the bundled copy.
    # depends_on('sqlite@3.8.10.2', when='@:4.4.0')
    depends_on("sqlite@3.8.10.3:", when="@4.8.0:")

    # Qt Creator 4.3.0+ requires a C++14 compiler
    conflicts("%gcc@:4.8", when="@4.3.0:")

    def url_for_version(self, version):
        url = "https://download.qt.io/official_releases/qtcreator/{0}/{1}/qt-creator-opensource-src-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        env.set("INSTALL_ROOT", self.prefix)

    def qmake_args(self):
        return ["-r"]
