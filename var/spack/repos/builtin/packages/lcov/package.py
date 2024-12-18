# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Lcov(MakefilePackage):
    """LCOV is a graphical front-end for GCC's coverage testing tool gcov.
    It collects gcov data for multiple source files and creates HTML pages
    containing the source code annotated with coverage information. It also
    adds overview pages for easy navigation within the file structure. LCOV
    supports statement, function and branch coverage measurement."""

    homepage = "https://ltp.sourceforge.net/coverage/lcov.php"
    url = "https://github.com/linux-test-project/lcov/releases/download/v2.0/lcov-2.0.tar.gz"
    git = "https://github.com/linux-test-project/lcov.git"

    maintainers("KineticTheory")

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("2.0", sha256="1857bb18e27abe8bcec701a907d5c47e01db4d4c512fc098d1a6acd29267bf46")
    version("1.16", sha256="987031ad5528c8a746d4b52b380bc1bffe412de1f2b9c2ba5224995668e3240b")
    version("1.15", sha256="c1cda2fa33bec9aa2c2c73c87226cfe97de0831887176b45ee523c5e30f8053a")
    version("1.14", sha256="14995699187440e0ae4da57fe3a64adc0a3c5cf14feab971f8db38fb7d8f071a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # dependencies from
    # https://github.com/linux-test-project/lcov/blob/02ece21d54ccd16255d74f8b00f8875b6c15653a/README#L91-L111
    depends_on("perl", type=("build", "run"))
    depends_on("perl-b-hooks-endofscope", type=("run"))
    depends_on("perl-capture-tiny", type=("run"))
    depends_on("perl-class-inspector", type=("run"))
    depends_on("perl-class-singleton", type=("run"))
    depends_on("perl-datetime", type=("run"))
    depends_on("perl-datetime-locale", type=("run"))
    depends_on("perl-datetime-timezone", type=("run"))
    depends_on("perl-devel-cover", type=("run"))
    depends_on("perl-devel-stacktrace", type=("run"))
    depends_on("perl-digest-md5", type=("run"))
    depends_on("perl-eval-closure", type=("run"))
    depends_on("perl-exception-class", type=("run"))
    depends_on("perl-file-sharedir", type=("run"))
    depends_on("perl-file-spec", type=("run"))
    depends_on("perl-json", type=("run"))
    depends_on("perl-memory-process", type=("run"))
    depends_on("perl-module-implementation", type=("run"))
    depends_on("perl-mro-compat", type=("run"))
    depends_on("perl-namespace-clean", type=("run"))
    depends_on("perl-package-stash", type=("run"))
    depends_on("perl-params-validationcompiler", type=("run"))
    depends_on("perl-role-tiny", type=("run"))
    depends_on("perl-specio", type=("run"))
    depends_on("perl-sub-identify", type=("run"))
    depends_on("perl-time-hires", type=("run"))
    depends_on("perl-timedate", type=("run"))

    def install(self, spec, prefix):
        make(
            "LCOV_PERL_PATH=%s" % self.spec["perl"].command.path,
            "DESTDIR=",
            "PREFIX=%s" % prefix,
            "install",
        )
