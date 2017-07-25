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
# "Benedikt Hegner (CERN)"
# "Patrick Gartung (FNAL)"

import os
import re
import tarfile
import yaml
import shutil

import llnl.util.tty as tty
from spack.util.gpg import Gpg
from llnl.util.filesystem import mkdirp, join_path
from spack.util.web import spider
import spack.cmd
import spack
from spack.stage import Stage
import spack.fetch_strategy as fs
import spack.relocate
from contextlib import closing


def buildinfo_file_name(spec):
    """
    Filename of the binary package meta-data file
    """
    installpath = join_path(spack.store.layout.root,
                            install_directory_name(spec))
    return os.path.join(installpath, ".spack", "binary_distribution")


def read_buildinfo_file(spec):
    """
    Read buildinfo file
    """
    filename = buildinfo_file_name(spec)
    with open(filename, 'r') as inputfile:
        content = inputfile.read()
        buildinfo = yaml.load(content)
    return buildinfo


def write_buildinfo_file(spec):
    """
    Create a cache file containing information
    required for the relocation
    """
    text_to_relocate = []
    binary_to_relocate = []
    blacklist = (".spack", "man")
    for root, dirs, files in os.walk(spec.prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for filename in files:
            path_name = os.path.join(root, filename)
            filetype = spack.relocate.get_filetype(path_name)
            if spack.relocate.needs_binary_relocation(filetype):
                rel_path_name = os.path.relpath(path_name, spec.prefix)
                binary_to_relocate.append(rel_path_name)
            elif spack.relocate.needs_text_relocation(filetype):
                rel_path_name = os.path.relpath(path_name, spec.prefix)
                text_to_relocate.append(rel_path_name)

    # Create buildinfo data and write it to disk
    buildinfo = {}
    buildinfo['buildpath'] = spack.store.layout.root
    buildinfo['relocate_textfiles'] = text_to_relocate
    buildinfo['relocate_binaries'] = binary_to_relocate
    filename = buildinfo_file_name(spec)
    with open(filename, 'w') as outfile:
        outfile.write(yaml.dump(buildinfo, default_flow_style=True))


def install_directory_name(spec):
    """
    Return name of the install directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>-<dag_hash>/
    """
    return "%s/%s/%s/%s-%s-%s" % (spack.store.layout.root,
                                  spack.architecture.sys_type(),
                                  str(spec.compiler).replace("@", "-"),
                                  spec.name, spec.version, spec.dag_hash())


def tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>/
    """
    return "%s/%s/%s-%s" % (spack.architecture.sys_type(),
                            str(spec.compiler).replace("@", "-"),
                            spec.name, spec.version)


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    return "%s-%s-%s-%s-%s%s" % (spack.architecture.sys_type(),
                                 str(spec.compiler).replace("@", "-"),
                                 spec.name,
                                 spec.version,
                                 spec.dag_hash(),
                                 ext)


def tarball_path_name(spec, ext):
    """
    Return the full path+name for a given spec according to the convention
    <tarball_directory_name>/<tarball_name>
    """
    return os.path.join(tarball_directory_name(spec),
                        tarball_name(spec, ext))


def build_tarball(spec, outdir, force=False, rel=False, yes_to_all=False,
                  key=None):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_dir = join_path(outdir, "build_cache",
                            tarball_directory_name(spec))
    tarfile_path = join_path(tarfile_dir, tarfile_name)
    mkdirp(tarfile_dir)
    spackfile_path = os.path.join(
        outdir, "build_cache", tarball_path_name(spec, '.spack'))
    if os.path.exists(spackfile_path):
        if force:
            os.remove(spackfile_path)
        else:
            tty.warn("file exists, use -f to force overwrite: %s" %
                     spackfile_path)
            return

    # need to copy the spec file so the build cache can be downloaded
    # without concretizing with the current spack packages
    # and preferences
    spec_file = join_path(spec.prefix, ".spack", "spec.yaml")
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = join_path(outdir, "build_cache", specfile_name)
    indexfile_path = join_path(outdir, "build_cache", "index.html")
    if os.path.exists(specfile_path):
        if force:
            os.remove(specfile_path)
        else:
            tty.warn("file exists, use -f to force overwrite: %s" %
                     specfile_path)
            return
    shutil.copyfile(spec_file, specfile_path)

    # create info for later relocation and create tar
    write_buildinfo_file(spec)
    if rel:
        prelocate_package(spec)
    with closing(tarfile.open(tarfile_path, 'w:gz')) as tar:
        tar.add(name='%s' % spec.prefix, arcname='%s' %
                os.path.basename(spec.prefix))

    # Sign the packages if keys available
    sign = True
    if key is None:
        keys = Gpg.signing_keys()
        if len(keys) == 1:
            key = keys[0]
        if len(keys) > 1:
            tty.warn(
                'multiple signing keys are available;' +
                ' please choose one with -k option')
            Gpg.list(False, True)
            sign = False
        if len(keys) == 0:
            tty.warn('No signing keys are available')
            if yes_to_all:
                sign = False
            else:
                raise RuntimeError('not creating unsigned build cache;' +
                                   'use spack buildcache create -y ' +
                                   'option to override')
    if sign:
        Gpg.sign(key, specfile_path, '%s.asc' % specfile_path)
        Gpg.sign(key, tarfile_path, '%s.asc' % tarfile_path)
    with closing(tarfile.open(spackfile_path, 'w')) as tar:
        tar.add(name='%s' % tarfile_path, arcname='%s' % tarfile_name)
        tar.add(name='%s' % specfile_path, arcname='%s' % specfile_name)
        if sign:
            tar.add(name='%s.asc' % tarfile_path, arcname='%s.asc' %
                    tarfile_name)
            tar.add(name='%s.asc' % specfile_path,
                    arcname='%s.asc' % specfile_name)
    os.remove(tarfile_path)
    if sign:
        os.remove('%s.asc' % tarfile_path)
        os.remove('%s.asc' % specfile_path)
    if os.path.exists(indexfile_path):
        os.remove(indexfile_path)
    f = open(indexfile_path, 'w')
    header = """<html>
<head></head>
<list>"""
    footer = "</list></html>"
    paths = os.listdir(outdir + '/build_cache')
    f.write(header)
    for path in paths:
        rel = os.path.basename(path)
        f.write('<li><a href="%s" %s</a>' % (rel, rel))
    f.write(footer)
    f.close()


def download_tarball(spec):
    """
    Download binary tarball for given package into stage area
    Return True if successful
    """
    mirrors = spack.config.get_config('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of pre-compiled packages.")
    tarball = tarball_path_name(spec, '.spack')
    for key in mirrors:
        url = mirrors[key] + "/build_cache/" + tarball
        # print url
        # stage the tarball into standard place
        stage = Stage(url, name="build_cache", keep=True)
        stage.create()
        try:
            stage.fetch()
            return stage.save_filename
        except fs.FetchError:
            next
    return None


def extract_tarball(spec, filename, yes_to_all=False, force=False):
    """
    extract binary tarball for given package into install area
    """
    installpath = install_directory_name(spec)
    if os.path.exists(installpath) and force:
        shutil.rmtree(installpath)
    mkdirp(installpath)
    stagepath = os.path.dirname(filename)
    spackfile_name = tarball_name(spec, '.spack')
    spackfile_path = os.path.join(stagepath, spackfile_name)
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_path = os.path.join(stagepath, tarfile_name)
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.join(stagepath, specfile_name)

    with closing(tarfile.open(spackfile_path, 'r')) as tar:
        tar.extractall(stagepath)

    install = False
#   signed
    if os.path.exists('%s.asc' % specfile_path) and os.path.exists(
            '%s.asc' % tarfile_path):
        if Gpg.verify('%s.asc' % specfile_path, specfile_path) and Gpg.verify(
                '%s.asc' % tarfile_path, tarfile_path):
            install = True
        # unverified
        else:
            if yes_to_all:
                install = True
        os.remove(tarfile_path + '.asc')
        os.remove(specfile_path + '.asc')
#   unsigned
    else:
        if yes_to_all:
            install = True
    if install:
        with closing(tarfile.open(tarfile_path, 'r')) as tar:
            tar.extractall(path=join_path(installpath, '..'))
        os.remove(tarfile_path)
        os.remove(specfile_path)
    else:
        os.remove(tarfile_path)
        os.remove(specfile_path)
        tty.warn('not installing unsigned or unverified build cache '
                 'use spack buildcache create -y option to override')


def prelocate_package(spec):
    """
    Prelocate the given package
    """
    buildinfo = read_buildinfo_file(spec)
    old_path = buildinfo['buildpath']
    for filename in buildinfo['relocate_binaries']:
        path_name = os.path.join(spec.prefix, filename)
        spack.relocate.prelocate_binary(path_name,
                                        old_path)


def relocate_package(spec):
    """
    Relocate the given package
    """
    buildinfo = read_buildinfo_file(spec)
    new_path = spack.store.layout.root
    old_path = buildinfo['buildpath']

# Need to relocate to add new compiler path to rpath
    tty.msg("Relocating package from",
            "%s to %s." % (old_path, new_path))
    installpath = install_directory_name(spec)
    for filename in buildinfo['relocate_binaries']:
        path_name = os.path.join(installpath, filename)
        spack.relocate.relocate_binary(path_name,
                                       old_path,
                                       new_path)

    for filename in buildinfo['relocate_textfiles']:
        path_name = os.path.join(installpath, filename)
        spack.relocate.relocate_text(path_name, old_path, new_path)


def get_specs():
    """
    Get spec.yaml's for build caches available on mirror
    """
    mirrors = spack.config.get_config('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of build caches.")
    path = str(spack.architecture.sys_type())
    specs = set()
    from collections import defaultdict
    durls = defaultdict(list)
    for key in mirrors:
        url = mirrors[key]
        tty.msg("Finding buildcaches on %s" % url)
        p, links = spider(url + "/build_cache")
        for link in links:
            if re.search("spec.yaml", link) and re.search(path, link):
                with Stage(link, name="build_cache", keep=True) as stage:
                    try:
                        stage.fetch()
                    except fs.FetchError:
                        next
                    with open(stage.save_filename, 'r') as f:
                        spec = spack.spec.Spec.from_yaml(f)
                        specs.add(spec)
                        durls[spec].append(link)
    return specs, durls


def get_keys(install=False, yes_to_all=False):
    """
    Get pgp public keys available on mirror
    """
    mirrors = spack.config.get_config('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of build caches.")
    for key in mirrors:
        url = mirrors[key]
        tty.msg("Finding public keys on %s" % url)
        p, links = spider(url + "/build_cache", depth=1)
        for link in links:
            if re.search("\.key", link):
                with Stage(link, name="build_cache", keep=True) as stage:
                    try:
                        stage.fetch()
                    except fs.FetchError:
                        next
                tty.msg('Found key %s' % link)
                if install:
                    if yes_to_all:
                        Gpg.trust(stage.save_filename)
                        tty.msg('Added this key to trusted keys.')
                    else:
                        answer = tty.get_yes_or_no(
                            'Add this key to trusted keys?')
                        if answer:
                            Gpg.trust(stage.save_filename)
                            tty.msg('Added this key to trusted keys.')
                        else:
                            tty.msg('Will not add this key to trusted keys.')
