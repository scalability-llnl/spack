# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yq(GoPackage):
    """yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor.
    This is different from the py-yq package that is a wrapper around jq."""

    homepage = "https://mikefarah.gitbook.io/yq"
    url = "https://github.com/mikefarah/yq/archive/refs/tags/v4.45.1.tar.gz"

    maintainers("teaguesterling")

    license("MIT", checked_by="teaguesterling")

    version("4.45.1", sha256="074a21a002c32a1db3850064ad1fc420083d037951c8102adecfea6c5fd96427")
    version("4.44.6", sha256="c0acef928168e5fdb26cd7e8320eddde822f30cf1942817f3f6b854dd721653f")
    version("4.44.5", sha256="1505367f4a6c0c4f3b91c6197ffed4112d29ef97c48d0b5e66530cfa851d3f0e")
    version("4.44.3", sha256="ea950f5622480fc0ff3708c52589426a737cd4ec887a52922a74efa1be8f2fbf")
    version("4.43.1", sha256="e5581d28bae2bcdf70501dfd251233c592eb3e39a210956ee74965b784435d63")
    version("4.41.1", sha256="25d61e72887f57510f88d1a30d515c7e2d79e7c6dce5c96aea7c069fcbc089e7")
    version("4.40.7", sha256="c38024d40ee37d26caba1824965d9ea1d65468f48b2bacd45647ff4f547fa59f")
    version("4.35.2", sha256="8b17d710c56f764e9beff06d7a7b1c77d87c4ba4219ce4ce67e7ee29670f4f13")

    # from go.mod
    depends_on("go@1.21:", type="build", when="@4.40:")
    depends_on("go@1.20:", type="build", when="@4.31:")
