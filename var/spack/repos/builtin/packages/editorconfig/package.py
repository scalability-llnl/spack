# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Editorconfig(CMakePackage):
    """
    EditorConfig helps maintain consistent coding styles for multiple
    developers working on the same project across various editors and IDEs.
    """

    homepage = "https://editorconfig.org/"
    url = "https://github.com/editorconfig/editorconfig-core-c/archive/refs/tags/v0.12.7.tar.gz"

    license("BSD-2-Clause", checked_by="taliaferro")

    version("0.12.7", sha256="f89d2e144fd67bdf0d7acfb2ac7618c6f087e1b3f2c3a707656b4180df422195")

    depends_on("c", type="build")  # generated

    depends_on("pcre2")
