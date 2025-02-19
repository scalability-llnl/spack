# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRomanNumeralsPy(PythonPackage):
    """Manipulate well-formed Roman numerals."""

    homepage = "https://github.com/AA-Turner/roman-numerals"
    pypi = "roman_numerals_py/roman_numerals_py-3.0.0.tar.gz"

    license("0BSD OR CC0-1.0")

    version("3.0.0", sha256="91199c4373658c03d87d9fe004f4a5120a20f6cb192be745c2377cce274ef41c")

    depends_on("py-flit-core@3.7:3", type="build")
