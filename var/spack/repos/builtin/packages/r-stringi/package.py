# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStringi(RPackage):
    """Allows for fast, correct, consistent, portable, as well as convenient
    character string/text processing in every locale and any native encoding.
    Owing to the use of the ICU library, the package provides R users with
    platform-independent functions known to Java, Perl, Python, PHP, and Ruby
    programmers. Among available features there are: pattern searching (e.g.,
    with ICU Java-like regular expressions or the Unicode Collation Algorithm),
    random string generation, case mapping, string transliteration,
    concatenation, Unicode normalization, date-time formatting and parsing,
    etc."""

    homepage = "http://www.gagolewski.com/software/stringi/"
    url      = "https://cloud.r-project.org/src/contrib/stringi_1.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/stringi"

    version('1.4.3', sha256='13cecb396b700f81af38746e97b550a1d9fda377ca70c78f6cdfc770d33379ed')
    version('1.3.1', sha256='32df663bb6e9527e1ac265eec2116d26f7b7e62ea5ae7cc5de217cbb8defc362')
    version('1.1.5', sha256='651e85fc4ec6cf71ad8a4347f2bd4b00a490cf9eec20921a83bf5222740402f2')
    version('1.1.3', sha256='9ef22062e4be797c1cb6c2c8822ad5c237edb08b0318a96be8bd1930191af389')
    version('1.1.2', sha256='e50b7162ceb7ebae403475f6f8a76a39532a2abc82112db88661f48aa4b9218e')
    version('1.1.1', sha256='243178a138fe68c86384feb85ead8eb605e8230113d638da5650bca01e24e165')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('icu4c@52:')
