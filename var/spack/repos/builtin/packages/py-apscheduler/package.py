# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApscheduler(PythonPackage):
    """In-process task scheduler with Cron-like capabilities."""

    homepage = "https://github.com/agronholm/apscheduler"
    pypi = "APScheduler/APScheduler-3.3.1.tar.gz"

    license("MIT")

    version("3.3.1", sha256="f68874dff1bdffcc6ce3adb7840c1e4d162c609a3e3f831351df30b75732767b")
    version("2.1.0", sha256="3b4b44387616902ad6d13122961013630eb25519937e5aa7c450de85656c9753")

    depends_on("py-setuptools@0.7:", type="build")

    depends_on("py-six@1.4.0:", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-tzlocal@1.2:", type=("build", "run"))
