# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaconv(PythonPackage):
    """jaconv (Japanese Converter) is interconverter for
    Hiragana, Katakana, Hankaku (half-width character) and
    Zenkaku (full-width character)"""

    homepage = "https://github.com/ikegami-yukino/jaconv"
    pypi = "jaconv/jaconv-0.3.tar.gz"

    license("MIT")

    version("0.3", sha256="cc70c796c19a6765598c03eac59d1399a555a9a8839cc70e540ec26f0ec3e66e")

    depends_on("py-setuptools", type="build")
