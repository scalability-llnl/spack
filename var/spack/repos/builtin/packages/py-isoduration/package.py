# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsoduration(PythonPackage):
    """Operations with ISO 8601 durations."""

    homepage = "https://github.com/bolsote/isoduration"
    pypi = "isoduration/isoduration-20.11.0.tar.gz"

    license("0BSD")

    version("20.11.0", sha256="ac2f9015137935279eac671f94f89eb00584f940f5dc49462a0c4ee692ba1bd9")

    depends_on("py-setuptools", type="build")

    depends_on("py-arrow@0.15.0:", type=("build", "run"))
