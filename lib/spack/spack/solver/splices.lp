% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% These rules are conditionally loaded to handle the synthesis of spliced
% packages.
% =============================================================================
% Consider the concrete spec:
% foo@2.72%gcc@11.4 arch=linux-ubuntu22.04-icelake build_system=autotools ^bar ...
% It will emit the following facts for reuse (below is a subset)
% installed_hash("foo", "xxxyyy")
% hash_attr("xxxyyy", "hash", "foo", "xxxyyy")
% hash_attr("xxxyyy", "version", "foo", "2.72")
% hash_attr("xxxyyy", "node_os", "ubuntu22.04")
% hash_attr("xxxyyy", "hash", "bar", "zzzqqq")
% hash_attr("xxxyyy", "depends_on", "foo", "bar", "link")
% Rules that derive abi_splice_conditions_hold will be generated from 
% use of the `can_splice` directive. The will have the following form:
% can_splice("foo@1.0.0+a", when="@1.0.1+a", match_variants=["b"]) --->
% abi_splice_conditions_hold(0, node(SID, "foo"), "foo", BashHash) :-
%   installed_hash("foo", BaseHash),
%   attr("node", node(SID, SpliceName)),
%   attr("node_version_satisfies", node(SID, "foo"), "1.0.1"),
%   hash_attr("hash", "node_version_satisfies", "foo", "1.0.1"),
%   attr("variant_value", node(SID, "foo"), "a", "True"),
%   hash_attr("hash", "variant_value", "foo", "a", "True"),
%   attr("variant_value", node(SID, "foo"), "b", VariVar0),
%   hash_attr("hash", "variant_value", "foo", "b", VariVar0),

% If the splice is valid (i.e. abi_splice_conditions_hold is derived) in the
% dependency of a concrete spec the solver free to choose whether to continue
% with the exact hash semantics by simply imposing the child hash, or introducing
% a spliced node as the dependency instead 
{ imposed_constraint(ParentHash, "hash", ChildName, ChildHash) } :-
  hash_attr(ParentHash, "hash", ChildName, ChildHash),
  abi_splice_conditions_hold(_, node(SID, SpliceName), ChildName, ChildHash).

attr("splice_at_hash", ParentNode, node(SID, SpliceName), ChildName, ChildHash) :-
  attr("hash", ParentNode, ParentHash),
  hash_attr(ParentHash, "hash", ChildName, ChildHash),
  abi_splice_conditions_hold(_, node(SID, SpliceName), ChildName, ChildHash),
  ParentHash != ChildHash,
  not imposed_constraint(ParentHash, "hash", ChildName, ChildHash).
  
% Names and virtual providers may change when a dependency is spliced in
imposed_constraint(Hash, "dependency_holds", ParentName, SpliceName, Type) :-
  hash_attr(Hash, "depends_on", ParentName, DepName, Type),
  hash_attr(Hash, "hash", DepName, DepHash),
  attr("splice_at_hash", node(ID, ParentName), node(SID, SpliceName), DepName, DepHash).
 
imposed_constraint(Hash, "virtual_on_edge", ParentName, SpliceName, VirtName) :-
  hash_attr(Hash, "virtual_on_edge", ParentName, DepName, VirtName),
  attr("splice_at_hash", node(ID, ParentName), node(SID, SpliceName), DepName, DepHash).

