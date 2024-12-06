# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.lang

import spack.util.spack_yaml as syaml


@llnl.util.lang.lazy_lexicographic_ordering
class OperatingSystem:
    """Base class for all the Operating Systems.

    On a multiple architecture machine, the architecture spec field can be set to
    build a package against any target and operating system that is present on the
    platform. On Cray platforms or any other architecture that has different front
    and back end environments, the operating system will determine the method of
    compiler detection.

    There are two different types of compiler detection:

        1. Through the $PATH env variable (front-end detection)
        2. Through the module system. (back-end detection)

    Depending on which operating system is specified, the compiler will be detected
    using one of those methods.

    For platforms such as linux and darwin, the operating system is autodetected.
    """

    def __init__(self, name, version):
        self.name = name.replace("-", "_")
        self.version = str(version).replace("-", "_")

    def __str__(self):
        return "%s%s" % (self.name, self.version)

    def __repr__(self):
        return self.__str__()

    def _cmp_iter(self):
        yield self.name
        yield self.version

    def to_dict(self):
        return syaml.syaml_dict([("name", self.name), ("version", self.version)])
