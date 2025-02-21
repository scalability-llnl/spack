# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

import spack.deptypes as dt
from spack.package import *
from spack.util.environment import EnvironmentModifications, is_system_path


def use_archive_values(v):
    return v == "<file-uri>" or v.startswith("file://")


class Matlab(Package):
    """MATLAB (MATrix LABoratory) is a multi-paradigm numerical computing
    environment and fourth-generation programming language. A proprietary
    programming language developed by MathWorks, MATLAB allows matrix
    manipulations, plotting of functions and data, implementation of
    algorithms, creation of user interfaces, and interfacing with programs
    written in other languages, including C, C++, C#, Java, Fortran and Python.

    Note: MATLAB is licensed software. You will need to create an account on
    the MathWorks homepage and download MATLAB yourself. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    maintainers("kftse-ust-hk")
    homepage = "https://www.mathworks.com/products/matlab.html"
    manual_download = True
    version(
        "R2024b",
        md5="7edcb80bd5a4a1a586c48056bbb3ee69",
        sha256="ed83bc45f36189f9f645271c44635bfac8e592aa28a2777b55cb210e3f0a92ec",
    )
    version(
        "R2024a",
        md5="174abc8966e11fce8bb030cceac3434d",
        sha256="e07f09ccb6430205b601c298a366ccbede0733a7d44b88a51c51cece946f27a1",
    )
    version(
        "R2023b",
        preferred=True,
        md5="918e10896b6cec0c7940cf6fcdb7ddd8",
        sha256="4964cec46f0f506b077579398d4fad5fd081de556014e3bf5c2622c42ab46ffc",
    )
    version(
        "R2023a",
        md5="56b86eef09f3938e162f67c29e2fbdf9",
        sha256="586dcab53403e08aef6e1abea42fec5fa2a81cd7bd75607641cdad8c57c03259",
    )
    version(
        "R2022b",
        md5="a3328203a7c87dc87c456dbdbf633a0b",
        sha256="f1a6b10f3d2435e301e9fad84df7355dc947b2f99ab2a338fe2144d0228c8dde",
    )
    version(
        "R2022a",
        md5="d4adde66e76e6314e95eb76a4479eb5a",
        sha256="91baa0b652cf1705f264b28c62b06bc2be4fdfa034b941b6de59452d1cb6ee5f",
    )
    version(
        "R2021b",
        md5="47437cc62fb338354aa1cb76416124cb",
        sha256="acf8c4ee617ac513313f764dc70f3fb916d2415972b254e0f463d24d746a71c2",
    )
    version(
        "R2021a",
        md5="28e6be6ca187f8456b4830ba25e8b97d",
        sha256="53250f1e5ad67747fdc005e8494e04863cf133f6de8842c1d051c491dbe3c470",
    )
    version(
        "R2020b",
        md5="34fc14993b6a593ba5bd18ad68fc8939",
        sha256="a30bf88388dc47cced375e646fde0aed9e4df2b59ac6899589728460b1ab6472",
    )
    version(
        "R2020a",
        md5="47cc405f2c10c3ae3f79bb25f4e58b64",
        sha256="d16b0cfd798619d0a05d5443b6679e42dfa08ddd2b493cbb4ce7015ba9bd26b4",
    )
    version(
        "R2019b",
        sha256="d60787263afb810283b7820c4c8d9cb1f854c7cb80f47e136643fd95bf5fbd59",
        md5="ab21180fcbf0c7a64ea50e51e2f740ba",
    )
    version(
        "R2018b",
        sha256="8cfcddd3878d3a69371c4e838773bcabf12aaf0362cc2e1ae7e8820845635cac",
        md5="2dc9e0224a93a99ae6d514d0330c4ec9",
    )
    version("R2016b", sha256="a3121057b1905b132e5741de9f7f8350378592d84c5525faf3ec571620a336f2")
    version("R2015b", sha256="dead402960f4ab8f22debe8b28a402069166cd967d9dcca443f6c2940b00a783")

    variant(
        "mode",
        default="interactive",
        values=("interactive", "silent", "automated"),
        description="Installation mode (interactive, silent, or automated)",
    )
    variant(
        "key", default="<installation-key-here>", description="The file installation key to use"
    )
    variant(
        "build_dependencies",
        default=False,
        description="Build all dependencies for matlab installer / runtime",
    )

    variant(
        "use_archive",
        default="<file-uri>",
        values=use_archive_values,
        description="file:///path/to/archives.tar or compressed tar into archives "
        + "in order to work with offline installs. "
        + "The archive should contain in its root './common' and './glnxa64' folders. "
        + "Defaults to download from MathWorks, does not require an archive file.",
    )

    with when("+build_dependencies"):
        depends_on("atk", type=dt.ALL_TYPES)
        depends_on("at-spi2-core", type=dt.ALL_TYPES)
        depends_on("alsa-lib", type=dt.ALL_TYPES)
        depends_on("gdk-pixbuf", type=dt.ALL_TYPES)
        depends_on("gtkplus", type=dt.ALL_TYPES)
        depends_on("icu4c", type=dt.ALL_TYPES)
        depends_on("java", type=dt.ALL_TYPES)
        depends_on("libffi", type=dt.ALL_TYPES)
        depends_on("libxcomposite", type=dt.ALL_TYPES)
        depends_on("libxdamage", type=dt.ALL_TYPES)
        depends_on("libxrandr", type=dt.ALL_TYPES)
        depends_on("pango", type=dt.ALL_TYPES)
        with when("@R2023:"):
            depends_on("libbsd", type=dt.ALL_TYPES)
            depends_on("libxcb", type=dt.ALL_TYPES)
            depends_on("libxkbcommon", type=dt.ALL_TYPES)
            depends_on("xcb-util", type=dt.ALL_TYPES)
            depends_on("xcb-util-image", type=dt.ALL_TYPES)
            depends_on("xcb-util-keysyms", type=dt.ALL_TYPES)
            depends_on("xcb-util-renderutil", type=dt.ALL_TYPES)
            # depends_on("qt-base+dbus+gui+network+widgets", type=dt.ALL_TYPES)

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["licenses/license.dat"]
    license_vars = ["LM_LICENSE_FILE"]
    license_url = "https://www.mathworks.com/help/install/index.html"

    extendable = True

    def url_for_version(self, version):
        if version >= Version("R2024"):
            return "file://{0}/matlab_{1}_Linux.zip".format(os.getcwd(), version)
        return "file://{0}/matlab_{1}_glnxa64.zip".format(os.getcwd(), version)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        super().setup_run_environment(env)
        if self.spec.satisfies("+build_dependencies"):
            for spec in list(self.spec.traverse(order="topo", deptype=dt.BUILD)):
                if spec.virtual or is_system_path(spec.prefix):
                    continue
                if os.path.isdir(spec.prefix.lib):
                    env.prepend_path("LD_LIBRARY_PATH", spec.prefix.lib)
                if os.path.isdir(spec.prefix.lib64):
                    env.prepend_path("LD_LIBRARY_PATH", spec.prefix.lib64)

    def setup_build_environment(self, env):
        super().setup_run_environment(env)
        if self.spec.satisfies("+build_dependencies"):
            for spec in list(self.spec.traverse(order="topo", deptype=dt.BUILD)):
                if spec.virtual or is_system_path(spec.prefix):
                    continue
                if os.path.isdir(spec.prefix.lib):
                    env.prepend_path("LD_LIBRARY_PATH", spec.prefix.lib)
                if os.path.isdir(spec.prefix.lib64):
                    env.prepend_path("LD_LIBRARY_PATH", spec.prefix.lib64)

    def install(self, spec, prefix):
        config = {
            "destinationFolder": prefix,
            "mode": spec.variants["mode"].value,
            "fileInstallationKey": spec.variants["key"].value,
            "licensePath": self.global_license_file,
            "agreeToLicense": "yes",
        }

        # Store values requested by the installer in a file
        with open("spack_installer_input.txt", "w") as input_file:
            for key in config:
                input_file.write("{0}={1}\n".format(key, config[key]))

        # Run silent installation script
        # Full path required
        input_file = join_path(self.stage.source_path, "spack_installer_input.txt")

        if len(self.spec.variants["use_archive"].value.split("file://")) == 2:
            # Extract the archive
            subprocess.call(
                [
                    "tar",
                    "-C",
                    join_path(self.stage.source_path, "archives"),
                    "-xf",
                    self.spec.variants["use_archive"].value.split("file://")[1],
                ]
            )

        subprocess.call(["./install", "-inputFile", input_file])
