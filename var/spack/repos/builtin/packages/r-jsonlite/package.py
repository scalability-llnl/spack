# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJsonlite(RPackage):
    """A Simple and Robust JSON Parser and Generator for R.

    A fast JSON parser and generator optimized for statistical data and the
    web. Started out as a fork of 'RJSONIO', but has been completely rewritten
    in recent versions. The package offers flexible, robust, high performance
    tools for working with JSON in R and is particularly powerful for building
    pipelines and interacting with a web API. The implementation is based on
    the mapping described in the vignette (Ooms, 2014). In addition to
    converting JSON data from/to R objects, 'jsonlite' contains functions to
    stream, validate, and prettify JSON data. The unit tests included with the
    package verify that all edge cases are encoded and decoded consistently for
    use with dynamic data in systems and applications."""

    cran = "jsonlite"

    license("MIT")

    version("1.8.8", sha256="7de21316984c3ba3d7423d12f43d1c30c716007c5e39bf07e11885e0ceb0caa4")
    version("1.8.7", sha256="7d42b7784b72d728698ea02b97818df51e2015ffa39fec2eaa2400771b0f601c")
    version("1.8.5", sha256="dc3cca4bdca1b6d6836c412760ea9656140683126c54cb89c3e42219dec4a3ad")
    version("1.8.4", sha256="79eaabe042226b0918aa828cc63d54fee8be67ae7c67f5e0d3010f468efb1278")
    version("1.8.3", sha256="c57f1daf681fc7d5db893693a65ac61a48ddd7aabf66b28647b0e30df92ac8f0")
    version("1.8.2", sha256="677b645c081a7e004b71f0c48a1d46c1be9715163ccb6b419fbb0342a6c9cc3a")
    version("1.8.0", sha256="7b1892efebcb4cf4628f716000accd4b43bbf82b3e6ba90b9529d4fa0e55cd4c")
    version("1.7.3", sha256="720a0b5e36a5eb71677231442bba2267d077137cfa9e0700585acbee62eac558")
    version("1.7.2", sha256="06354b50435942f67ba264f79831e577809ef89e5f9a5a2201985396fe651fd2")
    version("1.6.1", sha256="74921dd249857a23afabc1ad1485a63a48828e57f240f0619deb04c60f883377")
    version("1.6", sha256="88c5b425229966b7409145a6cabc72db9ed04f8c37ee95901af0146bb285db53")
    version("1.5", sha256="6490371082a387cb1834048ad8cdecacb8b6b6643751b50298c741490c798e02")
    version("1.2", sha256="cb6b4660468d2db84ed09c7b8fefd169fcfc13e1e6b4e7ce64dce2713f34264d")
    version("1.0", sha256="d756dd6367e3fc515c855bb0b34a3a81955f8aeb494db029a893f3cdfcff962d")
    version("0.9.21", sha256="079349342ea6eb92bd5fa8f6a7c08d9e3652c3d41010b64afbc3297671eb3791")

    depends_on("c", type="build")  # generated
