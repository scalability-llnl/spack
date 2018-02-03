##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
from llnl.util.link_tree import LinkTree, MergeConflictError
import spack.store
from spack.package import ExtensionError


# See also: AspellDictPackage
class Aspell(AutotoolsPackage):
    """GNU Aspell is a Free and Open Source spell checker designed to
    eventually replace Ispell."""

    homepage = "http://aspell.net/"
    url      = "https://ftpmirror.gnu.org/aspell/aspell-0.60.6.1.tar.gz"

    extendable = True           # support activating dictionaries

    version('0.60.6.1', 'e66a9c9af6a60dc46134fdacf6ce97d7')

    # Note: aspell doesn't support non-global extensions so this skips
    # calling view.merge
    def activate(self, extension, view, **kwargs):
        if view.root != self.spec.prefix:
            raise ExtensionError(
                'aspell does not support non-global extensions')

        aspell = which(self.prefix.bin.aspell)
        # The dictionaries install all their bits into their prefix.lib dir,
        # we want to link them into aspell's dict-dir.
        dest_dir = aspell('dump', 'config', 'dict-dir', output=str).strip()
        tree = LinkTree(extension.prefix.lib)

        def ignore(filename):
            return (filename in spack.store.layout.hidden_file_paths or
                    kwargs.get('ignore', lambda f: False)(filename))

        conflict = tree.find_conflict(dest_dir, ignore=ignore)
        if conflict:
            raise MergeConflictError(conflict)

        tree.merge(dest_dir, ignore=ignore)

    def deactivate(self, extension, view, **kwargs):
        aspell = which(self.prefix.bin.aspell)
        dest_dir = aspell('dump', 'config', 'dict-dir', output=str).strip()

        def ignore(filename):
            return (filename in spack.store.layout.hidden_file_paths or
                    kwargs.get('ignore', lambda f: False)(filename))

        tree = LinkTree(extension.prefix.lib)
        tree.unmerge(dest_dir, ignore=ignore)
