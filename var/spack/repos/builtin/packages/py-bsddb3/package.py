# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBsddb3(PythonPackage):
    """This module provides a nearly complete wrapping of the Oracle/Sleepycat
    C API for the Database Environment, Database, Cursor, Log Cursor,
    Sequence and Transaction objects, and each of these is exposed
    as a Python type in the bsddb3.db module."""

    pypi = "bsddb3/bsddb3-6.2.5.tar.gz"

    license("BSD-3-Clause")

    version("6.2.5", sha256="784bf40ad935258507594a89b32ea11f362cde120751c8b96de163955ced7db8")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6:")
    depends_on("py-setuptools", type="build")
    depends_on("berkeley-db")

    # For testing... see here for an example that uses BerkeleyDB
    # https://code.activestate.com/recipes/189060-using-berkeley-db-database/
