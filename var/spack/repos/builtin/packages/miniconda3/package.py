# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform
from os.path import split

from spack.pkgkit import *


_versions = {
    '4.9.2': {
        'Linux-ppc64le': ('2b111dab4b72a34c969188aa7a91eca927a034b14a87f725fa8d295955364e71', 'https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-ppc64le.sh'),
        'Linux-x86_64': ('1314b90489f154602fd794accfc90446111514a5a72fe1f71ab83e07de9504a7', 'https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh')},
    '4.8.2': {
        'Linux-x86_64': ('5bbb193fd201ebe25f4aeb3c58ba83feced6a25982ef4afa86d5506c3656c142', 'https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.2-Linux-x86_64.sh')},
    '4.7.12.1': {
        'Linux-x86_64': ('bfe34e1fa28d6d75a7ad05fd02fa5472275673d5f5621b77380898dee1be15d2', 'https://repo.continuum.io/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh')},
    '4.6.14': {
        'Linux-x86_64': ('0d6b23895a91294a4924bd685a3a1f48e35a17970a073cd2f684ffe2c31fc4be', 'https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh')},
    '4.5.11': {
        'Linux-x86_64': ('ea4594241e13a2671c5b158b3b813f0794fe58d514795fbf72a1aad24db918cf', 'https://repo.continuum.io/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh')},
    '4.5.4': {
        'Linux-x86_64': ('80ecc86f8c2f131c5170e43df489514f80e3971dd105c075935470bbf2476dea', 'https://repo.continuum.io/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh')},
    '4.3.30': {
        'Linux-x86_64': ('66c822dfe76636b4cc2ae5604816e0e723aa01620f50087f06410ecf5bfdf38c', 'https://repo.continuum.io/miniconda/Miniconda3-4.3.30-Linux-x86_64.sh')},
    '4.3.14': {
        'Linux-x86_64': ('902f31a46b4a05477a9862485be5f84af761a444f8813345ff8dad8f6d3bccb2', 'https://repo.continuum.io/miniconda/Miniconda3-4.3.14-Linux-x86_64.sh')},
    '4.3.11': {
        'Linux-x86_64': ('b9fe70ce7b6fa8df05abfb56995959b897d0365299f5046063bc236843474fb8', 'https://repo.continuum.io/miniconda/Miniconda3-4.3.11-Linux-x86_64.sh')},
}


class Miniconda3(Package):
    """The minimalist bootstrap toolset for conda and Python3."""

    homepage = "https://conda.io/miniconda.html"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    def install(self, spec, prefix):
        # peel the name of the script out of the pathname of the
        # downloaded file
        dir, script = split(self.stage.archive_file)
        bash = which('bash')
        bash(script, '-b', '-f', '-p', self.prefix)
