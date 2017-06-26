##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import spack
import pytest

from spack.build_environment import get_std_cmake_args
from spack.spec import Spec


def test_cmake_std_args(config, builtin_mock):
    # Call the function on a CMakePackage instance
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    assert pkg.std_cmake_args == get_std_cmake_args(pkg)

    # Call it on another kind of package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    assert get_std_cmake_args(pkg)


@pytest.mark.usefixtures('config', 'builtin_mock')
class TestAutotoolsPackage(object):

    def test_with_or_without(self):
        s = Spec('a')
        s.concretize()
        pkg = spack.repo.get(s)

        # Called without parameters
        l = pkg.with_or_without('foo')
        assert '--with-bar' in l
        assert '--without-baz' in l
        assert '--no-fee' in l

        def activate(value):
            return 'something'

        l = pkg.with_or_without('foo', active_parameters=activate)
        assert '--with-bar=something' in l
        assert '--without-baz' in l
        assert '--no-fee' in l

        l = pkg.enable_or_disable('foo')
        assert '--enable-bar' in l
        assert '--disable-baz' in l
        assert '--disable-fee' in l
