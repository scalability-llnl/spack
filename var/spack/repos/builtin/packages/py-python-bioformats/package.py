# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonBioformats(PythonPackage):
    """Python-bioformats is a Python wrapper for Bio-Formats, a standalone
    Java library for reading and writing life sciences image file formats.
    Bio-Formats is capable of parsing both pixels and metadata for
    a large number of formats, as well as writing to several formats."""

    homepage = "https://github.com/CellProfiler/python-bioformats/"
    pypi = "python-bioformats/python-bioformats-4.0.5.tar.gz"

    license("GPL-2.0-only")

    version("4.0.7", sha256="9cdadd06e2453566bfcc512eb9f774654e9fd35ee02a7fb5e8fb097812c5733b")
    version("4.0.5", sha256="f9fa3a2b3c0f1eac6070dff6c513444e9fde9a1f794ec4c21fca85833dbb5192")
    version("4.0.0", sha256="9a952de4d326d961af0a497753a4b71b2f7844605023d170c931d3624e036506")

    depends_on("py-setuptools", type="build")
    depends_on("py-boto3@1.14.23:", type=("build", "run"))
    depends_on("py-future@0.18.2:", type=("build", "run"))
    depends_on("py-python-javabridge@4.0.3", type=("build", "run"))
