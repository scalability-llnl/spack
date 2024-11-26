# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJellyfish(PythonPackage):
    """a library for doing approximate and phonetic matching of strings."""

    pypi = "jellyfish/jellyfish-0.6.1.tar.gz"

    license("MIT")

    version("0.6.1", sha256="5104e45a2b804b48a46a92a5e6d6e86830fe60ae83b1da32c867402c8f4c2094")
    version("0.5.6", sha256="887a9a49d0caee913a883c3e7eb185f6260ebe2137562365be422d1316bd39c9")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
