# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.phase_callbacks
from spack.build_systems import generic
from spack.package import *


class BuilderAndMixins(Package):
    """This package defines a mixin for its builder"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")


class BuilderMixin(metaclass=spack.phase_callbacks.PhaseCallbacksMeta):
    @run_before("install")
    def before_install(self):
        pass

    @run_after("install")
    def after_install(self):
        pass


class GenericBuilder(BuilderMixin, generic.GenericBuilder):
    def install(self, pkg, spec, prefix):
        pass
