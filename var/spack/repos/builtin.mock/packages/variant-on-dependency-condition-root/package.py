# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VariantOnDependencyConditionRoot(Package):
    """Test that dependencies that are conditional on the state of
    other dependencies are added correctly, for instance:

    depends_on('A')
    depends_on('B', when='^A+x')
    """

    homepage = "https://www.example.org"
    url = "https://example.org/files/v3.4/cmake-3.4.3.tar.gz"

    version("1.0", md5="4cb3ff35b2472aae70f542116d616e63")

    depends_on("variant-on-dependency-condition-a")
    depends_on("variant-on-dependency-condition-b", when="^variant-on-dependency-condition-a+x")
