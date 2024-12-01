# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform as py_platform
import re

import llnl.util.lang

from spack.util.executable import Executable
from spack.version import Version

from ._operating_system import OperatingSystem


@llnl.util.lang.memoized
def macos_version():
    """Get the current macOS version as a version object.

    This has three mechanisms for determining the macOS version, which is used
    for spack identification (the ``os`` in the spec's ``arch``) and indirectly
    for setting the value of ``MACOSX_DEPLOYMENT_TARGET``, which affects the
    ``minos`` value of the ``LC_BUILD_VERSION`` macho header. Mixing ``minos``
    values can lead to lots of linker warnings, and using a consistent version
    (pinned to the major OS version) allows distribution across clients that
    might be slightly behind.

    The version determination is made with three mechanisms in decreasing
    priority:

    1. The ``MACOSX_DEPLOYMENT_TARGET`` variable overrides the actual operating
       system version, just like the value can be used to build for older macOS
       targets on newer systems. Spack currently will truncate this value when
       building packages, but at least the major version will be the same.

    2. The system ``sw_vers`` command reports the actual operating system
       version.

    3. The Python ``platform.mac_ver`` function is a fallback if the operating
       system identification fails, because some Python versions and/or
       installations report the OS
       on which Python was *built* rather than the one on which it is running.
    """
    env_ver = os.environ.get("MACOSX_DEPLOYMENT_TARGET", None)
    if env_ver:
        return Version(env_ver)

    try:
        output = Executable("sw_vers")(output=str, fail_on_error=False)
    except Exception:
        # FileNotFoundError, or spack.util.executable.ProcessError
        pass
    else:
        match = re.search(r"ProductVersion:\s*([0-9.]+)", output)
        if match:
            return Version(match.group(1))

    # Fall back to python-reported version, which can be inaccurate around
    # macOS 11 (e.g. showing 10.16 for macOS 12)
    return Version(py_platform.mac_ver()[0])


@llnl.util.lang.memoized
def macos_cltools_version():
    """Find the last installed version of the CommandLineTools.

    The CLT version might only affect the build if it's selected as the macOS
    SDK path.
    """
    pkgutil = Executable("pkgutil")
    output = pkgutil(
        "--pkg-info=com.apple.pkg.cltools_executables", output=str, fail_on_error=False
    )
    match = re.search(r"version:\s*([0-9.]+)", output)
    if match:
        return Version(match.group(1))

    # No CLTools installed by package manager: try Xcode
    output = pkgutil("--pkg-info=com.apple.pkg.Xcode", output=str, fail_on_error=False)
    match = re.search(r"version:\s*([0-9.]+)", output)
    if match:
        return Version(match.group(1))

    return None


@llnl.util.lang.memoized
def macos_sdk_path():
    """Return path to the active macOS SDK."""
    xcrun = Executable("xcrun")
    return xcrun("--show-sdk-path", output=str).rstrip()


def macos_sdk_version():
    """Return the version of the active macOS SDK.

    The SDK version usually corresponds to the installed Xcode version and can
    affect how some packages (especially those that use the GUI) can fail. This
    information should somehow be embedded into the future "compilers are
    dependencies" feature.

    The macOS deployment target cannot be greater than the SDK version, but
    usually it can be at least a few versions less.
    """
    xcrun = Executable("xcrun")
    return Version(xcrun("--show-sdk-version", output=str).rstrip())


class MacOs(OperatingSystem):
    """This class represents the macOS operating system. This will be
    auto detected using the python platform.mac_ver. The macOS
    platform will be represented using the major version operating
    system name, i.e el capitan, yosemite...etc.
    """

    def __init__(self):
        """Autodetects the mac version from a dictionary.

        If the mac version is too old or too new for Spack to recognize,
        will use a generic "macos" version string until Spack is updated.
        """
        mac_releases = {
            "10.0": "cheetah",
            "10.1": "puma",
            "10.2": "jaguar",
            "10.3": "panther",
            "10.4": "tiger",
            "10.5": "leopard",
            "10.6": "snowleopard",
            "10.7": "lion",
            "10.8": "mountainlion",
            "10.9": "mavericks",
            "10.10": "yosemite",
            "10.11": "elcapitan",
            "10.12": "sierra",
            "10.13": "highsierra",
            "10.14": "mojave",
            "10.15": "catalina",
            "10.16": "bigsur",
            "11": "bigsur",
            "12": "monterey",
            "13": "ventura",
            "14": "sonoma",
            "15": "sequoia",
        }

        version = macos_version()

        # Big Sur versions go 11.0, 11.0.1, 11.1 (vs. prior versions that
        # only used the minor component)
        part = 1 if version >= Version("11") else 2

        mac_ver = str(version.up_to(part))
        name = mac_releases.get(mac_ver, "macos")
        super().__init__(name, mac_ver)

    def __str__(self):
        return self.name
