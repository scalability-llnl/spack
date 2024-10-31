# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import numbers
import os
import urllib.parse

from spack.package import *


def _is_integral(x):
    """Accepts only integral values."""
    try:
        return isinstance(int(x), numbers.Integral) and (not isinstance(x, bool))
    except ValueError:
        return False


class Pythia6(CMakePackage):
    """PYTHIA is a program for the generation of high-energy physics events,
    i.e. for the description of collisions at high energies between elementary
    particles such as e+, e-, p and pbar in various combinations.

    PYTHIA6 is a Fortran package which is no longer maintained: new
    prospective users should use Pythia8 instead.

    This recipe includes patches required to interoperate with Root.
    """

    homepage = "https://pythiasix.hepforge.org/"
    url = "https://pythia.org/download/pythia6/pythia6428-split.tgz"

    tags = ["hep"]

    maintainers("gartung", "greenc-FNAL")

    version(
        "6.4.28",
        url="https://pythia.org/download/pythia6/pythia6428-split.tgz",
        sha256="01cbff47e99365b5e46f6d62c1735d3cae1932c4710604850d59f538cb758020",
    )

    depends_on("fortran", type="build")  # generated

    # Root's TPythia6 interface requires extra sources to be built into
    # the Pythia6 library.
    variant("root", default=False, description="Build extra (non OEM) code to allow use by Root.")

    # The maximum number of particles (NMXHEP) supported by the arrays
    # in the /HEPEVT/ COMMON block may need tweaking if pythia6 is
    # intended to be used with other code with different requirements.
    variant(
        "nmxhep",
        default=4000,
        values=_is_integral,
        description="Extent of particle arrays in the /HEPEVT/ COMMON block.",
    )

    # In the unlikely event of new versions >6.4.28,
    # pythia6_common_address.c should be checked for accuracy against
    # the definitions of the relevant COMMON blocks in the Pythia6
    # Fortran source, and patched if necessaary.
    resource(
        name="root-pythia6-shim",
        url="https://root.cern.ch/download/pythia6.tar.gz",
        sha256="d613dcb27c905710e2f13a934913cc5545e3e5d0e477e580107385d9ef260056",
        when="+root",
        destination=".",
        placement={
            "pythia6_common_address.c": "pythia6_common_address.c",
            "tpythia6_called_from_cc.F": "tpythia6_called_from_cc.F",
        },
    )

    # Download examples separately.
    examples = {
        "main60.f": "d713b8b267c4405cc9d31c58bba267ae3378902a26fa52393003bf35fd56902c",
        "main61.f": "e2a3d5524e43d16f60d9edc6e7198d41006d1ba127fb7b0e265aa509e13128b4",
        "main62.f": "dce822a72fe2d6cfb6d43c479ba98928fb0a39290a6ee26fdcacc66229313045",
        "main63.f": "b2dd343b3cd7969979b80c564d82b92e0d776d66bb19d346b52f2af27adeb62d",
        "main64.f": "a35f2f232e6e0d68d67fd350d4d46b0a353f5c7811de0c2db47ae16d17ed1843",
        "main65.f": "03c81e0bbd77710b0461e18265e80e3bd51360b9f416c86013401f882ac39a5e",
        "main66.f": "50dd9221a7e84ee7c5005db6758e5880d190eab8cce8a52e7c7b29e9fee8d3da",
        "main67.f": "1984aa90fe4e3d628c3bcceaa6fca1b08231d835158d975fa171337d55ca4a2f",
        "main68.f": "c8d6def1298477ffec6a1d98c7e02dcee0debe6badc7c63f752f9194b82f212d",
        "main69.f": "d14399d43f8c4b670907558849d3e5a4d7625d027de3c10002185c58b20b061a",
        "main71.f": "2e47af778003b0596e8999f0914033c6eda7335211b9e96ac3075d45a3cde12e",
        "main72.f": "e27ce2af68b40436c51c65767ebb5ff0955ab8dfdfc5fc5c217ae73cd53070da",
        "main73.f": "567db2d1a66896ce5103ffa7e10742442b0e934088883e91339536e0249772c4",
        "main75.f": "b850986c43a5af1e7d13b66d22b01584e3c68bb338be32eac39e31f971b80be4",
        "main77.f": "0679852c4f35719531ad38dc1dbb374b884181eb5e483c36d8867ccb449177a4",
        "main78.f": "09ed4b065d2c7ad439d4083d048a3a8f469963c1bb191811857c88f56ef07a5d",
        "main79.f": "27ca84d6d0877f3605cbc1b865c3e1f571e7d2c9301094a4122e726a903dbead",
        # Following files were not transferred to the new pythia.org website
        # https://web.archive.org/web/20150215042950/http://pythia6.hepforge.org/examples/main81.f
        # "main81.f": "b02fecd1cd0f9ba16eaae53e9da0ba602569fdf0e46856cccdfb4c5b7ba33e8b",
        # https://web.archive.org/web/20150215042950/http://pythia6.hepforge.org/examples/ttbar.lhe
        # "ttbar.lhe": "db772b69ab4e0300d973b57414523ac8e7fa8535eac49ee52a6b69b1c131983d",
    }

    for example, checksum in examples.items():
        resource(
            name=example,
            url="https://pythia.org/download/pythia6/{0}".format(example),
            sha256=checksum,
            expand=False,
            destination="example",
            placement={example: example},
        )

    # Docs.
    docs = {
        "https://pythia.org/download/pythia6/pythia6428.update": "a229be4ba9a4eb65a9d53600a5f388b620038d56694c6cb4671c2be224b67751",
        "https://pythia.org/download/pythia6/lutp0613man2.pdf": "03d637310ea80f0d7aea761492bd38452c602890d8cf913a1ec9edacd79fa43d",
        "https://pythia.org/download/misc/pythia6plans.txt": "1befc8c6e641051a97a53ba4df7f890bf0c4d6ba9e0774c03df69b0fef481d89",
    }

    for docurl, checksum in docs.items():
        doc = os.path.basename(urllib.parse.urlparse(docurl).path)
        resource(
            name=doc,
            url=docurl,
            sha256=checksum,
            expand=False,
            destination="doc",
            placement={doc: doc},
        )

    # The included patch customizes some routines provided in dummy form
    # by the original source to be useful out of the box in the vast
    # majority of cases. If your case is different, platform- or
    # variant-based adjustments should be made.
    patch("pythia6.patch", level=0)
    patch("pythia6-root.patch", level=1, when="+root")

    def patch(self):
        # Use our provided CMakeLists.txt. The Makefile provided with
        # the source is GCC (gfortran) specific, and would have required
        # additional patching for the +root variant.
        llnl.util.filesystem.copy(
            os.path.join(os.path.dirname(__file__), "CMakeLists.txt"), self.stage.source_path
        )
        # Apply the variant value at the relevant place in the source.
        filter_file(
            r"^(\s+PARAMETER\s*\(\s*NMXHEP\s*=\s*)\d+",
            r"\1{0}".format(self.spec.variants["nmxhep"].value),
            "pyhepc.f",
        )

    def setup_build_environment(self, env):
        if self.spec.satisfies("%gcc@10:"):
            env.append_flags("CFLAGS", "-fcommon")
            env.append_flags("FFLAGS", "-fcommon")

    def cmake_args(self):
        args = ["-DPYTHIA6_VERSION={0}".format(self.version.dotted)]
        if self.spec.satisfies("platform=darwin"):
            args.append(self.define("CMAKE_MACOSX_RPATH", True))
        return args
