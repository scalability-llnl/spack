# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPythonDateutil(PythonPackage):
    """Typing stubs for python-dateutil."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-python-dateutil/types-python-dateutil-2.8.19.tar.gz"

    version("2.8.19.14", sha256="1f4f10ac98bb8b16ade9dbee3518d9ace017821d94b057a425b069f834737f4b")
    version("2.8.19", sha256="bfd3eb39c7253aea4ba23b10f69b017d30b013662bb4be4ab48b20bbd763f309")

    depends_on("py-setuptools", type="build")
