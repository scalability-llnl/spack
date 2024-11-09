# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import set_env


class Sbcl(MakefilePackage):
    """Steel Bank Common Lisp (SBCL) is a high performance Common Lisp compiler.
    It is open source / free software, with a permissive license. In addition
    to the compiler and runtime system for ANSI Common Lisp, it provides an
    interactive environment including a debugger, a statistical profiler, a
    code coverage tool, and many other extensions.
    """

    homepage = "https://www.sbcl.org/"
    url = "https://sourceforge.net/projects/sbcl/files/sbcl/2.4.8/sbcl-2.4.8-source.tar.bz2"
    git = "git://git.code.sf.net/p/sbcl/sbcl"

    maintainers("ashermancinelli")

    # NOTE: The sbcl homepage lists
    # while the sourceforge repo lists "Public Domain, MIT License", the
    # COPYING file distributed with the source code contains this message:
    #
    # > Thus, there are no known obstacles to copying, using, and modifying
    # > SBCL freely, as long as copyright notices of MIT, Symbolics, Xerox and
    # > Gerd Moellmann are retained.
    #
    # MIT seems the most appropriate, but if we can add more context to this
    # license message, then we should.
    license("MIT", checked_by="ashermancinelli")

    version("master", branch="master")
    version("2.4.8", sha256="fc6ecdcc538e80a14a998d530ccc384a41790f4f4fc6cd7ffe8cb126a677694c")

    depends_on("c", type="build")
    depends_on("sbcl-bootstrap", type="build")
    depends_on("zstd", when="platform=darwin")

    variant(
        "fancy", default=True, description="Enable extra features like compression and threading."
    )

    # TODO(ashermancinelli): there's nothing on the platform support page that
    #                        makes me think this shouldn't build, but I can't
    #                        get the sbcl binary to link with gcc on darwin.
    conflicts(
        "+fancy%gcc",
        when="platform=darwin",
        msg="Cannot build with gcc on darwin because pthreads will fail to link",
    )

    phases = ["build", "install"]

    def build(self, spec, prefix):
        sh = which("sh")

        version_str = str(spec.version)

        # NOTE: add any other git versions here.
        # When installing from git, the build system expects a dummy version
        # to be provided as a lisp expression.
        if version_str in ("master",):
            with open("version.lisp-expr", "w") as f:
                f.write(f'"{version_str}"')

        build_args = []
        build_args.append("--prefix={0}".format(prefix))

        if "+fancy" in self.spec:
            build_args.append("--fancy")

        sbcl_bootstrap_prefix = self.spec["sbcl-bootstrap"].prefix.lib.sbcl
        with set_env(SBCL_HOME=sbcl_bootstrap_prefix):
            sh("make.sh", *build_args)

    def install(self, spec, prefix):
        sh = which("sh")
        sh("install.sh")
