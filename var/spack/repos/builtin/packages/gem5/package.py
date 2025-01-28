# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.config
from spack.package import *


class Gem5(SConsPackage):
    """The gem5 simulator is a modular platform for computer-system
    architecture research, encompassing system-level architecture as
    well as processor microarchitecture. gem5 is a community led
    project with an open governance model. gem5 was originally
    conceived for computer architecture research in academia, but it
    has grown to be used in computer system design by academia,
    industry for research, and in teaching."""

    homepage = "https://www.gem5.org"
    git = "https://github.com/gem5/gem5"
    url = "https://github.com/gem5/gem5/archive/refs/tags/v24.0.0.0.tar.gz"

    version("24.0.0.1", tag="v24.0.0.1", commit="b1a44b89c7bae73fae2dc547bc1f871452075b85")
    version("24.0.0.0", tag="v24.0.0.0", commit="43769abaf05120fed1e4e0cfbb34619edbc10f3f")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("scons", type="build")
    depends_on("py-mypy", type="build")
    depends_on("py-pybind11", type="build")
    depends_on("python")
    depends_on("gettext")
    depends_on("hdf5+cxx")
    depends_on("protobuf")
    depends_on("gperftools")
    depends_on("graphviz+pangocairo", type=("build", "run"))
    depends_on("py-pydot", type=("build", "run"))
    depends_on("capstone")

    def patch(self):
        filter_file(
            " Environment(tools=[",
            " Environment(ENV=os.environ, tools=[",
            "SConstruct",
            string=True,
        )
        filter_file(
            """conf.env['CONF']['HAVE_PERF_ATTR_EXCLUDE_HOST'] = conf.CheckMember(""",
            """conf.env['CONF']['HAVE_PERF_ATTR_EXCLUDE_HOST'] = bool(conf.CheckMember(""",
            "src/cpu/kvm/SConsopts",
            string=True,
        )
        filter_file(
            """perf_event_attr', 'exclude_host')""",
            """perf_event_attr', 'exclude_host'))""",
            "src/cpu/kvm/SConsopts",
            string=True,
        )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("build/ALL/gem5.opt", prefix.bin)

    def build_args(self, spec, prefix):
        args = []
        args.append("build/ALL/gem5.opt")
        args.append(f"-j{spack.config.determine_number_of_jobs(parallel=True)}")
        args.append("--ignore-style")

        return args
