# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Goimports(GoPackage):
    """Updates your Go import lines, adding missing ones and removing unreferenced ones."""

    homepage = "https://golang.org/x/tools/cmd/goimports"
    url = "https://github.com/golang/tools/archive/refs/tags/v0.25.0.tar.gz"
    list_url = "https://github.com/golang/tools/tags"

    maintainers("alecbcs")

    license("BSD-3-Clause", checked_by="alecbcs")

    version("0.28.0", sha256="2c0aa55c1748ba406eec2db21bf44ebec62b1d5812b6ba350b5d421af1544adb")
    version("0.25.0", sha256="c536188f5db744371f526f3059960945ed580b3ee60553a4f01956251ab36d20")

    depends_on("go@1.22:", type="build", when="@0.25:")

    build_directory = "cmd/goimports"
