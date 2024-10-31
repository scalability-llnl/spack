# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *
from spack.util.environment import set_env


class SbclBootstrap(Package):
    """Steel Bank Common Lisp (SBCL) is a high performance Common Lisp compiler.
    It is open source / free software, with a permissive license. In addition
    to the compiler and runtime system for ANSI Common Lisp, it provides an
    interactive environment including a debugger, a statistical profiler, a
    code coverage tool, and many other extensions.
    """

    homepage = "https://www.sbcl.org/"

    maintainers("ashermancinelli")

    # sbcl-bootstrap is not available on Windows, but is depended on by sbcl:
    skip_version_audit = ["platform=windows"]

    # NOTE: The sbcl homepage lists
    # while the sourceforge repo lists "Public Domain, MIT License", the
    # COPYING file distributed with the source code contains this message:
    #
    # Thus, there are no known obstacles to copying, using, and modifying
    # SBCL freely, as long as copyright notices of MIT, Symbolics, Xerox and
    # Gerd Moellmann are retained.
    #
    # MIT seems the most appropriate, but if we can add more context to this
    # license message, then we should.
    license("MIT", checked_by="ashermancinelli")

    # By checking objdump -T of the sbcl binary in each prebuilt tarball, I
    # found the latest reference to glibc for each version.
    sbcl_releases = {
        "2.4.0": {
            "darwin": {"arm64": "1d01fac2d9748f769c9246a0a11a2c011d7843337f8f06ca144f5a500e10c117"}
        },
        "2.3.11": {
            "linux": {
                "x86_64": "98784b04f68882b887984242eef73dbb092ec5c778dd536b2c60846715e03f3c",
                "min_glibc": "2.34",
            }
        },
        # TODO(ashermancinelli): I don't have a machine to test this on, but the binaries are
        #                        available.
        # "2.2.9": {
        #     "darwin": {
        #         "x86_64": "0000000000000000000000000000000000000000000000000000000000000000"
        #     }
        # },
        "2.0.11": {
            "linux": {
                "x86_64": "b7e61bc6b8d238f8878e660bc0635e99c2ea1255bfd6153d702fe9a00f8138fd",
                "min_glibc": "2.28",
            }
        },
        "1.4.16": {
            "linux": {
                "x86_64": "df3d905d37656a7eeeba72d703577afc94a21d756a4dde0949310200f82ce575",
                "min_glibc": "2.14",
            }
        },
        "1.4.2": {
            "linux": {
                "aarch64": "ddac6499f36c18ecbce9822a53ef3914c0def5276a457446a456c62999b16d36",
                "min_glibc": "2.17",
            }
        },
        "1.3.21": {
            "linux": {
                "x86_64": "c1c3e17e1857fb1c22af575941be5cd1d5444b462397b1b3c9f3877aee2e814b",
                "min_glibc": "2.3",
            }
        },
    }

    os = platform.system().lower()
    target = platform.machine().lower()

    for ver in sbcl_releases:
        if os in sbcl_releases[ver]:
            if target in sbcl_releases[ver][os]:
                version(ver, sha256=sbcl_releases[ver][os][target])
                if "min_glibc" in sbcl_releases[ver][os]:
                    conflicts(
                        "glibc@:{0}".format(sbcl_releases[ver][os]["min_glibc"]),
                        when="@{0}".format(ver),
                    )

    supported_sysinfo_msg = (
        "Not a supported platform. See https://www.sbcl.org/platform-table.html"
    )
    for sysinfo in ["platform=windows", "target=ppc64le"]:
        conflicts(sysinfo, msg=supported_sysinfo_msg)

    def url_for_version(self, version):
        target = platform.machine().lower()
        os = platform.system().lower()
        sbcl_targets = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x86-64"}
        if target not in sbcl_targets:
            return None
        sbcl_url = "https://sourceforge.net/projects/sbcl/files/sbcl/{version}/sbcl-{version}-{target}-{os}-binary.tar.bz2"
        return sbcl_url.format(version=version, target=sbcl_targets[target], os=os)

    def install(self, spec, prefix):
        sh = which("sh")
        with set_env(INSTALL_ROOT=self.spec.prefix):
            sh("install.sh")
