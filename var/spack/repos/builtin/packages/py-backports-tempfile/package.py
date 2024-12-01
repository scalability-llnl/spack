# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsTempfile(PythonPackage):
    """This package provides backports of new features in Python's tempfile
    module under the backports namespace
    """

    homepage = "https://github.com/PiDelport/backports.tempfile"
    pypi = "backports.tempfile/backports.tempfile-1.0.tar.gz"

    license("PSF-2.0")

    version("1.0", sha256="1c648c452e8770d759bdc5a5e2431209be70d25484e1be24876cf2168722c762")

    depends_on("py-setuptools", type="build")
    depends_on("py-backports-weakref", type=("build", "run"))
