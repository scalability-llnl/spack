# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyUnicodeDisplayWidth(RubyPackage):
    """Determines the monospace display width of a string in Ruby."""

    homepage = "https://github.com/janlelis/unicode-display_width"
    url = "https://github.com/janlelis/unicode-display_width/archive/v1.7.0.tar.gz"

    license("MIT")

    version("1.7.0", sha256="2dd6faa95e022a9f52841d29be6c622c58fff9fb0b84fb2cb30d4f0e13fa8a73")

    depends_on("ruby@1.9.3:", type=("build", "run"))
