# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re

from spack.package import *


class GitAnnex(Package):
    """
    git-annex allows managing files with git, without checking the file
    contents into git. While that may seem paradoxical, it is useful when
    dealing with files larger than git can currently easily handle, whether
    due to limitations in memory, time, or disk space.
    """

    homepage = "https://git-annex.branchable.com"

    # git-annex is written in Haskell which is currently not supported in
    # spack, thus a similar approach as in the pandoc package was chosen. The
    # following installs the standalone binaries for git-annex.

    # git-annex does not use download links encoding the version but updates
    # the "current" standalone file and keeps track of the version via
    # git-annex itself
    #
    # Steps to find the static link e.g. for amd64:
    # - $ git clone https://downloads.kitenet.net/.git/
    # - $ cd downloads.kitenet.net
    # - $ ls -l git-annex/linux/current/
    #   gives for example for amd64
    #   git-annex-standalone-amd64.tar.gz ->
    #       ../../../.git/annex/objects/KM/Ff/SHA256E-s51276461--a1cef631ef2cc0c977580eacaa1294d7617727df99214920ca6e8f3172bae03e.tar.gz/SHA256E-s51276461--a1cef631ef2cc0c977580eacaa1294d7617727df99214920ca6e8f3172bae03e.tar.gz
    # - exchange "../../../" with "https://downloads.kitenet.net" and you have the link
    # the version to the link can be found in
    # git-annex/linux/current/git-annex-standalone-amd64.tar.gz.info
    # Caution: the version on the webpage
    # (meaning here: https://downloads.kitenet.net/git-annex/linux/current/) is
    # broken and always behind

    # if for some reason the sources vanish from https://downloads.kitenet.net/
    # an alternative source can be found with
    # - $ git annex whereis git-annex/linux/current/git-annex-standalone-arm64.tar.gz
    #     -> gives web url

    skip_version_audit = ["platform=darwin", "platform=windows"]

    license("AGPL-3.0-or-later")

    if platform.system() == "Linux" and platform.machine() == "aarch64":
        # git-annex-standalone-arm64.tar.gz
        version(
            "10.20230408",
            sha256="4efc0636eae3a8e55ccbdd638339b00f39d5691a8f44874dcb0b90ce1425cc47",
            url="https://downloads.kitenet.net/.git/annex/objects/V8/52/SHA256E-s66738845--4efc0636eae3a8e55ccbdd638339b00f39d5691a8f44874dcb0b90ce1425cc47.tar.gz/SHA256E-s66738845--4efc0636eae3a8e55ccbdd638339b00f39d5691a8f44874dcb0b90ce1425cc47.tar.gz",
        )
        # release 10.20220223 was not properly updated for arm64 upstream
        version(
            "10.20220121",
            sha256="3f8a50f61cb092e4e658a320b86ee7bd38238bbd1286fa462bb12797d36e1f25",
            url="https://downloads.kitenet.net/.git/annex/objects/Kp/K5/SHA256E-s55243787--3f8a50f61cb092e4e658a320b86ee7bd38238bbd1286fa462bb12797d36e1f25.tar.gz/SHA256E-s55243787--3f8a50f61cb092e4e658a320b86ee7bd38238bbd1286fa462bb12797d36e1f25.tar.gz",
        )
        # release 8.20210804 was not properly updated for arm64 upstream
        # the sha256sums of 8.20210622 and 8.20210804 were the same
        version(
            "8.20210622",
            sha256="869f875e280db0cc3243d9d0d33492f1c3bc182053544c1d5eb0ec463125fe76",
            # original link is broken
            url="http://archive.org/download/git-annex-builds/SHA256E-s55109776--869f875e280db0cc3243d9d0d33492f1c3bc182053544c1d5eb0ec463125fe76.tar.gz",
        )

    elif platform.system() == "Linux":
        # git-annex-standalone-amd64.tar.gz
        version(
            "10.20230408",
            sha256="5c322c5c5b35e5835bb94c97be143d2717de1e8fb66f7b037720f7dd1d9cc71f",
            url="https://downloads.kitenet.net/.git/annex/objects/79/22/SHA256E-s54263192--5c322c5c5b35e5835bb94c97be143d2717de1e8fb66f7b037720f7dd1d9cc71f.tar.gz/SHA256E-s54263192--5c322c5c5b35e5835bb94c97be143d2717de1e8fb66f7b037720f7dd1d9cc71f.tar.gz",
        )
        version(
            "10.20220223",
            sha256="498a877e040f20e032879d026a78aa86b74f2652774efe3e8b81f054ca1f4485",
            url="http://archive.org/download/git-annex-builds/SHA256E-s52308746--498a877e040f20e032879d026a78aa86b74f2652774efe3e8b81f054ca1f4485.tar.gz",
        )
        version(
            "10.20220121",
            sha256="45cfaddc859d24f7e5e7eb3ab10c14a94d744705d365f26b54a50855ab1068f3",
            url="http://archive.org/download/git-annex-builds/SHA256E-s52034939--45cfaddc859d24f7e5e7eb3ab10c14a94d744705d365f26b54a50855ab1068f3.tar.gz",
        )
        version(
            "8.20210804",
            sha256="f9d4bec06dddaeced25eec5f46360223797363e608fe37cfa93b2481f0166e1f",
            url="http://archive.org/download/git-annex-builds/SHA256E-s51465538--f9d4bec06dddaeced25eec5f46360223797363e608fe37cfa93b2481f0166e1f.tar.gz",
        )
        version(
            "8.20210622",
            sha256="a1cef631ef2cc0c977580eacaa1294d7617727df99214920ca6e8f3172bae03e",
            url="http://archive.org/download/git-annex-builds/SHA256E-s51276461--a1cef631ef2cc0c977580eacaa1294d7617727df99214920ca6e8f3172bae03e.tar.gz",
        )

    variant(
        "standalone", default=False, description="Install git-annex fully standalone incl. git"
    )

    depends_on("git", when="~standalone")

    conflicts("platform=darwin", msg="Darwin is not supported.")
    conflicts("platform=windows", msg="Windows is not supported.")

    executables = ["^git-annex$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"git-annex version: ([0-9.]+)", output)
        if not match:
            return None
        version = match.group(1)
        return version

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)

        if spec.satisfies("~standalone"):
            # use git provided by spack instead of the one in the package
            git_files = ["git", "git-receive-pack", "git-shell", "git-upload-pack"]
            for i in git_files:
                os.remove(join_path(prefix.bin, i))
                os.symlink(join_path(spec["git"].prefix.bin, i), join_path(prefix.bin, i))
