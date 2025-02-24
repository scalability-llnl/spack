# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Fzf(GoPackage):
    """A general-purpose command-line fuzzy finder that provides fast, interactive
    filtering for files, processes, git commits, and more. It supports fuzzy
    search with real-time preview and various input sources."""

    homepage = "https://github.com/junegunn/fzf"
    url = "https://github.com/junegunn/fzf/archive/v0.54.0.tar.gz"
    git = "https://github.com/junegunn/fzf.git"

    maintainers("alecbcs")

    license("MIT")

    sanity_check_is_file = ["bin/fzf"]

    # Versions from newest to oldest
    version("master", branch="master")
    version("0.60.0", sha256="69255fd9301e491b6ac6788bf1caf5d4f70d9209b4b8ab70ceb1caf6a69b5c16")
    version("0.57.0", sha256="d4e8e25fad2d3f75943b403c40b61326db74b705bf629c279978fdd0ceb1f97c")
    version("0.56.2", sha256="1d67edb3e3ffbb14fcbf786bfcc0b5b8d87db6a0685135677b8ef4c114d2b864")
    version("0.55.0", sha256="805383f71bca7f8fb271ecd716852aea88fd898d5027d58add9e43df6ea766da")
    version("0.54.3", sha256="6413f3916f8058b396820f9078b1336d94c72cbae39c593b1d16b83fcc4fdf74")
    version("0.53.0", sha256="d45abbfb64f21913c633d46818d9d3eb3d7ebc7e94bd16f45941958aa5480e1d")
    version("0.52.1", sha256="96848746ca78249c1fdd16f170776ce2f667097b60e4ffbd5ecdbd7dfac72ef9")
    version("0.48.1", sha256="c8dbb545d651808ef4e1f51edba177fa918ea56ac53376c690dc6f2dd0156a71")
    version("0.47.0", sha256="bc566cb4630418bc9981898d3350dbfddc114637a896acaa8d818a51945bdf30")
    version("0.46.1", sha256="b0d640be3ae79980fdf461096f7d9d36d38ec752e25f8c4d2ca3ca6c041c2491")
    version("0.45.0", sha256="f0dd5548f80fe7f80d9277bb8fe252ac6e42a41e76fc85ce0f3af702cd987600")
    version("0.44.1", sha256="295f3aec9519f0cf2dce67a14e94d8a743d82c19520e5671f39c71c9ea04f90c")
    version("0.42.0", sha256="743c1bfc7851b0796ab73c6da7db09d915c2b54c0dd3e8611308985af8ed3df2")
    version("0.41.1", sha256="982682eaac377c8a55ae8d7491fcd0e888d6c13915d01da9ebb6b7c434d7f4b5")
    version("0.40.0", sha256="9597f297a6811d300f619fff5aadab8003adbcc1566199a43886d2ea09109a65")

    # Variants
    variant("vim", default=False, description="Install vim plugins for fzf")

    # Build dependencies
    depends_on("go@1.20:", type="build", when="@0.49.0:")
    depends_on("go@1.17:", type="build")

    executables = ["^fzf$"]

    @classmethod
    def determine_version(cls, exe):
        """Determine version of installed fzf executable."""
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"(^[\d.]+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        """Generate download URL for a specific version."""
        base = "refs/tags/v" if self.spec.satisfies("@:0.53.0") else ""
        return f"https://github.com/junegunn/fzf/archive/{base}{version}.tar.gz"

    def setup_build_environment(self, env):
        """Set up the build environment for fzf."""
        # Setup build env from GoPackage builder
        super().setup_build_environment(env)

        # Set required environment variables for non-git builds
        env.set("FZF_VERSION", self.spec.version)
        env.set("FZF_REVISION", "tarball")

    @run_after("install")
    def install_completions(self):
        mkdirp(bash_completion_path(self.prefix))
        mkdirp(zsh_completion_path(self.prefix))

        install("shell/completion.bash", bash_completion_path(self.prefix) / "fzf.bash")
        install("shell/completion.zsh", zsh_completion_path(self.prefix) / "_fzf")

    @run_after("install", when="+vim")
    def install_vim_plugin(self):
        mkdirp(self.prefix.share.fzf.plugins)
        install("plugin/fzf.vim", self.prefix.share.fzf.plugins)
