# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Srcml(CMakePackage):
    """srcML is an XML format for source code. The XML markup identifies elements of
    the abstract syntax of the source-code language. The toolkit includes parsing
    supports conversion of C, C++, C#, and Java both to and from the srcML format.
    The format allows leveraging XML tools to support the various tasks of source
    code exploration, analysis, and manipulation."""

    homepage = "https://github.com/srcML/srcML"
    url = "https://github.com/srcML/srcML/archive/refs/tags/v1.0.0.tar.gz"

    maintainers("meyersbs")

    license("GPL-3.0-or-later")

    version("1.0.0", sha256="3ddf33271c3b3953d5e3ecbb14c4f925fc0e609a81250d921d3516537dcffae2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.14:", type="build")
    depends_on("antlr+cxx+java+pic")
    depends_on("libxslt")
    depends_on("libarchive@3:")
    depends_on("curl")
    depends_on("boost@:1.78.0")

    patch(
        "https://patch-diff.githubusercontent.com/raw/srcML/srcML/pull/1829.patch?full_index=1",
        sha256="384068e00a01809cdc9b6eca79fd6833bf3214d4b9ac1765b52bc374a7af333e",
    )

    def patch(self):
        filter_file(r"add_subdirectory\(package\)", "#noop", "CMakeLists.txt")
