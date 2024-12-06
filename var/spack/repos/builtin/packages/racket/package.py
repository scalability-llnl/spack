# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.makefile
from spack.package import *


class Racket(MakefilePackage):
    """The Racket programming language."""

    homepage = "https://www.racket-lang.org"

    maintainers("arjunguha", "elfprince13")

    license("Apache-2.0 OR MIT")

    version("8.3", sha256="3b963cd29ae119e1acc2c6dc4781bd9f25027979589caaae3fdfc021aac2324b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libffi", type=("build", "link", "run"))
    depends_on("patchutils")

    variant("cs", default=True, description="Build Racket CS (new ChezScheme VM)")
    variant("bc", default=False, description="Build Racket BC (old MZScheme VM)")
    variant("shared", default=True, description="Enable shared")
    variant("jit", default=True, description="Just-in-Time Compilation")

    parallel = False
    extendable = True

    def url_for_version(self, version):
        return "https://mirror.racket-lang.org/installers/{0}/racket-minimal-{0}-src-builtpkgs.tgz".format(
            version
        )


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    build_directory = "src"

    def toggle(self, spec, variant):
        toggle_text = "enable" if spec.variants[variant].value else "disable"
        return "--{0}-{1}".format(toggle_text, variant)

    def edit(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            configure = Executable("./configure")
            configure_args = [
                self.toggle(spec, "cs"),
                self.toggle(spec, "bc"),
                self.toggle(spec, "jit"),
            ]
            toggle_shared = self.toggle(spec, "shared")
            if spec.satisfies("platform=darwin"):
                configure_args += ["--enable-macprefix"]
                if "+xonx" in spec:
                    configure_args += ["--enable-xonx", toggle_shared]
            else:
                configure_args += [toggle_shared]
            configure_args += ["--prefix={0}".format(prefix)]
            configure(*configure_args)

    @property
    def build_targets(self):
        result = []
        if "+bc" in self.spec:
            result.append("bc")
        if "+cs" in self.spec:
            result.append("cs")
        return result

    @property
    def install_targets(self):
        result = []
        if "+bc" in self.spec:
            result.append("install-bc")
        if "+cs" in self.spec:
            result.append("install-cs")
        return result
