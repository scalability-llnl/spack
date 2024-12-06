# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os.path

from spack.package import *


class Express(CMakePackage):
    """eXpress is a streaming tool for quantifying the abundances of a set of
    target sequences from sampled subsequences."""

    homepage = "http://bio.math.berkeley.edu/eXpress/"
    url = "https://github.com/adarob/eXpress/archive/1.5.2.zip"

    license("Artistic-2.0")

    # 1.5.1 used to be known as 2015-11-29 (same commit), but they've
    # added tags, so lets use 'em
    version("1.5.3", sha256="dfea819bbe7187a06462d6549a13f9cad7f3f128cb5c62bd90946f972c45a1f2")
    version("1.5.2", sha256="25a63cca3dac6bd0daf04d2f0b2275e47d2190c90522bd231b1d7a875a59a52e")
    version("1.5.1", sha256="fa3522de9cc25f1ede22fa196928912a6da2a2038681911115ec3e4da3d61293")

    depends_on(
        "boost"
        "+date_time+exception+filesystem+system+chrono"
        "+atomic+container+math+thread+program_options"
    )
    depends_on("bamtools")
    depends_on("zlib-api")

    # patch from the debian package repo:
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=811859
    patch("gcc-6.patch", when="@:1.5.2%gcc@6.0.0:")
    patch("gcc-6.patch", when="@:1.5.2%fj")

    def patch(self):
        with working_dir("src"):
            files = glob.iglob("*.*")
            for file in files:
                if os.path.isfile(file):
                    edit = FileFilter(file)
                    edit.filter(
                        "#include <api",
                        "#include <%s" % self.spec["bamtools"].prefix.include.bamtools.api,
                    )
            edit = FileFilter("CMakeLists.txt")
            edit.filter(
                r"\${CMAKE_CURRENT_SOURCE_DIR}/../bamtools/lib/" "libbamtools.a",
                "%s" % self.spec["bamtools"].libs,
            )

    def setup_build_environment(self, env):
        env.prepend_path("CPATH", self.spec["bamtools"].prefix.include.bamtools)
