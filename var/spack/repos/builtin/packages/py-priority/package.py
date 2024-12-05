# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPriority(PythonPackage):
    """Priority is a pure-Python implementation of the priority
    logic for HTTP/2, set out in RFC 7540 Section 5.3 (Stream
    Priority). This logic allows for clients to express a
    preference for how the server allocates its (limited)
    resources to the many outstanding HTTP requests that may be
    running over a single HTTP/2 connection."""

    homepage = "https://github.com/python-hyper/priority/"
    pypi = "priority/priority-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="c965d54f1b8d0d0b19479db3924c7c36cf672dbf2aec92d43fbdaf4492ba18c0")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
