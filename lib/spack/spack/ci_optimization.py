# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from compat import Mapping, Sequence

import copy
import hashlib

import spack.util.spack_yaml as syaml


def sort_yaml_obj(obj):
    if isinstance(obj, Mapping):
        return syaml.syaml_dict(
            (k, sort_yaml_obj(v))
            for k, v in
            sorted(obj.items(), key=(lambda item: str(item[0]))))

    if isinstance(obj, Sequence) and not isinstance(obj, str):
        return syaml.syaml_list(sort_yaml_obj(x) for x in obj)

    return obj


def matches(obj, proto):
    """Returns True if the test object "obj" matches the prototype object
    "proto".

    If obj and proto are mappings, obj matches proto if (key in obj) and
    (obj[key] matches proto[key]) for every key in proto.

    If obj and proto are sequences, obj matches proto if they are of the same
    length and (a matches b) for every (a,b) in zip(obj, proto).

    Otherwise, obj matches proto if obj == proto.

    Precondition: proto must not have any reference cycles
    """
    if isinstance(obj, Mapping):
        if not isinstance(proto, Mapping):
            return False

        return all(
            (key in obj and matches(obj[key], val))
            for key, val in proto.items()
        )

    if (isinstance(obj, Sequence) and
            not isinstance(obj, str)):

        if not (isinstance(proto, Sequence) and
                not isinstance(proto, str)):
            return False

        if len(obj) != len(proto):
            return False

        return all(
            matches(obj[index], val)
            for index, val in enumerate(proto)
        )

    return obj == proto


def subkeys(obj, proto):
    """Returns the test mapping "obj" after factoring out the items it has in
    common with the prototype mapping "proto".

    Consider a recursive merge operation, merge(a, b) on mappings a and b, that
    returns a mapping, m, whose keys are the union of the keys of a and b, and
    for every such key, "k", its corresponding value is:

      - merge(a[key], b[key])  if a[key] and b[key] are mappings, or
      - b[key]                 if (key in b) and not matches(a[key], b[key]),
                               or
      - a[key]                 otherwise


    If obj and proto are mappings, the returned object is the smallest object,
    "a", such that merge(a, proto) matches obj.

    Otherwise, obj is returned.
    """
    if not (isinstance(obj, Mapping) and
            isinstance(proto, Mapping)):
        return obj

    new_obj = {}
    for key, value in obj.items():
        if key not in proto:
            new_obj[key] = value
            continue

        if (matches(value, proto[key]) and
            matches(proto[key], value)):
            continue

        if isinstance(value, Mapping):
            new_obj[key] = subkeys(value, proto[key])
            continue

        new_obj[key] = value

    return new_obj


def add_extends(yaml, key):
    """Modifies the given object "yaml" so that it includes an "extends" key
    whose value features "key".

    If "extends" is not in yaml, then yaml is modified such that
    yaml["extends"] == key.

    If yaml["extends"] is a str, then yaml is modified such that
    yaml["extends"] == [yaml["extends"], key]

    If yaml["extends"] is a list that does not include key, then key is
    appended to the list.

    Otherwise, yaml is left unchanged.
    """

    has_key = ('extends' in yaml)
    extends = yaml.get('extends')

    if has_key and not isinstance(extends, (str, Sequence)):
        return

    if extends is None:
        yaml['extends'] = key
        return

    if isinstance(extends, str):
        if extends != key:
            yaml['extends'] = [extends, key]
        return

    if key not in extends:
        extends.append(key)


def common_subobject(yaml, sub):
    """Factor prototype object "sub" out of the values of mapping "yaml".

    Consider a modified copy of yaml, "new", where for each key, "key" in yaml:

      - If yaml[key] matches sub, then new[key] = subkeys(yaml[key], sub).
      - Otherwise, new[key] = yaml[key].

    If the above match criteria is not satisfied for any such key, then (yaml,
    None) is returned. The yaml object is returned unchanged.

    Otherwise, each matching value in new is modified as in
    add_extends(new[key], common_key), and then new[common_key] is set to sub.
    The common_key value is chosen such that it does not match any preexisting
    key in new. In this case, (new, common_key) is returned.
    """
    match_list = set(k for k, v in yaml.items() if matches(v, sub))

    if not match_list:
        return yaml, None

    common_prefix = '.c'
    common_index = 0

    while True:
        common_key = ''.join((common_prefix, str(common_index)))
        if common_key not in yaml:
            break
        common_index += 1

    new_yaml = {}

    for key, val in yaml.items():
        new_yaml[key] = copy.deepcopy(val)

        if not matches(val, sub):
            continue

        new_yaml[key] = subkeys(new_yaml[key], sub)
        add_extends(new_yaml[key], common_key)

    new_yaml[common_key] = sub

    return new_yaml, common_key


def print_delta(name, old, new, applied=None):
    delta = new - old
    reldelta = (1000 * delta) // old
    reldelta = (reldelta // 10, reldelta % 10)

    if applied is None:
        applied = (new <= old)

    print('\n'.join((
        '{0} {1}:',
        '  before: {2: 10d}',
        '  after : {3: 10d}',
        '  delta : {4:+10d} ({5:=+3d}.{6}%)',
    )).format(
        name,
        ('+' if applied else 'x'),
        old,
        new,
        delta,
        reldelta[0],
        reldelta[1]
    ))


def try_optimization_pass(name, yaml, optimization_pass, *args, **kwargs):
    """Try applying an optimization pass and return information about the
    result

    "name" is a string describing the nature of the pass. If it is a non-empty
    string, summary statistics are also printed to stdout.

    "yaml" is the object to apply the pass to.

    "optimization_pass" is the function implementing the pass to be applied.

    "args" and "kwargs" are the additional arguments to pass to optimization
    pass. The pass is applied as

    >>> (new_yaml, *other_results) = optimization_pass(yaml, *args, **kwargs)

    The pass's results are greedily rejected if it does not modify the original
    yaml document, or if it produces a yaml document that serializes to a
    larger string.

    Returns (new_yaml, yaml, applied, other_results) if applied, or
    (yaml, new_yaml, applied, other_results) otherwise.
    """
    result = optimization_pass(yaml, *args, **kwargs)
    new_yaml, other_results = result[0], result[1:]

    if new_yaml is yaml:
        # pass was not applied
        return (yaml, new_yaml, False, other_results)

    pre_size = len(syaml.dump_config(
        sort_yaml_obj(yaml), default_flow_style=True))
    post_size = len(syaml.dump_config(
        sort_yaml_obj(new_yaml), default_flow_style=True))

    # pass makes the size worse: not applying
    applied = (post_size <= pre_size)
    if applied:
        yaml, new_yaml = new_yaml, yaml

    if name:
        print_delta(name, pre_size, post_size, applied)

    return (yaml, new_yaml, applied, other_results)


def build_histogram(iterator, key):
    """Builds a histogram of values given an iterable of mappings and a key.

    For each mapping "m" with key "key" in iterator, the value m[key] is
    considered.

    Returns a list of tuples (hash, count, proportion, value), where

      - "hash" is a sha1sum hash of the value.
      - "count" is the number of occurences of values that hash to "hash".
      - "proportion" is the proportion of all values considered above that
        hash to "hash".
      - "value" is one of the values considered above that hash to "hash".
        Which value is chosen when multiple values hash to the same "hash" is
        undefined.

    The list is sorted in descending order by count, yielding the most
    frequently occuring hashes first.
    """
    buckets = collections.defaultdict(int)
    values = {}

    num_objects = 0
    for obj in iterator:
        num_objects += 1

        try:
            val = obj[key]
        except (KeyError, TypeError):
            continue

        value_hash = hashlib.sha1()
        value_hash.update(syaml.dump_config(sort_yaml_obj(val)).encode())
        value_hash = value_hash.hexdigest()

        buckets[value_hash] += 1
        values[value_hash] = val

    return [(h, buckets[h], float(buckets[h]) / num_objects, values[h])
            for h in sorted(buckets.keys(), key=lambda k: -buckets[k])]


def optimizer(yaml):
    original_size = len(syaml.dump_config(
        sort_yaml_obj(yaml), default_flow_style=True))

    # try factoring out commonly repeated portions
    common_job = {
        'variables': {
            'SPACK_COMPILER_ACTION': 'NONE',
            'SPACK_RELATED_BUILDS_CDASH': ''
        },

        'after_script': ['rm -rf "./spack"'],

        'artifacts': {
            'paths': ['jobs_scratch_dir', 'cdash_report'],
            'when': 'always'
        },
    }

    # look for a list of tags that appear frequently
    _, count, proportion, tags = next(iter(
        build_histogram(yaml.values(), 'tags')),
        (None,) * 4)

    # If a list of tags is found, and there are more than one job that uses it,
    # *and* the jobs that do use it represent at least 70% of all jobs, then
    # add the list to the prototype object.
    if tags and count > 1 and proportion >= 0.70:
        common_job['tags'] = tags

    # apply common object factorization
    yaml, other, applied, rest = try_optimization_pass(
        'general common object factorization',
        yaml, common_subobject, common_job)

    # look for a common script, and try factoring that out
    _, count, proportion, script = next(iter(
        build_histogram(yaml.values(), 'script')),
        (None,) * 4)

    if script and count > 1 and proportion >= 0.70:
        yaml, other, applied, rest = try_optimization_pass(
            'script factorization',
            yaml, common_subobject, {'script': script})

    # look for a common before_script, and try factoring that out
    _, count, proportion, script = next(iter(
        build_histogram(yaml.values(), 'before_script')),
        (None,) * 4)

    if script and count > 1 and proportion >= 0.70:
        yaml, other, applied, rest = try_optimization_pass(
            'before_script factorization',
            yaml, common_subobject, {'before_script': script})

    # Look specifically for the SPACK_ROOT_SPEC environment variables.
    # Try to factor them out.
    h = build_histogram((
        getattr(val, 'get', lambda *args: {})('variables')
        for val in yaml.values()), 'SPACK_ROOT_SPEC')

    # In this case, we try to factor out *all* instances of the SPACK_ROOT_SPEC
    # environment variable; not just the one that appears with the greatest
    # frequency. We only require that more than 1 job uses a given instance's
    # value, because we expect the value to be very large, and so expect even
    # few-to-one factorizations to yield large space savings.
    counter = 0
    for _, count, proportion, spec in h:
        if count <= 1:
            continue

        counter += 1

        yaml, other, applied, rest = try_optimization_pass(
            'SPACK_ROOT_SPEC factorization ({count})'.format(count=counter),
            yaml,
            common_subobject,
            {'variables': {'SPACK_ROOT_SPEC': spec}})

    new_size = len(syaml.dump_config(
        sort_yaml_obj(yaml), default_flow_style=True))

    print('\n')
    print_delta('overall summary', original_size, new_size)
    print('\n')
    return yaml
