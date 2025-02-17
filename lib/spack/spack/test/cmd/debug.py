# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import spack
import spack.platforms
import spack.spec
from spack.main import SpackCommand

debug = SpackCommand("debug")


def test_report():
    out = debug("report")
    host_platform = spack.platforms.host()
    host_os = host_platform.default_operating_system()
    host_target = host_platform.default_target()
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))

    assert spack.get_version() in out
    assert platform.python_version() in out
    assert str(architecture) in out
