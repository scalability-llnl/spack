# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Boost(Package):
    """Fake boost package."""

    homepage = "http://www.boost.org"
    url = "http://downloads.sourceforge.net/project/boost/boost/1.63.0/boost_1_63_0.tar.bz2"

    version("1.63.0", md5="1c837ecd990bb022d07e7aab32b09847")

    default_install_libs = set(
        [
            "atomic",
            "chrono",
            "date_time",
            "filesystem",
            "graph",
            "iostreams",
            "locale",
            "log",
            "math",
            "program_options",
            "random",
            "regex",
            "serialization",
            "signals",
            "system",
            "test",
            "thread",
            "timer",
            "wave",
        ]
    )

    # mpi/python are not installed by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    default_noinstall_libs = set(["mpi", "python"])

    all_libs = default_install_libs | default_noinstall_libs

    for lib in all_libs:
        variant(
            lib,
            default=(lib not in default_noinstall_libs),
            description="Compile with {0} library".format(lib),
        )

    variant("debug", default=False, description="Switch to the debug version of Boost")
    variant("shared", default=True, description="Additionally build shared libraries")
    variant(
        "multithreaded", default=True, description="Build multi-threaded versions of libraries"
    )
    variant(
        "singlethreaded", default=False, description="Build single-threaded versions of libraries"
    )
    variant("icu", default=False, description="Build with Unicode and ICU suport")
    variant("graph", default=False, description="Build the Boost Graph library")
    variant("taggedlayout", default=False, description="Augment library names with build options")
