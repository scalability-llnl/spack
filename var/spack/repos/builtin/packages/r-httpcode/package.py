# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHttpcode(RPackage):
    """'HTTP' Status Code Helper.

    Find and explain the meaning of 'HTTP' status codes. Functions included for
    searching for codes by full or partial number, by message, and get
    appropriate dog and cat images for many status codes."""

    cran = "httpcode"

    license("MIT")

    version("0.3.0", sha256="593a030a4f94c3df8c15576837c17344701bac023ae108783d0f06c476062f76")
    version("0.2.0", sha256="fbc1853db742a2cc1df11285cf27ce2ea43bc0ba5f7d393ee96c7e0ee328681a")
