# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zuo(AutotoolsPackage):
    """A tiny Racket for scripting."""

    homepage = "https://github.com/racket/zuo"
    url = "https://github.com/racket/zuo/archive/refs/tags/v1.11.tar.gz"

    license("Apache-2.0 AND MIT", checked_by="Buldram")
    maintainers("Buldram")

    version("1.11", sha256="8404bea8ecae4576f44dece7efcab69d94c8a30ec10ea186f86823d37e74694b")

    variant("big", default=False, description="Enable hygienic macro support")

    depends_on("c", type="build")

    def setup_build_environment(self, env):
        env.set("ZUO_JOBS", make_jobs)

    def configure_args(self):
        return [*self.enable_or_disable("big")]
