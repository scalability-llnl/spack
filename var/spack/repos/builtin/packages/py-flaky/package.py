# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaky(PythonPackage):
    """Flaky is a plugin for nose or pytest that automatically reruns flaky tests."""

    homepage = "https://github.com/box/flaky"
    pypi = "flaky/flaky-3.7.0.tar.gz"

    version("3.7.0", sha256="3ad100780721a1911f57a165809b7ea265a7863305acb66708220820caf8aa0d")

    depends_on("py-setuptools", type=("build"))
