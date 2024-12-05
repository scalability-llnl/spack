# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIdentify(PythonPackage):
    """File identification library for Python.

    Given a file (or some information about a file), return a set of
    standardized tags identifying what the file is."""

    homepage = "https://github.com/pre-commit/identify"
    pypi = "identify/identify-1.4.7.tar.gz"

    license("MIT")

    version("2.5.24", sha256="0aac67d5b4812498056d28a9a512a483f5085cc28640b02b258a59dac34301d4")
    version("2.5.5", sha256="322a5699daecf7c6fd60e68852f36f2ecbb6a36ff6e6e973e0d2bb6fca203ee6")
    version("2.5.3", sha256="887e7b91a1be152b0d46bbf072130235a8117392b9f1828446079a816a05ef44")
    version("1.4.7", sha256="d8919589bd2a5f99c66302fec0ef9027b12ae150b0b0213999ad3f695fc7296e")

    depends_on("py-setuptools", type="build")
