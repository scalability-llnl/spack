# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
    version("4.9", sha256="9e25465a856d3ba626d6163046669c0d4010d520f2fb848b0d611e1ec6af1b22")
    version("4.8", sha256="0a744e67a0ce8b5e1e04961f542d2c33ddb6ceed46ba760dd35c4922b21f1146")
    version("4.7", sha256="81ccccc045bfd7ee3f1909cc443158ea0d1833f77d6342fd19c33864a2ab71d1")
    version("4.6", sha256="15acaf9a88cfb5a2a640d3ef55a48af644fba92b46aac0768efe94c4addf7e3f")
    version("4.5", sha256="fadc15bd6d4400c06e5ccc47845b42e60774f368570e475bd882767ee18749aa")
    version("4.4", sha256="e04a3f0f0c2af1e18cb6f005d18267c7703644274d21bb93f03b30e4fd3d1653")
    version("4.3", sha256="b6df8e262e5613dd192bac610a6da711306627d56573f1a770a173ef078953bb")
    version("4.2", sha256="5675f9fe53bddfd92681ef88bf6c0fab3ad897f9e74dd6cdff32fe1fa62c687f")
    version("4.1.1", sha256="f0e02668da6324c12c39db35fe5c26bd45f3e02e5684a351b8ce8a357419ceba")

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
        default="none",
        description="Choose the icons to use "
        "(see https://github.com/jarun/nnn/wiki/Advanced-use-cases#file-icons)",
    )

    variant("colemak", default=False, description="Key bindings for Colemak keyboard layout")
    variant("gitstatus", default=False, description="Add git status column to the detail view")
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
