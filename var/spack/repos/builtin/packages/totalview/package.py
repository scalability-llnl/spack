# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Totalview(Package):
    """Totalview parallel debugger.

    Select the version associated with your machine architecture'
    '."""

    homepage = "https://totalview.io"
    maintainers("dshrader", "petertea", "suzannepaterno", "elliebinkley")
    license_required = True
    license_comment = "#"
    license_files = ["tv_license/license.lic"]
    license_vars = ["RLM_LICENSE"]

    # As the install of Totalview is via multiple tarballs, the base install
    # will be the documentation.  The architecture-specific tarballs are added
    # as resources dependent on the specific architecture used.

    version(
        "2024.2-x86-64",
        sha256="b6d9cfd804ff1f6641fbd92f9730b34f62062ead9b1324eaf44f34ea78c69ef1",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.2/totalview_2024.2.11_linux_x86-64.tar",
    )

    version(
        "2024.2-powerle",
        sha256="2bc1ef377e95f6f09d1f221a1dcc2f79415bad9e1e8403c647f38e2d383524d6",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.2/totalview_2024.2.11_linux_powerle.tar",
    )

    version(
        "2024.2-linux-arm64",
        sha256="63f737e61c2fb7f4816bcfc1d00e9e7c39817455531abdd09500f953be4ac75d",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.2/totalview_2024.2.11_linux_arm64.tar",
    )

    version(
        "2024.1-x86-64",
        sha256="964b73e70cb9046ce320bb0f95891b05c96a59117e5243fdc269855831c7059b",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.1/totalview_2024.1.21_linux_x86-64.tar",
    )

    version(
        "2024.1-powerle",
        sha256="c4dd8a3099d4f6ed23a6646b1d091129e0bf0b10c7a0d7ec73bd767818bab39b",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.1/totalview_2024.1.21_linux_powerle.tar",
    )

    version(
        "2024.1-linux-arm64",
        sha256="769527478dceb30855413970621f09a9dc54ef863ddaf75bb5a40142a54af346",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.1/totalview_2024.1.21_linux_arm64.tar",
    )

    def setup_run_environment(self, env):
        env.prepend_path(
            "PATH",
            join_path(self.prefix, "toolworks", "totalview.{0}".format(self.version), "bin"),
        )
        env.prepend_path(
            "TVROOT", join_path(self.prefix, "toolworks", "totalview.{0}".format(self.version))
        )
        env.prepend_path("TVDSVRLAUNCHCMD", "ssh")

    def install(self, spec, prefix):
        # Assemble install line
        install_cmd = which("./Install")
        arg_list = ["-agree", "-nosymlink", "-directory", "{0}".format(prefix)]

        # Platform specification.
        if spec.target.family == "x86_64" and spec.platform == "linux":
            arg_list.extend(["-platform", "linux-x86-64"])
        elif spec.target.family == "aarch64":
            arg_list.extend(["-platform", "linux-arm64"])
        elif spec.target.family == "ppc64le":
            arg_list.extend(["-platform", "linux-powerle"])
        else:
            raise InstallError("Architecture {0} not permitted!".format(spec.target.family))

        install_cmd.exe.extend(arg_list)

        # Run install script for totalview (which automatically installs memoryscape)
        install_cmd = which("./Install")
        arg_list.extend(["-install", "totalview"])
        install_cmd.exe.extend(arg_list)
        install_cmd()

        # If a license file was created
        symlink(
            join_path(self.prefix, "tv_license", "license.lic"),
            join_path(self.prefix, "toolworks", "tv_license", "license.lic"),
        )
