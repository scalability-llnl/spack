# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCaliperReader(PythonPackage):
    """A Python library for reading Caliper .cali files."""

    homepage = "https://github.com/LLNL/Caliper"
    pypi = "caliper-reader/caliper-reader-0.4.0.tar.gz"

    license("BSD-3-Clause")

    version("0.4.0", sha256="00c2c0165a0665dbae58579a1477cb785b3f11350f060e95a6e5ce42f02d5c37")

    depends_on("py-setuptools", type="build")
