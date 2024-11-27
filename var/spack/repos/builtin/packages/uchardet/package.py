# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Uchardet(CMakePackage):
    """uchardet is an encoding detector library, which takes a sequence of
    bytes in an unknown character encoding without any additional information,
    and attempts to determine the encoding of the text. Returned encoding names
    are iconv-compatible."""

    homepage = "https://www.freedesktop.org/wiki/Software/uchardet/"
    url = "https://www.freedesktop.org/software/uchardet/releases/uchardet-0.0.6.tar.xz"
    git = "https://gitlab.freedesktop.org/uchardet/uchardet.git"

    license("MPL-1.1")

    version("master", branch="master")
    version("0.0.8", sha256="8351328cdfbcb2432e63938721dd781eb8c11ebc56e3a89d0f84576b96002c61")
    version("0.0.7", sha256="8351328cdfbcb2432e63938721dd781eb8c11ebc56e3a89d0f84576b96002c61")
    version("0.0.6", sha256="8351328cdfbcb2432e63938721dd781eb8c11ebc56e3a89d0f84576b96002c61")
    version("0.0.5", sha256="7c5569c8ee1a129959347f5340655897e6a8f81ec3344de0012a243f868eabd1")
    version("0.0.4", sha256="9dbe41fc73ba6a70676c04b1f0dd812914c0bbb65940283f2d54c5a2338a2acd")
    version("0.0.3", sha256="8caba57524b6e306e764b4dabf5bfec48b6f9d89b73543ed7c95263890e2006f")
    version("0.0.2", sha256="eb59b5b36269212a0d5f44d654cdbeb02e4e43ff59e3ce0205d6a64670991e83")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version >= Version("0.0.6"):
            url = "https://www.freedesktop.org/software/uchardet/releases/uchardet-0.0.6.tar.xz"
        else:
            url = "https://github.com/BYVoid/uchardet/archive/v0.0.5.tar.gz"
        return url

    def cmake_args(self):
        args = []
        if self.spec.satisfies("platform=darwin"):
            args += [
                # From https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/uchardet.rb
                self.define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib),
                # From https://github.com/mutationpp/Mutationpp/issues/26
                self.define("CMAKE_MACOSX_RPATH", "ON"),
            ]
        return args
