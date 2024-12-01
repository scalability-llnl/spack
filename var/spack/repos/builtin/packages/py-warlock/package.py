# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWarlock(PythonPackage):
    """Self-validating Python objects using JSON schema"""

    homepage = "https://github.com/bcwaldon/warlock"
    url = "https://github.com/bcwaldon/warlock/archive/1.3.3.tar.gz"

    license("Apache-2.0")

    version("1.3.3", sha256="b77e4977d5dc54d47f88cbcc9ab2d716f5f10171d123138785dad96aeb2858d0")

    depends_on("py-setuptools", type="build")
    depends_on("py-jsonschema@0.7:3", type=("build", "run"))
    depends_on("py-jsonpatch@0.10:1", type=("build", "run"))
    depends_on("py-six@1:", type=("build", "run"))
