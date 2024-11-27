# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXenv(PythonPackage):
    """Helpers to work with the environment in a platform independent way."""

    homepage = "https://gitlab.cern.ch/gaudi/xenv"
    pypi = "xenv/xenv-1.0.0.tar.gz"
    git = "https://gitlab.cern.ch/gaudi/xenv.git"

    license("GPL-3.0-or-later")

    version("develop", branch="master")
    version("1.0.0", sha256="cea9547295f0bd07c87e68353bb9eb1c2f2d1c09a840e3196c19cbc807ee4558")

    depends_on("py-setuptools", type=("build", "run"))
