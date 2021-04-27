# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.pkgkit import *


class HdfEos2(AutotoolsPackage):
    """HDF-EOS (Hierarchical Data Format - Earth Observing System) is a
    self-describing file format based upon HDF for standard data products
    that are derived from EOS missions.  HDF-EOS2 is based upon HDF4.
    """

    homepage = "https://hdfeos.org"
    # The download URLs are messing, and include sha256 checksum.
    # This is just a template.  See version_list and url_for_version below
    # Template for url_for_version. 0 is sha256 checksum, 1 is filename
    url = "https://git.earthdata.nasa.gov/rest/git-lfs/storage/DAS/hdfeos/{0}?response-content-disposition=attachment%3B%20filename%3D%22{1}%22%3B%20filename*%3Dutf-8%27%27{1}"

    # Crazy URL scheme, differing with each version, and including the
    # sha256 checksum in the URL.  Yuck
    # The data in version_list is used to generate versions and urls
    # In basename expansions, 0 is raw version,
    # 1 is for version with dots => underscores
    version_list = [
        {'version': '2.20v1.00',
            'sha256': 'cb0f900d2732ab01e51284d6c9e90d0e852d61bba9bce3b43af0430ab5414903',
            'basename': 'HDF-EOS{0}.tar.Z'},
        {'version': '2.19b',
            'sha256': 'a69993508dbf5fa6120bac3c906ab26f1ad277348dfc2c891305023cfdf5dc9d',
            'basename': 'hdfeos{1}.zip'}
    ]

    for vrec in version_list:
        ver = vrec['version']
        sha256 = vrec['sha256']
        version(ver, sha256=sha256)

    variant('shared', default=True,
            description='Build shared libraries (can be used with +static)')
    variant('static', default=True,
            description='Build static libraries (can be used with +shared)')

    conflicts('~static', when='~shared',
              msg='At least one of +static or +shared must be set')

    # Build dependencies
    depends_on('hdf')

    # The standard Makefile.am, etc. add a --single_module flag to LDFLAGS
    # to pass to the linker.
    # That appears to be only recognized by the Darwin linker, remove it
    # if we are not running on darwin/
    if sys.platform != "darwin":
        patch('hdf-eos2.nondarwin-no-single_module.patch')

    def url_for_version(self, version):
        vrec = [x for x in self.version_list
                if x['version'] == version.dotted.string]
        if vrec:
            fname = vrec[0]['basename'].format(version.dotted,
                                               version.underscored)
            sha256 = vrec[0]['sha256']
            myurl = self.url.format(sha256, fname)
            return myurl
        else:
            sys.exit('ERROR: cannot generate URL for version {0};'
                     'version/checksum not found in version_list'.format(
                         version))

    def configure_args(self):
        extra_args = []

        # Package really wants h4cc to be used
        extra_args.append('CC={0}/bin/h4cc -Df2cFortran'.format(
            self.spec['hdf'].prefix))

        # We always build PIC code
        extra_args.append('--with-pic')

        # Set shared/static appropriately
        extra_args.extend(self.enable_or_disable('shared'))
        extra_args.extend(self.enable_or_disable('static'))

        # Provide config args for dependencies
        extra_args.append('--with-hdf4={0}'.format(self.spec['hdf'].prefix))
        if self.spec['jpeg']:
            extra_args.append('--with-jpeg={0}'.format(
                self.spec['jpeg'].prefix))
        if self.spec['zlib']:
            extra_args.append('--with-zlib={0}'.format(
                self.spec['zlib'].prefix))

        return extra_args
