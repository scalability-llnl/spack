# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladDeprecated(PythonPackage):
    """DataLad extension package for deprecated functionality that was phased
    out in the core package."""

    homepage = "https://github.com/datalad/datalad-deprecated"
    pypi = "datalad_deprecated/datalad_deprecated-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="874cf31c7640a9eafe7c5ecf36f0924d5d5b47222666a55ef10eabb9c29f46cd")

    depends_on("py-setuptools@43:", type="build")

    depends_on("py-datalad@0.18:", type=("build", "run"))
    depends_on("py-jsmin", type=("build", "run"))
    depends_on("py-whoosh", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-mutagen@1.36:", type=("build", "run"))
    depends_on("py-exifread", type=("build", "run"))
    depends_on("py-python-xmp-toolkit", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
