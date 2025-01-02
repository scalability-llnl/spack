# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gopls(GoPackage):
    """The official Go language server developed by the Go team."""

    homepage = "https://golang.org/x/tools/gopls"
    url = "https://github.com/golang/tools/archive/refs/tags/gopls/v0.16.2.tar.gz"

    maintainers("alecbcs")

    license("BSD-3-Clause", checked_by="alecbcs")

    version("0.16.2", sha256="be68b3159fcb8cde9ebb8b468f67f03531c58be2de33edbac69e5599f2d4a2c1")

    build_directory = "gopls"
