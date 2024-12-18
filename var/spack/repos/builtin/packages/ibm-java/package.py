# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from llnl.util.symlink import readlink

from spack.package import *


class IbmJava(Package):
    """Binary distribution of the IBM Java Software Development Kit
    for big and little-endian powerpc (power7, 8 and 9).  Note: IBM
    is fairly aggressive about taking down old versions, so old
    (and even current) versions may not be available."""

    homepage = "https://developer.ibm.com/javasdk/"
    maintainers("mwkrentel")

    # Note: IBM is fairly aggressive about taking down old versions,
    # so we may need to update this frequently.  Also, old revs may
    # not be available for download.

    version_list = [
        ("8.0.6.20", "ppc64", "88748d1502a35845b18d514dd76835f0f47270c6ffbd81f67f611e32d042b288"),
        (
            "8.0.6.20",
            "ppc64le",
            "4a7ac4712548d7630f2471a067406c94c3846fff75a0afc660682129dcf80e5b",
        ),
        ("8.0.6.11", "ppc64", "6fd17a6b9a34bb66e0db37f6402dc1b7612d54084c94b859f4a42f445fd174d4"),
        (
            "8.0.6.11",
            "ppc64le",
            "d69ff7519e32e89db88a9a4d4d88d1881524073ac940f35d3860db2c6647be2e",
        ),
        ("8.0.6.10", "ppc64", "ff5151ead88f891624eefe33d80d56c325ca0aa4b93bd96c135cad326993eda2"),
        (
            "8.0.6.10",
            "ppc64le",
            "ea99ab28dd300b08940882d178247e99aafe5a998b1621cf288dfb247394e067",
        ),
        ("8.0.6.7", "ppc64", "a1accb461a039af4587ea86511e317fea1d423e7f781459a17ed3947afed2982"),
        ("8.0.6.7", "ppc64le", "9ede76a597af28c7f10c6f8a68788cc2dcd39fdab178c9bac56df8b3766ac717"),
        ("8.0.6.0", "ppc64", "e142746a83e47ab91d71839d5776f112ed154ae180d0628e3f10886151dad710"),
        ("8.0.6.0", "ppc64le", "18c2eccf99225e6e7643141d8da4110cacc39f2fa00149fc26341d2272cc0102"),
        ("8.0.5.30", "ppc64", "d39ce321bdadd2b2b829637cacf9c1c0d90235a83ff6e7dcfa7078faca2f212f"),
        (
            "8.0.5.30",
            "ppc64le",
            "dec6434d926861366c135aac6234fc28b3e7685917015aa3a3089c06c3b3d8f0",
        ),
    ]

    # There are separate tar files for big and little-endian machine
    # types.  And no, this won't work cross platform.

    for ver, mach, sha in version_list:
        if mach == platform.machine():
            version(ver, sha256=sha, expand=False)

    provides("java@8")

    conflicts("target=x86_64:", msg="ibm-java is only available for ppc64 and ppc64le")
    conflicts("target=aarch64", msg="ibm-java is only available for ppc64 and ppc64le")

    # This assumes version numbers are 4-tuples: 8.0.5.30
    def url_for_version(self, version):
        # Convert 8.0.5.30 to 8.0-5.30 for the file name.
        dash = "{0}.{1}-{2}.{3}".format(*(str(version).split(".")))

        url = (
            "http://public.dhe.ibm.com/ibmdl/export/pub/systems/cloud"
            "/runtimes/java/{0}/linux/{1}/ibm-java-sdk-{2}-{1}"
            "-archive.bin"
        ).format(version, platform.machine(), dash)

        return url

    @property
    def libs(self):
        return find_libraries(["libjvm"], root=self.home, recursive=True)

    def setup_run_environment(self, env):
        env.set("JAVA_HOME", self.home)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("JAVA_HOME", self.home)

    def install(self, spec, prefix):
        archive = os.path.basename(self.stage.archive_file)

        # The archive.bin file is quite fussy and doesn't work as a
        # symlink.
        if os.path.islink(archive):
            targ = readlink(archive)
            os.unlink(archive)
            copy(targ, archive)

        # The properties file is how we avoid an interactive install.
        prop = "properties"
        with open(prop, "w") as file:
            file.write("INSTALLER_UI=silent\n")
            file.write("USER_INSTALL_DIR=%s\n" % prefix)
            file.write("LICENSE_ACCEPTED=TRUE\n")

        # Running the archive file installs everything.
        set_executable(archive)
        inst = Executable(join_path(".", archive))
        inst("-f", prop)

        return
