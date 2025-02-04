# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nnn(MakefilePackage):
    """nnn (n³) is a full-featured terminal file manager.
    It's tiny, nearly 0-config and incredibly fast."""

    homepage = "https://github.com/jarun/nnn"
    url = "https://github.com/jarun/nnn/archive/refs/tags/v5.0.tar.gz"

    maintainers("fthaler")

    license("BSD-2-Clause", checked_by="fthaler")

    version("5.0", sha256="31e8fd85f3dd7ab2bf0525c3c0926269a1e6d35a5343a6714315642370d8605a")

    depends_on("binutils", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("coreutils")
    depends_on("file")
    depends_on("git", when="+gitstatus")
    depends_on("ncurses")
    depends_on("pcre", when="+pcre")
    depends_on("readline", when="+readline")
    depends_on("sed")
    depends_on("tar")
    depends_on("zip")

    variant("mouse", default=True, description="Enable mouse support")
    variant(
        "pcre",
        default=False,
        description="Use Perl Compatible Regular Expressions (default is POSIX)",
    )
    variant("readline", default=True, description="Compile with readline")
    variant(
        "icons",
        values=("none", "emoji", "nerd", "icons-in-terminal"),
        default="emoji",
        description="Choose the icons to use "
        "(see https://github.com/jarun/nnn/wiki/Advanced-use-cases#file-icons)",
    )

    variant("colemak", default=False, description="Key bindings for Colemak keyboard layout")
    variant("gitstatus", default=True, description="Add git status column to the detail view")
    variant("namefirst", default=False, description="Print filenames first in the detail view")
    variant(
        "restorepreview",
        default=False,
        description="Add pipe to close and restore preview-tui for internal undetached edits",
    )

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("PREFIX", self.prefix)
        if "+pcre" in spec:
            env.append_flags("CPPFLAGS", spec["pcre"].headers.include_flags)
            env.append_flags("LDFLAGS", spec["pcre"].libs.ld_flags)

    @property
    def build_targets(self):
        spec = self.spec
        targets = []
        if "~mouse" in spec:
            targets.append("O_NOMOUSE=1")
        if "+pcre" in spec:
            targets.append("O_PCRE=1")
        if "~readline" in spec:
            targets.append("O_NORL=1")

        if "icons=emoji" in spec:
            targets.append("O_EMOJI=1")
        elif "icons=nerd" in spec:
            targets.append("O_NERD=1")
        elif "icons=icons-in-terminal" in spec:
            targets.append("O_ICONS=1")

        if "+colemak" in spec:
            targets.append("O_COLEMAK=1")
        if "+gitstatus" in spec:
            targets.append("O_GITSTATUS=1")
        if "+namefirst" in spec:
            targets.append("O_NAMEFIRST=1")
        if "+restorepreview" in spec:
            targets.append("O_RESTOREPREVIEW=1")
        return targets

    @property
    def install_targets(self):
        return self.build_targets + ["strip", "install"]
