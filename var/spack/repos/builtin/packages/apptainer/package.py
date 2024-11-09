# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from glob import glob
from os.path import basename

from spack.package import *
from spack.pkg.builtin.singularityce import SingularityBase


# Apptainer is the new name of Singularity, piggy-back on the original package
class Apptainer(SingularityBase):
    """Apptainer is an open source container platform designed to be simple, fast, and
    secure. Many container platforms are available, but Apptainer is designed for
    ease-of-use on shared systems and in high performance computing (HPC)
    environments.

    Needs post-install chmod/chown steps to enable full functionality.
    See package definition or `spack-build-out.txt` build log for details,
    e.g.:

        tail -15 $(spack location -i apptainer)/.spack/spack-build-out.txt
    """

    homepage = "https://apptainer.org"
    url = "https://github.com/apptainer/apptainer/releases/download/v1.0.2/apptainer-1.0.2.tar.gz"
    git = "https://github.com/apptainer/apptainer.git"

    license(
        "BSD-3-Clause AND BSD-3-Clause-LBNL"
        " AND BSD-2-Clause AND Apache-2.0 AND MIT AND MPL-2.0 AND Unlicense",
        checked_by="tgamblin",
    )

    version("main", branch="main")
    version("1.3.4", sha256="c6ccfdd7c967e5c36dde8711f369c4ac669a16632b79fa0dcaf7e772b7a47397")
    version("1.3.3", sha256="94a274ab4898cdb131f4e3867c4e15f7e16bc2823303d2afcbafee0242f0838d")
    version("1.3.2", sha256="483910727e1a15843b93d9f2db1fc87e27804de9c74da13cc32cd4bd0d35e079")
    # version "1.3.1" has security vulnerability CVE-2024-3727
    # see also https://github.com/advisories/GHSA-6wvf-f2vw-3425
    version("1.2.5", sha256="606b67ef97683e1420401718687d258b1034fdf2edae72eeacd0828dffbfc2c2")
    version("1.1.9", sha256="c615777539154288542cf393d3fd44c04ccb3260bc6330dc324d4e4ebe902bfa")
    version("1.1.7", sha256="e6d3956a26c3965703402e17f153ba07f59bf710068806462b314d2d04e825e7")
    version("1.1.6", sha256="5f32d305279a51ce8bdbe69e733c4ac12b1efdcb77758fab8ec9463e96a8fd82")
    version("1.1.5", sha256="3eadb26b6656a89a111abe29c7e50eab0023e9a8718f1e77e46ca871398bfa67")
    version("1.1.4", sha256="b1ab9d5842002803e66da8f456ee00f352ea2bb43436d5b668f19ef7475ed4a5")
    version("1.1.3", sha256="c7bf7f4d5955e1868739627928238d02f94ca9fd0caf110b0243d65548427899")
    version("1.0.2", sha256="2d7a9d0a76d5574459d249c3415e21423980d9154ce85e8c34b0600782a7dfd3")

    depends_on("c", type="build")  # generated

    depends_on("e2fsprogs@1.47:+fuse2fs", type="run")
    depends_on("go@1.17.5:", when="@1.1.0:")
    depends_on("go@1.19:", when="@1.2:")
    depends_on("go@1.20:", when="@1.3:")
    depends_on("gocryptfs@2.4:", type="run", when="@1.3:")
    depends_on("squashfuse", type="run")
    depends_on("squashfuse@0.5.1:", type="run", when="@1.3:")
    depends_on("fuse-overlayfs", type="run")
    depends_on("fuse-overlayfs@1.13:", type="run", when="@1.3:")

    singularity_org = "apptainer"
    singularity_name = "apptainer"
    singularity_security_urls = (
        "https://apptainer.org/docs/admin/main/security.html",
        "https://apptainer.org/docs/admin/main/admin_quickstart.html#apptainer-security",
    )

    # Override config options from SingularityBase
    @property
    def config_options(self):
        spec = self.spec
        options = []
        if spec.satisfies("@1.1.0: +suid"):
            options.append("--with-suid")
        return options

    def flag_handler(self, name, flags):
        # Certain go modules this build pulls in cannot be built with anything
        # other than -O0. Best to just discard any injected flags.
        return (None, flags, None)

    # They started vendoring the fuse bits and assume they'll be in the
    # libexec/apptainer prefix as a result. When singularity is run with
    # suid it doesn't search the user's $PATH for security reasons.
    # Since we don't use the vendored deps and instead install them in
    # their own prefixes they are not found by default.
    # This is likely only relevant for 1.3:, but it should be fine everywhere
    @run_after("install")
    def fix_binary_path(self):
        for i in [
            s for s in ["e2fsprogs", "gocryptfs", "squashfuse", "fuse-overlayfs"] if s in self.spec
        ]:
            for binary in glob(join_path(self.spec[i].prefix.bin, "*")):
                symlink(
                    binary, join_path(self.spec.prefix.libexec.apptainer.bin, basename(binary))
                )
