# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLockfile(PythonPackage):
    """The lockfile package exports a LockFile class which provides a
    simple API for locking files. Unlike the Windows msvcrt.locking
    function, the fcntl.lockf and flock functions, and the
    deprecated posixfile module, the API is identical across both
    Unix (including Linux and Mac) and Windows platforms. The lock
    mechanism relies on the atomic nature of the link (on Unix) and
    mkdir (on Windows) system calls. An implementation based on
    SQLite is also provided, more as a demonstration of the
    possibilities it provides than as production-quality code.
    """

    pypi = "lockfile/lockfile-0.10.2.tar.gz"
    homepage = "https://launchpad.net/pylockfile"

    license("MIT")

    version("0.12.2", sha256="6aed02de03cba24efabcd600b30540140634fc06cfa603822d508d5361e9f799")
    version("0.10.2", sha256="9e42252f17d1dd89ee31745e0c4fbe58862c25147eb0ef5295c9cd9bcb4ea2c1")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
    depends_on("py-pbr@1.8:", type="build", when="@0.12.2:")
