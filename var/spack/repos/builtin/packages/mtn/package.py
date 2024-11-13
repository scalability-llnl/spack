# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mtn(MakefilePackage):
    """Movie Thumbnailer is CLI thumbnail generator using FFmpeg."""

    homepage = "https://gitlab.com/movie_thumbnailer/mtn"
    url = "https://gitlab.com/movie_thumbnailer/mtn/-/archive/v3.4.2/mtn-v3.4.2.tar.gz"

    maintainers("ledif")

    license("GPL-2.0-or-later")

    version("3.4.2", sha256="19b2076c00f5b0ad70c2467189b17f335c6e7ece5d1a01ed8910779f6a5ca52a")

    depends_on("c", type="build")  # generated

    depends_on("ffmpeg")
    depends_on("libgd")

    def build(self, spec, prefix):
        src_dir = join_path(self.build_directory, "src")
        with working_dir(src_dir):
            make()

    def install(self, spec, prefix):
        src_dir = join_path(self.build_directory, "src")
        with working_dir(src_dir):
            make(f"PREFIX={prefix}", "install")
