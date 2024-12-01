# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRaven(PythonPackage):
    """Raven is a client for Sentry."""

    homepage = "https://github.com/getsentry/raven-python"
    pypi = "raven/raven-6.10.0.tar.gz"

    license("BSD-3-Clause")

    version("6.10.0", sha256="3fa6de6efa2493a7c827472e984ce9b020797d0da16f1db67197bcc23c8fae54")

    variant("flask", default=False, description="Build flask backend")

    depends_on("py-setuptools", type="build")
    depends_on("py-flask@0.8:", when="+flask", type=("build", "run"))
    depends_on("py-blinker@1.1:", when="+flask", type=("build", "run"))
