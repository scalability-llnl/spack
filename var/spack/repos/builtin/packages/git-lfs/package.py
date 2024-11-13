# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class GitLfs(MakefilePackage):
    """Git LFS is a system for managing and versioning large files in
    association with a Git repository.  Instead of storing the large files
    within the Git repository as blobs, Git LFS stores special "pointer
    files" in the repository, while storing the actual file contents on a
    Git LFS server."""

    homepage = "https://git-lfs.github.com"
    url = "https://github.com/git-lfs/git-lfs/archive/v2.6.1.tar.gz"

    tags = ["build-tools"]

    executables = ["^git-lfs$"]

    maintainers("sethrj")

    license("MIT")

    version("3.5.1", sha256="d682a12c0bc48d08d28834dd0d575c91d53dd6c6db63c45c2db7c3dd2fb69ea4")
    version("3.4.1", sha256="2a36239d7968ae18e1ba2820dc664c4ef753f10bf424f98bccaf44d527f19a17")
    version("3.3.0", sha256="d5eeb9ee33188d3dd6a391f8a39b96d271f10295129789e5b3a1ac0e9f5114f5")
    version("3.1.2", sha256="5c9bc449068d0104ea124c25f596af16da85e7b5bf256bc544d8ce5f4fe231f2")
    version("2.13.3", sha256="f8bd7a06e61e47417eb54c3a0db809ea864a9322629b5544b78661edab17b950")
    version("2.12.1", sha256="2b2e70f1233f7efe9a010771510391a07527ec7c0af721ecf8edabac5d60f62b")
    version("2.11.0", sha256="8183c4cbef8cf9c2e86b0c0a9822451e2df272f89ceb357c498bfdf0ff1b36c7")
    version("2.10.0", sha256="07fd5c57a1039d5717dc192affbe3268ec2fd03accdca462cb504c0b4194cd23")
    version("2.9.0", sha256="f1963ad88747577ffeeb854649aeacaa741c59be74683da4d46b129a72d111b7")
    version("2.8.0", sha256="10b476bb8862ebceddc6f0a55f5fb63e2c1e5bed6554f6e3b207dd0155a196ad")
    version("2.7.2", sha256="e65659f12ec557ae8c778c01ca62d921413221864b68bd93cfa41399028ae67f")
    version("2.7.1", sha256="af60c2370d135ab13724d302a0b1c226ec9fb0ee6d29ecc335e9add4c86497b4")
    version("2.7.0", sha256="1c829ddd163be2206a44edb366bd7f6d84c5afae3496687405ca9d2a5f3af07b")
    version("2.6.1", sha256="e17cd9d4e66d1116be32f7ddc7e660c7f8fabbf510bc01b01ec15a22dd934ead")

    depends_on("go@1.21:", type="build", when="@3.5:")
    depends_on("go@1.20:", type="build", when="@3.4:")
    depends_on("go@1.19:", type="build", when="@3.3:")
    depends_on("go@1.18:", type="build", when="@3.2:")
    depends_on("go@1.17:", type="build", when="@2.13:")
    depends_on("go@1.5:", type="build", when="@:2.12")
    depends_on("git@1.8.2:", type="run")

    patch("patches/issue-10702.patch", when="@2.7.0:2.7.1")

    # Mysterious syscall failures of old versions on new systems
    conflicts("os=bigsur", when="@:2.11")
    conflicts("os=monterey", when="@:2.11")

    parallel = False

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"git-lfs/(\S+)", output)
        return match.group(1) if match else None

    # Git-lfs does not provide an 'install' target in the Makefile
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path("bin", "git-lfs"), prefix.bin)
