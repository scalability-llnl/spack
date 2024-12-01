# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TrivialPkgWithValidHash(Package):
    url = "http://www.unit-test-should-replace-this-url/trivial_install-1.0"

    version(
        "1.0",
        sha256="6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72",
        expand=False,
    )

    hashed_content = "test content"

    def install(self, spec, prefix):
        pass
