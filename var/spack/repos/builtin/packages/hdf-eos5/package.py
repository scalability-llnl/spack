# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from os import chmod

from spack.package import *


class HdfEos5(AutotoolsPackage):
    """HDF-EOS (Hierarchical Data Format - Earth Observing System) is a
    self-describing file format based upon HDF for standard data products
    that are derived from EOS missions.  HDF-EOS5 is based upon HDF5.
    """

    homepage = "https://hdfeos.org"
    # The download URLs are messing, and include sha256 checksum.
    # This is just a template.  See version_list and url_for_version below
    # Template for url_for_version. 0 is sha256 checksum, 1 is filename
    url = "https://git.earthdata.nasa.gov/rest/git-lfs/storage/DAS/hdfeos5/{0}?response-content-disposition=attachment%3B%20filename%3D%22{1}%22%3B%20filename*%3Dutf-8%27%27{1}"

    # Crazy URL scheme, differing with each version, and including the
    # sha256 checksum in the URL.  Yuck
    # The data in version_list is used to generate versions and urls
    # In basename expansions, 0 is raw version,
    # 1 is for version with dots => underscores
    version_list = [
        {
            "version": "5.1.16",
            "sha256": "7054de24b90b6d9533329ef8dc89912c5227c83fb447792103279364e13dd452",
            "basename": "HDF-EOS{0}.tar.Z",
        },
        {
            "version": "5.1.15",
            "sha256": "fbf4d085f9bf6ffad259aee1e9f60cf060e7e99c447894ad8955df02de83c92c",
            "basename": "hdfeos{1}.zip",
        },
    ]

    for vrec in version_list:
        ver = vrec["version"]
        sha256 = vrec["sha256"]
        version(ver, sha256=sha256)

    variant(
        "shared", default=True, description="Build shared libraries (can be used with +static)"
    )
    variant(
        "static", default=True, description="Build shared libraries (can be used with +shared)"
    )

    conflicts("~static", when="~shared", msg="At least one of +static or +shared must be set")

    maintainers("payerle")

    # Build dependencies
    depends_on("hdf5+hl")

    # The standard Makefile.am, etc. add a --single_module flag to LDFLAGS
    # to pass to the linker.
    # That appears to be only recognized by the Darwin linker, remove it
    # if we are not running on darwin/
    if sys.platform != "darwin":
        patch("hdf-eos5.nondarwin-no-single_module.patch")

    def url_for_version(self, version):
        vrec = [x for x in self.version_list if x["version"] == version.dotted.string]
        if vrec:
            fname = vrec[0]["basename"].format(version.dotted, version.underscored)
            sha256 = vrec[0]["sha256"]
            myurl = self.url.format(sha256, fname)
            return myurl
        else:
            sys.exit(
                "ERROR: cannot generate URL for version {0};"
                "version/checksum not found in version_list".format(version)
            )

    @run_before("configure")
    def fix_configure(self):
        # spack patches the configure file unless autoconf is run,
        # and this fails because configure has the wrong permissions (644)
        if not self.force_autoreconf:
            chmod(join_path(self.stage.source_path, "configure"), 0o755)

        # The configure script as written really wants you to use h5cc. This causes
        # problems because h5cc differs when HDF5 is built with autotools vs cmake,
        # and we lose all nice flags from the Spack wrappers. These filter operations
        # allow use to use the Spack wrappers again.
        with keep_modification_time("configure"):
            filter_file(r"$CC -show &> /dev/null", "true", "configure", string=True)
            filter_file(r"CC=./$SZIP_CC", "", "configure", string=True)

    def configure_args(self):
        extra_args = []

        # We always build PIC code
        extra_args.append("--with-pic")
        # We always enable installation of include directories
        extra_args.append("--enable-install-include")

        # Set shared/static appropriately
        extra_args.extend(self.enable_or_disable("shared"))
        extra_args.extend(self.enable_or_disable("static"))

        # Provide config args for dependencies
        extra_args.append("--with-hdf5={0}".format(self.spec["hdf5"].prefix))
        if self.spec.satisfies("^szip"):
            extra_args.append("--with-szlib={0}".format(self.spec["szip"].prefix))
        if self.spec.satisfies("^zlib-api"):
            extra_args.append("--with-zlib={0}".format(self.spec["zlib-api"].prefix))

        return extra_args
