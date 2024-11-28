# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Filebench(AutotoolsPackage):
    """
    Filebench is a file system and storage benchmark that can generate a
    large variety of workloads. Unlike typical benchmarks it is extremely
    flexible and allows to specify application's I/O behavior using its
    extensive Workload Model Language (WML). Users can either describe
    desired workloads from scratch or use(with or without modifications)
    workload personalities shipped with Filebench(e.g., mail-, web-, file-,
    and database-server workloads). Filebench is equally good for micro
    and macro-benchmarking, quick to setup, and relatively easy to use.
    """

    homepage = "https://github.com/filebench/filebench"
    url = "https://github.com/filebench/filebench/archive/1.4.9.1.tar.gz"

    license("CDDL-1.0")

    version("1.4.9.1", sha256="77ae91b83c828ded1219550aec74fbbd6975dce02cb5ab13c3b99ac2154e5c2e")
    version("1.4.9", sha256="61b8a838c1450b51a4ce61481a19a1bf0d6e3993180c524ff4051f7c18bd9c6a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
