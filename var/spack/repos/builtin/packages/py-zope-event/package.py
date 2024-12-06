# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZopeEvent(PythonPackage):
    """Very basic event publishing system."""

    homepage = "https://github.com/zopefoundation/zope.event"
    pypi = "zope.event/zope.event-4.3.0.tar.gz"

    license("ZPL-2.1", checked_by="wdconinc")

    version("5.0", sha256="bac440d8d9891b4068e2b5a2c5e2c9765a9df762944bda6955f96bb9b91e67cd")
    version("4.6", sha256="81d98813046fc86cc4136e3698fee628a3282f9c320db18658c21749235fce80")
    version("4.5.1", sha256="4ab47faac13163ca3c5d6d8a5595212e14770322e95c338d955e3688ba19082a")
    version("4.5.0", sha256="5e76517f5b9b119acf37ca8819781db6c16ea433f7e2062c4afc2b6fbedb1330")
    version("4.3.0", sha256="e0ecea24247a837c71c106b0341a7a997e3653da820d21ef6c08b32548f733e7")

    depends_on("python@3.7:", type=("build", "run"), when="@5:")
    depends_on("py-setuptools", type=("build", "run"))
