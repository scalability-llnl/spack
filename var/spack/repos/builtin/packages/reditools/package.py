# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Reditools(PythonPackage):
    """REDItools: python scripts for RNA editing detection by RNA-Seq data.

    REDItools are simple python scripts conceived to facilitate the
    investigation of RNA editing at large-scale and devoted to research groups
    that would to explore such phenomenon in own data but don't have sufficient
    bioinformatics skills. They work on main operating systems (although
    unix/linux-based OS are preferred), can handle reads from whatever platform
    in the standard BAM format and implement a variety of filters."""

    homepage = "https://github.com/BioinfoUNIBA/REDItools"
    git      = "https://github.com/BioinfoUNIBA/REDItools.git"

    version('1.3_2020-03-20', commit='cf47f3d54f324aeb9650bcf8bfacf5a967762a55')

    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-fisher', type=('build', 'run'))
    depends_on('blat', type='run')
    depends_on('tabix', type='run')

    patch('REDItoolDenovo.py.patch')
    patch('interpreter.patch')
    patch('setup.py.patch')
    patch('python2to3.patch', when='^python@3:')
