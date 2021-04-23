# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import os
import re
import sys
import tarfile
import shutil
import tempfile
import hashlib
import glob
from ordereddict_backport import OrderedDict
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union  # novm

from contextlib import closing
import ruamel.yaml as yaml

import json

from six.moves.urllib.error import URLError, HTTPError

import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.cmd
import spack.config as config
import spack.database as spack_db
import spack.fetch_strategy as fs
import spack.util.file_cache as file_cache
import spack.relocate as relocate
import spack.util.gpg
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.mirror
import spack.store
import spack.util.url as url_util
import spack.util.web as web_util
from spack.caches import misc_cache_location
from spack.spec import Spec
from spack.stage import Stage


_build_cache_relative_path = 'build_cache'
_build_cache_keys_relative_path = '_pgp'


class BinaryCacheIndex(object):
    """Wraps a set of Database instances fetched from remote mirrors.

    The BinaryCacheIndex tracks what specs are available on (usually remote)
    binary caches.

    This index is "best effort", in the sense that whenever we don't find
    what we're looking for here, we will attempt to fetch it directly from
    configured mirrors anyway.  Thus, it has the potential to speed things
    up, but cache misses shouldn't break any spack functionality.

    At the moment, everything in this class is initialized as lazily as
    possible, so that it avoids slowing anything in spack down until
    absolutely necessary.

    TODO: What's the cost if, e.g., we realize in the middle of a spack
    install that the cache is out of date, and we fetch directly?  Does it
    mean we should have paid the price to update the cache earlier?
    """
    _index_contents_key = None                              # type: str
    _index_cache_root = None                                # type: str
    _index_file_cache = None                                # type: file_cache.FileCache
    _local_index_cache = None                               # type: Dict

    def __init__(self):
        # type: () -> None
        self._index_contents_key = 'contents.json'
        self._index_cache_root = binary_index_location()

        # Manages local copies of remote binary cache indices.
        self._index_file_cache = file_cache.FileCache(self._index_cache_root)

        # A map of mirror URL to index hash and cache key (index path).
        self._local_index_cache = self._init_local_index_cache()

    def _init_local_index_cache(self):
        # type: () -> Dict
        self._index_file_cache.init_entry(self._index_contents_key)
        cache_path = self._index_file_cache.cache_path(self._index_contents_key)

        if not os.path.isfile(cache_path):
            return {}
        with self._index_file_cache.read_transaction(
                self._index_contents_key) as cache_file:
            return json.load(cache_file)

    @llnl.util.lang.memoized
    def _read_local_db(self, index_path):
        # type: (str) -> spack_db.Database
        absolute_index_file_path = self._index_file_cache.cache_path(index_path)
        return spack_db.Database.from_file(absolute_index_file_path)

    def _local_mirror_dbs(self):
        # type: () -> Iterator[Tuple[str, spack_db.Database]]
        for url, cache_entry in self._local_index_cache.items():
            yield url, self._read_local_db(cache_entry['index_path'])

    def clear(self):
        # type: () -> None
        """ For testing purposes we need to be able to empty the cache and
        clear associated data structures. """
        self._read_local_db.cache.clear()
        self._index_file_cache.destroy()
        self._index_file_cache = file_cache.FileCache(self._index_cache_root)
        self._local_index_cache = self._init_local_index_cache()

    def query_remote_dbs(self, query_spec):
        # type: (Optional[Spec]) -> List[Spec]
        """Match the given maybe-concrete spec to concrete specs from mirrors.

        If ``query_spec`` is None, return all specs from all mirrors."""
        results = []
        for _url, db in self._local_mirror_dbs():
            # TODO: allow providing multiple query_specs at once!
            # TODO: allow specifying whether to match all architectures!
            results.extend(db.query(query_spec=query_spec, installed=any))
        return results

    def get_mirrors_for_spec(self, spec=None, full_hash_match=False, index_only=False):
        # type: (Optional[Spec], bool, bool) -> List[Dict[str, Union[str, Spec]]]
        """Check if a concrete spec exists on any mirrors.

        This method will *not* re-read Database instances from disk or fetch them from
        any mirror urls. However, since we assert that the provided spec must be
        concrete, we can attempt a "direct fetch" of the spec.yaml if it is not found
        within the locally cached Database instances. This direct fetch will fail
        quickly if the local dbs *were* up to date, and will succeed quickly if not
        (much more quickly than re-fetching the entire db corresponding to the mirror).

        Args:
            spec (Spec): The concrete spec to look for in binary mirrors.
            full_hash_match (bool): If True, only includes mirrors where the spec
                full hash matches the locally computed full hash of the ``spec``
                argument.  If False, any mirror which has a matching DAG hash
                is included in the results.
            index_only (bool): Do not attempt direct fetching of ``spec.yaml``
                files from remote mirrors, only consider the indices.

        Return:
            A list of objects, each containing a ``mirror_url`` and ``spec`` key
                indicating all mirrors where the spec can be found.
        """
        results = []  # type: List[Dict[str, Union[str, Spec]]]
        if spec is None:
            return results
        if not spec.concrete:
            raise TypeError('spec {0} was not concrete'.format(spec))

        def maybe_add_result(url, candidate_spec):
            # type: (str, Spec) -> None
            assert spec is not None               # mypy's local inference is not great.
            if full_hash_match and candidate_spec.full_hash() != spec.full_hash():
                return
            results.append(dict(mirror_url=url, spec=candidate_spec))

        for url, db in self._local_mirror_dbs():
            _, maybe_record = db.query_by_spec_hash(spec.dag_hash())
            if maybe_record is not None:
                maybe_add_result(url, maybe_record.spec)

        # If we found any results in the local mirror dbs, return those without
        # performing any network calls.
        if results:
            return results

        if not spack.mirror.MirrorCollection():
            tty.debug("No Spack mirrors are currently configured")
            return results

        # If we have no results, try fetching directly from the configured mirrors
        # unless index_only=True was specified.
        if index_only:
            return results
        for mirror in spack.mirror.MirrorCollection().values():
            directly_fetched = try_direct_fetch(spec, mirror)
            if directly_fetched is not None:
                maybe_add_result(mirror.fetch_url, directly_fetched)
        return results

    def _prune_old_cached_mirrors(self, configured_mirror_urls):
        # type: (Iterable[str]) -> None
        """Delete Database json files for mirrors that have been removed."""
        old_urls = set(self._local_index_cache.keys()) - set(configured_mirror_urls)

        for url in old_urls:
            cache_entry = self._local_index_cache[url]
            try:
                self._index_file_cache.remove(cache_entry['index_path'])
            except OSError as e:
                tty.debug('Local index {0} for url {1} did not exist; skipping'
                          .format(cache_entry['index_path'], url),
                          e)
            del self._local_index_cache[url]

    def refresh_mirrors(self):
        # type: () -> None
        """Point the local cache to the configured mirrors, and prune old mirror dbs."""
        # Re-read the mirror configuration.
        configured_mirror_urls = [
            mirror.fetch_url
            for mirror in spack.mirror.MirrorCollection().values()
        ]

        # Remove cached index.json files for mirrors which are no longer configured.
        self._prune_old_cached_mirrors(configured_mirror_urls)

        # Now re-fetch any updated indices for the configured URLs.
        for url in configured_mirror_urls:
            # (1) We fetch the index hash first in order to quickly no-op if the index
            # has not changed since we last fetched. The index hash is often
            # significantly smaller and quicker to download than the entire
            # index.json itself.
            try:
                fresh_hash = fetch_index_hash(url)
            except WebFailure as e:
                # If we fail to reach a configured mirror, make sure the user knows, and
                # move on to the next one. We will continue using the cached index.json
                # from before this method was called.
                tty.warn(e)
                continue

            # (2) Compare the hash to any previous entry for this url. If the hash is
            # different, clean up the old entry. If not, don't re-fetch the index or
            # re-read the Database from disk.
            existing_entry = self._local_index_cache.pop(url, None)
            if existing_entry is not None:
                # TODO: add testing for this branch!
                if existing_entry['index_hash'] == fresh_hash:
                    # Re-add the entry, since it remains valid.
                    self._local_index_cache[url] = existing_entry
                    continue
                self._index_file_cache.remove(existing_entry['index_path'])
                # self._read_local_db() memoizes Database instances, but those can take
                # up a nontrivial amount of memory. Since we know we'll need to re-fetch
                # this, delete the old entry, if there was any cached entry. This is
                # *not* necessary for correctness, because the index_path argument
                # provided to self._read_local_db() is constructed from the index hash.
                # TODO: Determine whether python actually frees memory immediately upon
                # deleting a dict entry, or whether there's anything further we need
                # to do.
                self._read_local_db.cache.pop(existing_entry['index_path'], None)

            # (3) Fetch the index and verify the hash matches. This will block on
            # synchronous network I/O. We successfully retrieved the index hash just
            # above, so we do not attempt to catch any network error.
            # TODO: do this all in parallel with subprocesses!
            index_object_str = fetch_index(url, fresh_hash)

            # (4) Calculate a filename from the hash of the url and of the downloaded
            # index.json.
            url_hash = compute_hash(url)
            cache_key = '{0}_{1}'.format(url_hash[:10], fresh_hash[:10])
            json_index_file = '{0}.json'.format(cache_key)

            # (5) Write the index.json contents to our persistent caching location.
            self._index_file_cache.init_entry(json_index_file)
            with self._index_file_cache.write_transaction(json_index_file) as (_, new):
                new.write(index_object_str)

            # (6) Point this object's registry to the newly fetched index file so that
            # the Database gets re-read from disk.
            self._local_index_cache[url] = {
                'index_hash': fresh_hash,
                'index_path': json_index_file,
            }


def binary_index_location():
    """Set up a BinaryCacheIndex for remote buildcache dbs in the user's homedir."""
    cache_root = os.path.join(misc_cache_location(), 'indices')
    cache_root = spack.util.path.canonicalize_path(cache_root)
    return cache_root


#: Singleton binary_index instance
binary_index = llnl.util.lang.Singleton(BinaryCacheIndex)


class NoOverwriteException(spack.error.SpackError):
    """
    Raised when a file exists and must be overwritten.
    """

    def __init__(self, file_path):
        err_msg = "\n%s\nexists\n" % file_path
        err_msg += "Use -f option to overwrite."
        super(NoOverwriteException, self).__init__(err_msg)


class NoGpgException(spack.error.SpackError):
    """
    Raised when gpg2 is not in PATH
    """

    def __init__(self, msg):
        super(NoGpgException, self).__init__(msg)


class NoKeyException(spack.error.SpackError):
    """
    Raised when gpg has no default key added.
    """

    def __init__(self, msg):
        super(NoKeyException, self).__init__(msg)


class PickKeyException(spack.error.SpackError):
    """
    Raised when multiple keys can be used to sign.
    """

    def __init__(self, keys):
        err_msg = "Multiple keys available for signing\n%s\n" % keys
        err_msg += "Use spack buildcache create -k <key hash> to pick a key."
        super(PickKeyException, self).__init__(err_msg)


class NoVerifyException(spack.error.SpackError):
    """
    Raised if file fails signature verification.
    """
    pass


class NoChecksumException(spack.error.SpackError):
    """
    Raised if file fails checksum verification.
    """
    pass


class NewLayoutException(spack.error.SpackError):
    """
    Raised if directory layout is different from buildcache.
    """

    def __init__(self, msg):
        super(NewLayoutException, self).__init__(msg)


def compute_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def build_cache_relative_path():
    return _build_cache_relative_path


def build_cache_keys_relative_path():
    return _build_cache_keys_relative_path


def build_cache_prefix(prefix):
    return os.path.join(prefix, build_cache_relative_path())


def buildinfo_file_name(prefix):
    """
    Filename of the binary package meta-data file
    """
    name = os.path.join(prefix, ".spack/binary_distribution")
    return name


def read_buildinfo_file(prefix):
    """
    Read buildinfo file
    """
    filename = buildinfo_file_name(prefix)
    with open(filename, 'r') as inputfile:
        content = inputfile.read()
        buildinfo = yaml.load(content)
    return buildinfo


def get_buildfile_manifest(spec):
    """
    Return a data structure with information about a build, including
    text_to_relocate, binary_to_relocate, binary_to_relocate_fullpath
    link_to_relocate, and other, which means it doesn't fit any of previous
    checks (and should not be relocated). We blacklist docs (man) and
    metadata (.spack). This can be used to find a particular kind of file
    in spack, or to generate the build metadata.
    """
    data = {"text_to_relocate": [], "binary_to_relocate": [],
            "link_to_relocate": [], "other": [],
            "binary_to_relocate_fullpath": []}

    blacklist = (".spack", "man")

    # Do this at during tarball creation to save time when tarball unpacked.
    # Used by make_package_relative to determine binaries to change.
    for root, dirs, files in os.walk(spec.prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for filename in files:
            path_name = os.path.join(root, filename)
            m_type, m_subtype = relocate.mime_type(path_name)
            rel_path_name = os.path.relpath(path_name, spec.prefix)
            added = False

            if os.path.islink(path_name):
                link = os.readlink(path_name)
                if os.path.isabs(link):
                    # Relocate absolute links into the spack tree
                    if link.startswith(spack.store.layout.root):
                        data['link_to_relocate'].append(rel_path_name)
                    added = True

            if relocate.needs_binary_relocation(m_type, m_subtype):
                if ((m_subtype in ('x-executable', 'x-sharedlib')
                    and sys.platform != 'darwin') or
                   (m_subtype in ('x-mach-binary')
                    and sys.platform == 'darwin') or
                   (not filename.endswith('.o'))):
                    data['binary_to_relocate'].append(rel_path_name)
                    data['binary_to_relocate_fullpath'].append(path_name)
                    added = True

            if relocate.needs_text_relocation(m_type, m_subtype):
                data['text_to_relocate'].append(rel_path_name)
                added = True

            if not added:
                data['other'].append(path_name)
    return data


def write_buildinfo_file(spec, workdir, rel=False):
    """
    Create a cache file containing information
    required for the relocation
    """
    manifest = get_buildfile_manifest(spec)

    prefix_to_hash = dict()
    prefix_to_hash[str(spec.package.prefix)] = spec.dag_hash()
    deps = spack.build_environment.get_rpath_deps(spec.package)
    for d in deps:
        prefix_to_hash[str(d.prefix)] = d.dag_hash()

    # Create buildinfo data and write it to disk
    import spack.hooks.sbang as sbang
    buildinfo = {}
    buildinfo['sbang_install_path'] = sbang.sbang_install_path()
    buildinfo['relative_rpaths'] = rel
    buildinfo['buildpath'] = spack.store.layout.root
    buildinfo['spackprefix'] = spack.paths.prefix
    buildinfo['relative_prefix'] = os.path.relpath(
        spec.prefix, spack.store.layout.root)
    buildinfo['relocate_textfiles'] = manifest['text_to_relocate']
    buildinfo['relocate_binaries'] = manifest['binary_to_relocate']
    buildinfo['relocate_links'] = manifest['link_to_relocate']
    buildinfo['prefix_to_hash'] = prefix_to_hash
    filename = buildinfo_file_name(workdir)
    with open(filename, 'w') as outfile:
        outfile.write(syaml.dump(buildinfo, default_flow_style=True))


def tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>/
    """
    return "%s/%s/%s-%s" % (spec.architecture,
                            str(spec.compiler).replace("@", "-"),
                            spec.name, spec.version)


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    return "%s-%s-%s-%s-%s%s" % (spec.architecture,
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


def checksum_tarball(file):
    # calculate sha256 hash of tar file
    block_size = 65536
    hasher = hashlib.sha256()
    with open(file, 'rb') as tfile:
        buf = tfile.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = tfile.read(block_size)
    return hasher.hexdigest()


def select_signing_key(key=None):
    if key is None:
        keys = spack.util.gpg.signing_keys()
        if len(keys) == 1:
            key = keys[0]

        if len(keys) > 1:
            raise PickKeyException(str(keys))

        if len(keys) == 0:
            raise NoKeyException(
                "No default key available for signing.\n"
                "Use spack gpg init and spack gpg create"
                " to create a default key.")
    return key


def sign_tarball(key, force, specfile_path):
    if os.path.exists('%s.asc' % specfile_path):
        if force:
            os.remove('%s.asc' % specfile_path)
        else:
            raise NoOverwriteException('%s.asc' % specfile_path)

    key = select_signing_key(key)
    spack.util.gpg.sign(key, specfile_path, '%s.asc' % specfile_path)


def generate_package_index(cache_prefix):
    """Create the build cache index page.

    Creates (or replaces) the "index.json" page at the location given in
    cache_prefix.  This page contains a link for each binary package (.yaml)
    under cache_prefix.
    """
    tmpdir = tempfile.mkdtemp()
    db_root_dir = os.path.join(tmpdir, 'db_root')
    db = spack_db.Database(None, db_dir=db_root_dir,
                           enable_transaction_locking=False,
                           record_fields=['spec', 'ref_count'])

    try:
        file_list = (
            entry
            for entry in web_util.list_url(cache_prefix)
            if entry.endswith('.yaml'))
    except KeyError as inst:
        msg = 'No packages at {0}: {1}'.format(cache_prefix, inst)
        tty.warn(msg)
        return
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = 'Encountered problem listing packages at {0}: {1}'.format(
            cache_prefix, err)
        tty.warn(msg)
        return

    tty.debug('Retrieving spec.yaml files from {0} to build index'.format(
        cache_prefix))
    for file_path in file_list:
        try:
            yaml_url = url_util.join(cache_prefix, file_path)
            tty.debug('fetching {0}'.format(yaml_url))
            _, _, yaml_file = web_util.read_from_url(yaml_url)
            yaml_contents = codecs.getreader('utf-8')(yaml_file).read()
            s = Spec.from_yaml(yaml_contents)
            db.add(s, None)
        except (URLError, web_util.SpackWebError) as url_err:
            tty.error('Error reading spec.yaml: {0}'.format(file_path))
            tty.error(url_err)

    try:
        index_json_path = os.path.join(db_root_dir, 'index.json')
        with open(index_json_path, 'w') as f:
            db._write_to_file(f)

        # Read the index back in and compute it's hash
        with open(index_json_path) as f:
            index_string = f.read()
            index_hash = compute_hash(index_string)

        # Write the hash out to a local file
        index_hash_path = os.path.join(db_root_dir, 'index.json.hash')
        with open(index_hash_path, 'w') as f:
            f.write(index_hash)

        # Push the index itself
        web_util.push_to_url(
            index_json_path,
            url_util.join(cache_prefix, 'index.json'),
            keep_original=False,
            extra_args={'ContentType': 'application/json'})

        # Push the hash
        web_util.push_to_url(
            index_hash_path,
            url_util.join(cache_prefix, 'index.json.hash'),
            keep_original=False,
            extra_args={'ContentType': 'text/plain'})
    except Exception as err:
        msg = 'Encountered problem pushing package index to {0}: {1}'.format(
            cache_prefix, err)
        tty.warn(msg)
    finally:
        shutil.rmtree(tmpdir)


def generate_key_index(key_prefix, tmpdir=None):
    """Create the key index page.

    Creates (or replaces) the "index.json" page at the location given in
    key_prefix.  This page contains an entry for each key (.pub) under
    key_prefix.
    """

    tty.debug(' '.join(('Retrieving key.pub files from',
                        url_util.format(key_prefix),
                        'to build key index')))

    try:
        fingerprints = (
            entry[:-4]
            for entry in web_util.list_url(key_prefix, recursive=False)
            if entry.endswith('.pub'))
    except KeyError as inst:
        msg = 'No keys at {0}: {1}'.format(key_prefix, inst)
        tty.warn(msg)
        return
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = 'Encountered problem listing keys at {0}: {1}'.format(
            key_prefix, err)
        tty.warn(msg)
        return

    remove_tmpdir = False

    keys_local = url_util.local_file_path(key_prefix)
    if keys_local:
        target = os.path.join(keys_local, 'index.json')
    else:
        if not tmpdir:
            tmpdir = tempfile.mkdtemp()
            remove_tmpdir = True
        target = os.path.join(tmpdir, 'index.json')

    index = {
        'keys': dict(
            (fingerprint, {}) for fingerprint
            in sorted(set(fingerprints)))
    }
    with open(target, 'w') as f:
        sjson.dump(index, f)

    if not keys_local:
        try:
            web_util.push_to_url(
                target,
                url_util.join(key_prefix, 'index.json'),
                keep_original=False,
                extra_args={'ContentType': 'application/json'})
        except Exception as err:
            msg = 'Encountered problem pushing key index to {0}: {1}'.format(
                key_prefix, err)
            tty.warn(msg)
        finally:
            if remove_tmpdir:
                shutil.rmtree(tmpdir)


def build_tarball(spec, outdir, force=False, rel=False, unsigned=False,
                  allow_root=False, key=None, regenerate_index=False):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    if not spec.concrete:
        raise ValueError('spec must be concrete to build tarball')

    # set up some paths
    tmpdir = tempfile.mkdtemp()
    cache_prefix = build_cache_prefix(tmpdir)

    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_dir = os.path.join(cache_prefix, tarball_directory_name(spec))
    tarfile_path = os.path.join(tarfile_dir, tarfile_name)
    spackfile_path = os.path.join(
        cache_prefix, tarball_path_name(spec, '.spack'))

    remote_spackfile_path = url_util.join(
        outdir, os.path.relpath(spackfile_path, tmpdir))

    mkdirp(tarfile_dir)
    if web_util.url_exists(remote_spackfile_path):
        if force:
            web_util.remove_url(remote_spackfile_path)
        else:
            raise NoOverwriteException(url_util.format(remote_spackfile_path))

    # need to copy the spec file so the build cache can be downloaded
    # without concretizing with the current spack packages
    # and preferences
    spec_file = os.path.join(spec.prefix, ".spack", "spec.yaml")
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.realpath(
        os.path.join(cache_prefix, specfile_name))

    remote_specfile_path = url_util.join(
        outdir, os.path.relpath(specfile_path, os.path.realpath(tmpdir)))

    if web_util.url_exists(remote_specfile_path):
        if force:
            web_util.remove_url(remote_specfile_path)
        else:
            raise NoOverwriteException(url_util.format(remote_specfile_path))

    # make a copy of the install directory to work with
    workdir = os.path.join(tmpdir, os.path.basename(spec.prefix))
    # install_tree copies hardlinks
    # create a temporary tarfile from prefix and exract it to workdir
    # tarfile preserves hardlinks
    temp_tarfile_name = tarball_name(spec, '.tar')
    temp_tarfile_path = os.path.join(tarfile_dir, temp_tarfile_name)
    with closing(tarfile.open(temp_tarfile_path, 'w')) as tar:
        tar.add(name='%s' % spec.prefix,
                arcname='.')
    with closing(tarfile.open(temp_tarfile_path, 'r')) as tar:
        tar.extractall(workdir)
    os.remove(temp_tarfile_path)

    # create info for later relocation and create tar
    write_buildinfo_file(spec, workdir, rel)

    # optionally make the paths in the binaries relative to each other
    # in the spack install tree before creating tarball
    if rel:
        try:
            make_package_relative(workdir, spec, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            shutil.rmtree(tmpdir)
            tty.die(e)
    else:
        try:
            check_package_relocatable(workdir, spec, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            shutil.rmtree(tmpdir)
            tty.die(e)

    # create gzip compressed tarball of the install prefix
    with closing(tarfile.open(tarfile_path, 'w:gz')) as tar:
        tar.add(name='%s' % workdir,
                arcname='%s' % os.path.basename(spec.prefix))
    # remove copy of install directory
    shutil.rmtree(workdir)

    # get the sha256 checksum of the tarball
    checksum = checksum_tarball(tarfile_path)

    # add sha256 checksum to spec.yaml
    with open(spec_file, 'r') as inputfile:
        content = inputfile.read()
        spec_dict = yaml.load(content)
    bchecksum = {}
    bchecksum['hash_algorithm'] = 'sha256'
    bchecksum['hash'] = checksum
    spec_dict['binary_cache_checksum'] = bchecksum
    # Add original install prefix relative to layout root to spec.yaml.
    # This will be used to determine is the directory layout has changed.
    buildinfo = {}
    buildinfo['relative_prefix'] = os.path.relpath(
        spec.prefix, spack.store.layout.root)
    buildinfo['relative_rpaths'] = rel
    spec_dict['buildinfo'] = buildinfo

    with open(specfile_path, 'w') as outfile:
        outfile.write(syaml.dump(spec_dict))

    # sign the tarball and spec file with gpg
    if not unsigned:
        key = select_signing_key(key)
        sign_tarball(key, force, specfile_path)

    # put tarball, spec and signature files in .spack archive
    with closing(tarfile.open(spackfile_path, 'w')) as tar:
        tar.add(name=tarfile_path, arcname='%s' % tarfile_name)
        tar.add(name=specfile_path, arcname='%s' % specfile_name)
        if not unsigned:
            tar.add(name='%s.asc' % specfile_path,
                    arcname='%s.asc' % specfile_name)

    # cleanup file moved to archive
    os.remove(tarfile_path)
    if not unsigned:
        os.remove('%s.asc' % specfile_path)

    web_util.push_to_url(
        spackfile_path, remote_spackfile_path, keep_original=False)
    web_util.push_to_url(
        specfile_path, remote_specfile_path, keep_original=False)

    tty.debug('Buildcache for "{0}" written to \n {1}'
              .format(spec, remote_spackfile_path))

    try:
        # push the key to the build cache's _pgp directory so it can be
        # imported
        if not unsigned:
            push_keys(outdir,
                      keys=[key],
                      regenerate_index=regenerate_index,
                      tmpdir=tmpdir)

        # create an index.json for the build_cache directory so specs can be
        # found
        if regenerate_index:
            generate_package_index(url_util.join(
                outdir, os.path.relpath(cache_prefix, tmpdir)))
    finally:
        shutil.rmtree(tmpdir)

    return None


def download_tarball(spec, preferred_mirrors=None):
    """
    Download binary tarball for given package into stage area, returning
    path to downloaded tarball if successful, None otherwise.

    Args:
        spec (Spec): Concrete spec
        preferred_mirrors (list): If provided, this is a list of preferred
        mirror urls.  Other configured mirrors will only be used if the
        tarball can't be retrieved from one of these.

    Returns:
        Path to the downloaded tarball, or ``None`` if the tarball could not
            be downloaded from any configured mirrors.
    """
    if not spack.mirror.MirrorCollection():
        tty.die("Please add a spack mirror to allow " +
                "download of pre-compiled packages.")

    tarball = tarball_path_name(spec, '.spack')

    urls_to_try = []

    if preferred_mirrors:
        for preferred_url in preferred_mirrors:
            urls_to_try.append(url_util.join(
                preferred_url, _build_cache_relative_path, tarball))

    for mirror in spack.mirror.MirrorCollection().values():
        if not preferred_mirrors or mirror.fetch_url not in preferred_mirrors:
            urls_to_try.append(url_util.join(
                mirror.fetch_url, _build_cache_relative_path, tarball))

    for try_url in urls_to_try:
        # stage the tarball into standard place
        stage = Stage(try_url, name="build_cache", keep=True)
        stage.create()
        try:
            stage.fetch()
            return stage.save_filename
        except fs.FetchError:
            continue

    tty.warn("download_tarball() was unable to download " +
             "{0} from any configured mirrors".format(spec))
    return None


def make_package_relative(workdir, spec, allow_root):
    """
    Change paths in binaries to relative paths. Change absolute symlinks
    to relative symlinks.
    """
    prefix = spec.prefix
    buildinfo = read_buildinfo_file(workdir)
    old_layout_root = buildinfo['buildpath']
    orig_path_names = list()
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        orig_path_names.append(os.path.join(prefix, filename))
        cur_path_names.append(os.path.join(workdir, filename))

    platform = spack.architecture.get_platform(spec.platform)
    if 'macho' in platform.binary_formats:
        relocate.make_macho_binaries_relative(
            cur_path_names, orig_path_names, old_layout_root)

    if 'elf' in platform.binary_formats:
        relocate.make_elf_binaries_relative(
            cur_path_names, orig_path_names, old_layout_root)

    relocate.raise_if_not_relocatable(cur_path_names, allow_root)
    orig_path_names = list()
    cur_path_names = list()
    for linkname in buildinfo.get('relocate_links', []):
        orig_path_names.append(os.path.join(prefix, linkname))
        cur_path_names.append(os.path.join(workdir, linkname))
    relocate.make_link_relative(cur_path_names, orig_path_names)


def check_package_relocatable(workdir, spec, allow_root):
    """
    Check if package binaries are relocatable.
    Change links to placeholder links.
    """
    buildinfo = read_buildinfo_file(workdir)
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.raise_if_not_relocatable(cur_path_names, allow_root)


def relocate_package(spec, allow_root):
    """
    Relocate the given package
    """
    import spack.hooks.sbang as sbang

    workdir = str(spec.prefix)
    buildinfo = read_buildinfo_file(workdir)
    new_layout_root = str(spack.store.layout.root)
    new_prefix = str(spec.prefix)
    new_rel_prefix = str(os.path.relpath(new_prefix, new_layout_root))
    new_spack_prefix = str(spack.paths.prefix)

    old_sbang_install_path = None
    if 'sbang_install_path' in buildinfo:
        old_sbang_install_path = str(buildinfo['sbang_install_path'])
    old_layout_root = str(buildinfo['buildpath'])
    old_spack_prefix = str(buildinfo.get('spackprefix'))
    old_rel_prefix = buildinfo.get('relative_prefix')
    old_prefix = os.path.join(old_layout_root, old_rel_prefix)
    rel = buildinfo.get('relative_rpaths')
    prefix_to_hash = buildinfo.get('prefix_to_hash', None)
    if (old_rel_prefix != new_rel_prefix and not prefix_to_hash):
        msg = "Package tarball was created from an install "
        msg += "prefix with a different directory layout and an older "
        msg += "buildcache create implementation. It cannot be relocated."
        raise NewLayoutException(msg)
    # older buildcaches do not have the prefix_to_hash dictionary
    # need to set an empty dictionary and add one entry to
    # prefix_to_prefix to reproduce the old behavior
    if not prefix_to_hash:
        prefix_to_hash = dict()
    hash_to_prefix = dict()
    hash_to_prefix[spec.format('{hash}')] = str(spec.package.prefix)
    new_deps = spack.build_environment.get_rpath_deps(spec.package)
    for d in new_deps:
        hash_to_prefix[d.format('{hash}')] = str(d.prefix)
    # Spurious replacements (e.g. sbang) will cause issues with binaries
    # For example, the new sbang can be longer than the old one.
    # Hence 2 dictionaries are maintained here.
    prefix_to_prefix_text = OrderedDict({})
    prefix_to_prefix_bin = OrderedDict({})

    if old_sbang_install_path:
        prefix_to_prefix_text[old_sbang_install_path] = sbang.sbang_install_path()

    prefix_to_prefix_text[old_prefix] = new_prefix
    prefix_to_prefix_bin[old_prefix] = new_prefix
    prefix_to_prefix_text[old_layout_root] = new_layout_root
    prefix_to_prefix_bin[old_layout_root] = new_layout_root
    for orig_prefix, hash in prefix_to_hash.items():
        prefix_to_prefix_text[orig_prefix] = hash_to_prefix.get(hash, None)
        prefix_to_prefix_bin[orig_prefix] = hash_to_prefix.get(hash, None)
    # This is vestigial code for the *old* location of sbang. Previously,
    # sbang was a bash script, and it lived in the spack prefix. It is
    # now a POSIX script that lives in the install prefix. Old packages
    # will have the old sbang location in their shebangs.
    orig_sbang = '#!/bin/bash {0}/bin/sbang'.format(old_spack_prefix)
    new_sbang = sbang.sbang_shebang_line()
    prefix_to_prefix_text[orig_sbang] = new_sbang

    tty.debug("Relocating package from",
              "%s to %s." % (old_layout_root, new_layout_root))

    def is_backup_file(file):
        return file.endswith('~')

    # Text files containing the prefix text
    text_names = list()
    for filename in buildinfo['relocate_textfiles']:
        text_name = os.path.join(workdir, filename)
        # Don't add backup files generated by filter_file during install step.
        if not is_backup_file(text_name):
            text_names.append(text_name)

    # If we are not installing back to the same install tree do the relocation
    if old_layout_root != new_layout_root:
        files_to_relocate = [os.path.join(workdir, filename)
                             for filename in buildinfo.get('relocate_binaries')
                             ]
        # If the buildcache was not created with relativized rpaths
        # do the relocation of path in binaries
        platform = spack.architecture.get_platform(spec.platform)
        if 'macho' in platform.binary_formats:
            relocate.relocate_macho_binaries(files_to_relocate,
                                             old_layout_root,
                                             new_layout_root,
                                             prefix_to_prefix_bin, rel,
                                             old_prefix,
                                             new_prefix)
        if 'elf' in platform.binary_formats:
            relocate.relocate_elf_binaries(files_to_relocate,
                                           old_layout_root,
                                           new_layout_root,
                                           prefix_to_prefix_bin, rel,
                                           old_prefix,
                                           new_prefix)
            # Relocate links to the new install prefix
            links = [link for link in buildinfo.get('relocate_links', [])]
            relocate.relocate_links(
                links, old_layout_root, old_prefix, new_prefix
            )

        # For all buildcaches
        # relocate the install prefixes in text files including dependencies
        relocate.relocate_text(text_names, prefix_to_prefix_text)

        paths_to_relocate = [old_prefix, old_layout_root]
        paths_to_relocate.extend(prefix_to_hash.keys())
        files_to_relocate = list(filter(
            lambda pathname: not relocate.file_is_relocatable(
                pathname, paths_to_relocate=paths_to_relocate),
            map(lambda filename: os.path.join(workdir, filename),
                buildinfo['relocate_binaries'])))
        # relocate the install prefixes in binary files including dependencies
        relocate.relocate_text_bin(files_to_relocate, prefix_to_prefix_bin)

    # If we are installing back to the same location
    # relocate the sbang location if the spack directory changed
    else:
        if old_spack_prefix != new_spack_prefix:
            relocate.relocate_text(text_names, prefix_to_prefix_text)


def extract_tarball(spec, filename, allow_root=False, unsigned=False,
                    force=False):
    """
    extract binary tarball for given package into install area
    """
    if os.path.exists(spec.prefix):
        if force:
            shutil.rmtree(spec.prefix)
        else:
            raise NoOverwriteException(str(spec.prefix))

    tmpdir = tempfile.mkdtemp()
    stagepath = os.path.dirname(filename)
    spackfile_name = tarball_name(spec, '.spack')
    spackfile_path = os.path.join(stagepath, spackfile_name)
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_path = os.path.join(tmpdir, tarfile_name)
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.join(tmpdir, specfile_name)

    with closing(tarfile.open(spackfile_path, 'r')) as tar:
        tar.extractall(tmpdir)
    # some buildcache tarfiles use bzip2 compression
    if not os.path.exists(tarfile_path):
        tarfile_name = tarball_name(spec, '.tar.bz2')
        tarfile_path = os.path.join(tmpdir, tarfile_name)
    if not unsigned:
        if os.path.exists('%s.asc' % specfile_path):
            try:
                suppress = config.get('config:suppress_gpg_warnings', False)
                spack.util.gpg.verify(
                    '%s.asc' % specfile_path, specfile_path, suppress)
            except Exception as e:
                shutil.rmtree(tmpdir)
                raise e
        else:
            shutil.rmtree(tmpdir)
            raise NoVerifyException(
                "Package spec file failed signature verification.\n"
                "Use spack buildcache keys to download "
                "and install a key for verification from the mirror.")
    # get the sha256 checksum of the tarball
    checksum = checksum_tarball(tarfile_path)

    # get the sha256 checksum recorded at creation
    spec_dict = {}
    with open(specfile_path, 'r') as inputfile:
        content = inputfile.read()
        spec_dict = syaml.load(content)
    bchecksum = spec_dict['binary_cache_checksum']

    # if the checksums don't match don't install
    if bchecksum['hash'] != checksum:
        shutil.rmtree(tmpdir)
        raise NoChecksumException(
            "Package tarball failed checksum verification.\n"
            "It cannot be installed.")

    new_relative_prefix = str(os.path.relpath(spec.prefix,
                                              spack.store.layout.root))
    # if the original relative prefix is in the spec file use it
    buildinfo = spec_dict.get('buildinfo', {})
    old_relative_prefix = buildinfo.get('relative_prefix', new_relative_prefix)
    rel = buildinfo.get('relative_rpaths')
    # if the original relative prefix and new relative prefix differ the
    # directory layout has changed and the  buildcache cannot be installed
    # if it was created with relative rpaths
    info = 'old relative prefix %s\nnew relative prefix %s\nrelative rpaths %s'
    tty.debug(info %
              (old_relative_prefix, new_relative_prefix, rel))

    # extract the tarball in a temp directory
    with closing(tarfile.open(tarfile_path, 'r')) as tar:
        tar.extractall(path=tmpdir)
    # get the parent directory of the file .spack/binary_distribution
    # this should the directory unpacked from the tarball whose
    # name is unknown because the prefix naming is unknown
    bindist_file = glob.glob('%s/*/.spack/binary_distribution' % tmpdir)[0]
    workdir = re.sub('/.spack/binary_distribution$', '', bindist_file)
    tty.debug('workdir %s' % workdir)
    # install_tree copies hardlinks
    # create a temporary tarfile from prefix and exract it to workdir
    # tarfile preserves hardlinks
    temp_tarfile_name = tarball_name(spec, '.tar')
    temp_tarfile_path = os.path.join(tmpdir, temp_tarfile_name)
    with closing(tarfile.open(temp_tarfile_path, 'w')) as tar:
        tar.add(name='%s' % workdir,
                arcname='.')
    with closing(tarfile.open(temp_tarfile_path, 'r')) as tar:
        tar.extractall(spec.prefix)
    os.remove(temp_tarfile_path)

    # cleanup
    os.remove(tarfile_path)
    os.remove(specfile_path)

    try:
        relocate_package(spec, allow_root)
    except Exception as e:
        shutil.rmtree(spec.prefix)
        raise e
    else:
        manifest_file = os.path.join(spec.prefix,
                                     spack.store.layout.metadata_dir,
                                     spack.store.layout.manifest_file_name)
        if not os.path.exists(manifest_file):
            spec_id = spec.format('{name}/{hash:7}')
            tty.warn('No manifest file in tarball for spec %s' % spec_id)
    finally:
        shutil.rmtree(tmpdir)
        if os.path.exists(filename):
            os.remove(filename)


def try_direct_fetch(spec, mirror):
    # type: (Spec, spack.mirror.Mirror) -> Optional[Spec]
    """Fetch a concrete spec's spec.yaml from the given mirror.

    Return None if it cannot be found on the mirror."""
    if not spec.concrete:
        raise TypeError('spec {0} was not concrete'.format(spec))

    specfile_name = tarball_name(spec, '.spec.yaml')
    buildcache_fetch_url = url_util.join(
        mirror.fetch_url, _build_cache_relative_path, specfile_name)

    try:
        _, _, fs = web_util.read_from_url(buildcache_fetch_url)
        fetched_spec_yaml = codecs.getreader('utf-8')(fs).read()
    except (URLError, web_util.SpackWebError, HTTPError) as url_err:
        tty.debug('Did not find {0} on {1}'.format(specfile_name, buildcache_fetch_url),
                  url_err)
        return None

    fetched_spec = Spec.from_yaml(fetched_spec_yaml)
    # TODO: Spec.from_yaml() should really be able to detect whether a spec.yaml is
    # already concrete instead of having to invoke a private method here.
    fetched_spec._mark_concrete()

    return fetched_spec


class WebFailure(Exception):
    """An internal error due to network failure."""

    def __init__(self, msg, base):
        merged = '{0}: {1}'.format(msg, base)
        super(WebFailure, self).__init__(merged)


class InvalidIndexHash(Exception):
    """An index did not match an expected checksum."""

    def __init__(self, expected, received, entity_description, msg):
        merged = 'expected checksum {0} for {1}, but received {2}: {3}'.format(
            expected, entity_description, received, msg)
        super(InvalidIndexHash, self).__init__(merged)


def fetch_index_hash(mirror_url):
    # type: (str) -> str
    """Fetch a checksum for an index from a mirror."""
    hash_fetch_url = url_util.join(
        mirror_url, _build_cache_relative_path, 'index.json.hash')

    tty.debug('Fetching hash for index from {0}'.format(hash_fetch_url))

    try:
        _, _, fs = web_util.read_from_url(hash_fetch_url)
    except (URLError, web_util.SpackWebError) as e:
        raise WebFailure('Unable to read index hash {0}'.format(hash_fetch_url), e)
    return codecs.getreader('utf-8')(fs).read()


def fetch_index(mirror_url, expect_hash):
    # type: (str, str) -> str
    """Fetch an index from a mirror and validate its checksum."""
    index_fetch_url = url_util.join(
        mirror_url, _build_cache_relative_path, 'index.json')

    tty.debug('Fetching index from {0}'.format(index_fetch_url))

    try:
        _, _, fs = web_util.read_from_url(index_fetch_url)
        index_object_str = codecs.getreader('utf-8')(fs).read()
    except (URLError, web_util.SpackWebError) as e:
        raise WebFailure('Unable to read index {0}'.format(index_fetch_url), e)

    locally_computed_hash = compute_hash(index_object_str)

    if locally_computed_hash != expect_hash:
        raise InvalidIndexHash(expect_hash, locally_computed_hash,
                               'remote index at {0}'.format(mirror_url),
                               'this indicates an error in index tranmission')

    return index_object_str


def clear_spec_cache():
    binary_index.clear()


def get_keys(install=False, trust=False, force=False, mirrors=None):
    """Get pgp public keys available on mirror with suffix .pub
    """
    mirror_collection = (mirrors or spack.mirror.MirrorCollection())

    if not mirror_collection:
        tty.die("Please add a spack mirror to allow " +
                "download of build caches.")

    for mirror in mirror_collection.values():
        fetch_url = mirror.fetch_url
        keys_url = url_util.join(fetch_url,
                                 _build_cache_relative_path,
                                 _build_cache_keys_relative_path)
        keys_index = url_util.join(keys_url, 'index.json')

        tty.debug('Finding public keys in {0}'.format(
            url_util.format(fetch_url)))

        try:
            _, _, json_file = web_util.read_from_url(keys_index)
            json_index = sjson.load(codecs.getreader('utf-8')(json_file))
        except (URLError, web_util.SpackWebError) as url_err:
            if web_util.url_exists(keys_index):
                err_msg = [
                    'Unable to find public keys in {0},',
                    ' caught exception attempting to read from {1}.',
                ]

                tty.error(''.join(err_msg).format(
                    url_util.format(fetch_url),
                    url_util.format(keys_index)))

                tty.debug(url_err)

            continue

        for fingerprint, key_attributes in json_index['keys'].items():
            link = os.path.join(keys_url, fingerprint + '.pub')

            with Stage(link, name="build_cache", keep=True) as stage:
                if os.path.exists(stage.save_filename) and force:
                    os.remove(stage.save_filename)
                if not os.path.exists(stage.save_filename):
                    try:
                        stage.fetch()
                    except fs.FetchError:
                        continue

            tty.debug('Found key {0}'.format(fingerprint))
            if install:
                if trust:
                    spack.util.gpg.trust(stage.save_filename)
                    tty.debug('Added this key to trusted keys.')
                else:
                    tty.debug('Will not add this key to trusted keys.'
                              'Use -t to install all downloaded keys')


def push_keys(*mirrors, **kwargs):
    """
    Upload pgp public keys to the given mirrors
    """
    keys = kwargs.get('keys')
    regenerate_index = kwargs.get('regenerate_index', False)
    tmpdir = kwargs.get('tmpdir')
    remove_tmpdir = False

    keys = spack.util.gpg.public_keys(*(keys or []))

    try:
        for mirror in mirrors:
            push_url = getattr(mirror, 'push_url', mirror)
            keys_url = url_util.join(push_url,
                                     _build_cache_relative_path,
                                     _build_cache_keys_relative_path)
            keys_local = url_util.local_file_path(keys_url)

            verb = 'Writing' if keys_local else 'Uploading'
            tty.debug('{0} public keys to {1}'.format(
                verb, url_util.format(push_url)))

            if keys_local:  # mirror is local, don't bother with the tmpdir
                prefix = keys_local
                mkdirp(keys_local)
            else:
                # A tmp dir is created for the first mirror that is non-local.
                # On the off-hand chance that all the mirrors are local, then
                # we can avoid the need to create a tmp dir.
                if tmpdir is None:
                    tmpdir = tempfile.mkdtemp()
                    remove_tmpdir = True
                prefix = tmpdir

            for fingerprint in keys:
                tty.debug('    ' + fingerprint)
                filename = fingerprint + '.pub'

                export_target = os.path.join(prefix, filename)
                spack.util.gpg.export_keys(export_target, fingerprint)

                # If mirror is local, the above export writes directly to the
                # mirror (export_target points directly to the mirror).
                #
                # If not, then export_target is a tmpfile that needs to be
                # uploaded to the mirror.
                if not keys_local:
                    spack.util.web.push_to_url(
                        export_target,
                        url_util.join(keys_url, filename),
                        keep_original=False)

            if regenerate_index:
                if keys_local:
                    generate_key_index(keys_url)
                else:
                    generate_key_index(keys_url, tmpdir)
    finally:
        if remove_tmpdir:
            shutil.rmtree(tmpdir)


def needs_rebuild(spec, mirror_url, rebuild_on_errors=False):
    if not spec.concrete:
        raise ValueError('spec must be concrete to check against mirror')

    pkg_name = spec.name
    pkg_version = spec.version

    pkg_hash = spec.dag_hash()
    pkg_full_hash = spec.full_hash()

    tty.debug('Checking {0}-{1}, dag_hash = {2}, full_hash = {3}'.format(
        pkg_name, pkg_version, pkg_hash, pkg_full_hash))
    tty.debug(spec.tree())

    # Try to retrieve the .spec.yaml directly, based on the known
    # format of the name, in order to determine if the package
    # needs to be rebuilt.
    cache_prefix = build_cache_prefix(mirror_url)
    spec_yaml_file_name = tarball_name(spec, '.spec.yaml')
    file_path = os.path.join(cache_prefix, spec_yaml_file_name)

    result_of_error = 'Package ({0}) will {1}be rebuilt'.format(
        spec.short_spec, '' if rebuild_on_errors else 'not ')

    try:
        _, _, yaml_file = web_util.read_from_url(file_path)
        yaml_contents = codecs.getreader('utf-8')(yaml_file).read()
    except (URLError, web_util.SpackWebError) as url_err:
        err_msg = [
            'Unable to determine whether {0} needs rebuilding,',
            ' caught exception attempting to read from {1}.',
        ]
        tty.error(''.join(err_msg).format(spec.short_spec, file_path))
        tty.debug(url_err)
        tty.warn(result_of_error)
        return rebuild_on_errors

    if not yaml_contents:
        tty.error('Reading {0} returned nothing'.format(file_path))
        tty.warn(result_of_error)
        return rebuild_on_errors

    spec_yaml = syaml.load(yaml_contents)

    yaml_spec = spec_yaml['spec']
    name = spec.name

    # The "spec" key in the yaml is a list of objects, each with a single
    # key that is the package name.  While the list usually just contains
    # a single object, we iterate over the list looking for the object
    # with the name of this concrete spec as a key, out of an abundance
    # of caution.
    cached_pkg_specs = [item[name] for item in yaml_spec if name in item]
    cached_target = cached_pkg_specs[0] if cached_pkg_specs else None

    # If either the full_hash didn't exist in the .spec.yaml file, or it
    # did, but didn't match the one we computed locally, then we should
    # just rebuild.  This can be simplified once the dag_hash and the
    # full_hash become the same thing.
    rebuild = False
    if not cached_target or 'full_hash' not in cached_target:
        reason = 'full_hash was missing from remote spec.yaml'
        rebuild = True
    else:
        full_hash = cached_target['full_hash']
        if full_hash != pkg_full_hash:
            reason = 'hash mismatch, remote = {0}, local = {1}'.format(
                full_hash, pkg_full_hash)
            rebuild = True

    if rebuild:
        tty.msg('Rebuilding {0}, reason: {1}'.format(
            spec.short_spec, reason))
        tty.msg(spec.tree())

    return rebuild


def check_specs_against_mirrors(mirrors, specs, output_file=None,
                                rebuild_on_errors=False):
    """Check all the given specs against buildcaches on the given mirrors and
    determine if any of the specs need to be rebuilt.  Reasons for needing to
    rebuild include binary cache for spec isn't present on a mirror, or it is
    present but the full_hash has changed since last time spec was built.

    Arguments:
        mirrors (dict): Mirrors to check against
        specs (iterable): Specs to check against mirrors
        output_file (string): Path to output file to be written.  If provided,
            mirrors with missing or out-of-date specs will be formatted as a
            JSON object and written to this file.
        rebuild_on_errors (boolean): Treat any errors encountered while
            checking specs as a signal to rebuild package.

    Returns: 1 if any spec was out-of-date on any mirror, 0 otherwise.

    """
    rebuilds = {}
    for mirror in spack.mirror.MirrorCollection(mirrors).values():
        tty.debug('Checking for built specs at {0}'.format(mirror.fetch_url))

        rebuild_list = []

        for spec in specs:
            if needs_rebuild(spec, mirror.fetch_url, rebuild_on_errors):
                rebuild_list.append({
                    'short_spec': spec.short_spec,
                    'hash': spec.dag_hash()
                })

        if rebuild_list:
            rebuilds[mirror.fetch_url] = {
                'mirrorName': mirror.name,
                'mirrorUrl': mirror.fetch_url,
                'rebuildSpecs': rebuild_list
            }

    if output_file:
        with open(output_file, 'w') as outf:
            outf.write(json.dumps(rebuilds))

    return 1 if rebuilds else 0


def _download_buildcache_entry(mirror_root, descriptions):
    for description in descriptions:
        description_url = os.path.join(mirror_root, description['url'])
        path = description['path']
        fail_if_missing = description['required']

        mkdirp(path)

        stage = Stage(
            description_url, name="build_cache", path=path, keep=True)

        try:
            stage.fetch()
        except fs.FetchError as e:
            tty.debug(e)
            if fail_if_missing:
                tty.error('Failed to download required url {0}'.format(
                    description_url))
                return False

    return True


def download_buildcache_entry(file_descriptions, mirror_url=None):
    if not mirror_url and not spack.mirror.MirrorCollection():
        tty.die("Please provide or add a spack mirror to allow " +
                "download of buildcache entries.")

    if mirror_url:
        mirror_root = os.path.join(
            mirror_url, _build_cache_relative_path)
        return _download_buildcache_entry(mirror_root, file_descriptions)

    for mirror in spack.mirror.MirrorCollection().values():
        mirror_root = os.path.join(
            mirror.fetch_url,
            _build_cache_relative_path)

        if _download_buildcache_entry(mirror_root, file_descriptions):
            return True
        else:
            continue

    return False
