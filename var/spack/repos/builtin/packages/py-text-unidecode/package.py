# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTextUnidecode(PythonPackage):
    """text-unidecode is the most basic port of the Text::Unidecode Perl
    library."""

    homepage = "https://github.com/kmike/text-unidecode/"
    pypi = "text-unidecode/text-unidecode-1.3.tar.gz"

    license("Artistic-1.0-Perl")

    version("1.3", sha256="bad6603bb14d279193107714b288be206cac565dfa49aa5b105294dd5c4aab93")

    depends_on("py-setuptools", type="build")
