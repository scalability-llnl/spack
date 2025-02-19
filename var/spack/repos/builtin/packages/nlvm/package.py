# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path

from spack.package import *


class Nlvm(MakefilePackage):
    """LLVM-based compiler for the Nim programming language."""

    homepage = "https://github.com/arnetheduck/nlvm/"
    git = "https://github.com/arnetheduck/nlvm.git"

    license("MIT", checked_by="Buldram")
    maintainers("Buldram")

    version("2024.12.30", commit="89db076a7b2907d87463496017b5a5c2a7448686")

    variant("static_llvm", default=False, description="Link to LLVM statically")

    conflicts("%apple-clang", msg="Incompatible with Apple Clang's default linker")

    depends_on("llvm +clang @19.1", type="build")
    depends_on("llvm +llvm_dylib @19.1", type=("build", "link"), when="~static_llvm")
    depends_on(
        "nim@2.0.14",
        type=("build", "link"),
        patches=[
            patch(
                "https://github.com/nim-lang/Nim/compare/bf4de6a394e040d9810cba8c69fb2829ff04dcc6...6458db7e9a0dcbdfa632792267a06edc1663579f.patch?full_index=1",
                sha256="c8988abca46763a0e9923aeae7aa99e983077ee326303f466fb998cd2c90fa52",
            )
        ],
    )

    def edit(self, spec, prefix):
        if spec.satisfies("+static_llvm"):
            env["STATIC_LLVM"] = "1"

        # Use system LLVM
        makefile = FileFilter("Makefile")
        makefile.filter("../ext ", spec["llvm"].prefix, string=True)
        makefile.filter("$(LLVM_DEP) ", "", string=True)

        filter_file(
            'LLVM(Out|Root) & "(sta/)?bin/llvm-config',
            '"' + spec["llvm"].prefix.bin.join("llvm-config"),
            "llvm/llvm.nim",
        )
        filter_file("{.pass(L|C):.*LL(VM|D)(Out|Root).*.}", "", "llvm/llvm.nim")

        # Use system Nim
        makefile.filter("Nim/bin/nim", spec["nim"].prefix.bin.join("nim"), string=True)
        makefile.filter("../$(NIMC)", "$(NIMC)", string=True)
        makefile.filter(" $(NIMC) Nim/compiler/*.nim ", "", string=True)
        makefile.filter("testament: $(NIMC)", "testament:", string=True)

        nim_prefix = Path(spec["nim"].prefix).as_posix()  # TODO: Test escaping/Windows
        filter_file("../Nim", nim_prefix, "nlvm/nim.cfg", string=True)
        filter_file("../Nim", nim_prefix, "nlvm/nlvm.nim", string=True)
        filter_file('tmp / "Nim"', '"' + nim_prefix + '"', "nlvm/nlvm.nim", string=True)
        filter_file("../Nim", '"' + nim_prefix + '"', "nlvm/llgen.nim", string=True)

        # Move nlvm-lib, make absolute instead of dependent on Nim path
        filter_file("nlvm-lib", "lib", "nlvm/nlvm.nim", string=True)
        filter_file(
            'conf.prefixDir / RelativeDir"../lib"',
            'AbsoluteDir(tmp) / RelativeDir"lib"',
            "nlvm/nlvm.nim",
            string=True,
        )
        filter_file(
            'g.config.prefixDir.string / "../nlvm-lib',
            '"' + Path(prefix.lib).as_posix(),
            "nlvm/llgen.nim",
            string=True,
        )

    def install(self, spec, prefix):
        install_tree("nlvm", prefix.bin)
        install_tree("nlvm-lib", join_path(prefix, "lib"))
