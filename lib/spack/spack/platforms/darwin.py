# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform as py_platform

import archspec.cpu

from spack.operating_systems.mac_os import MacOs
from spack.version import Version

from ._platform import Platform


class Darwin(Platform):
    priority = 89

    binary_formats = ["macho"]

    def __init__(self):
        super().__init__("darwin")
        self._add_archspec_targets()

        self.default = archspec.cpu.host().name
        self.front_end = self.default
        self.back_end = self.default

        mac_os = MacOs()

        self.default_os = str(mac_os)
        self.front_os = str(mac_os)
        self.back_os = str(mac_os)

        self.add_operating_system(str(mac_os), mac_os)

    @classmethod
    def detect(cls):
        return "darwin" in py_platform.system().lower()

    def setup_platform_environment(self, pkg, env):
        """Specify deployment target based on target OS version.

        The ``MACOSX_DEPLOYMENT_TARGET`` environment variable provides a
        default ``-mmacosx-version-min`` argument for GCC and Clang compilers,
        as well as the default value of ``CMAKE_OSX_DEPLOYMENT_TARGET`` for
        CMake-based build systems. The default value for the deployment target
        is usually the major version (11, 10.16, ...) for CMake and Clang, but
        some versions of GCC specify a minor component as well (11.3), leading
        to numerous link warnings about inconsistent or incompatible target
        versions. Setting the environment variable ensures consistent versions
        for an install toolchain target, even when the host macOS version
        changes.

        TODO: it may be necessary to add SYSTEM_VERSION_COMPAT for older
        versions of the macosx developer tools; see
        https://github.com/spack/spack/pull/26290 for discussion.
        """

        os = self.operating_sys[pkg.spec.os]
        version = Version(os.version)
        if len(version) == 1:
            # Version has only one component: add a minor version to prevent
            # potential errors with `ld`,
            # which fails with `-macosx_version_min 11`
            # but succeeds with `-macosx_version_min 11.0`.
            # Most compilers seem to perform this translation automatically,
            # but older GCC does not.
            version = str(version) + ".0"
        env.set("MACOSX_DEPLOYMENT_TARGET", str(version))
