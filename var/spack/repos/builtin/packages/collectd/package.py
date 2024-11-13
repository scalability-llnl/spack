# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Collectd(AutotoolsPackage):
    """The system statistics collection daemon."""

    homepage = "https://collectd.org/"
    url = "https://github.com/collectd/collectd/releases/download/collectd-5.11.0/collectd-5.11.0.tar.bz2"

    license("GPL-2.0-or-later")

    version("5.12.0", sha256="5bae043042c19c31f77eb8464e56a01a5454e0b39fa07cf7ad0f1bfc9c3a09d6")
    version("5.11.0", sha256="37b10a806e34aa8570c1cafa6006c604796fae13cc2e1b3e630d33dcba9e5db2")
    version("5.10.0", sha256="a03359f563023e744c2dc743008a00a848f4cd506e072621d86b6d8313c0375b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("valgrind", type="test")
