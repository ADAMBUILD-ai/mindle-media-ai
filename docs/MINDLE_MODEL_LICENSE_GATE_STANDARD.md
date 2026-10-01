# MINDLE MODEL LICENSE GATE STANDARD

## Purpose

This standard protects a verified runtime baseline from an unsupported commercial-release claim. It does not modify model bytes, model revisions, product UI, prior runtime evidence, main, or Production.

## Required evidence per model

1. Exact official repository and immutable revision.
2. Exact model-card or repository license declaration, captured as bytes and SHA-256.
3. Artifact filename, bytes, and SHA-256 from the immutable verified baseline.
4. A preserved license-text snapshot, source URL, bytes, and SHA-256.
5. Private model-cache revision, path, and private-visibility recheck.
6. Terms analysis: rights scope, attribution/notices, termination or breach trigger, retroactive policy-change basis, and any derivative-chain issue.
7. One of: PERPETUAL_USE_GATE_PASS, LEGAL_REVIEW_REQUIRED, or REJECT_AND_REPLACE.

## Fail-closed rule

A model may be used in an existing non-production TESTED_PASS baseline without alteration, but it must not be promoted to commercial Release Candidate unless its perpetual-use gate is PERPETUAL_USE_GATE_PASS. A later publisher or service-policy change must never be assumed to rewrite a license grant without reviewed evidence.

## Preservation controls

Evidence is stored as a GitHub Actions artifact and in the dedicated private MINDLE MEDIA AI Hugging Face model repository. Credentials are read only from masked secrets and are never written to evidence. All work is CPU-only, has a 15-minute workflow cap, uses no GPU or paid compute, and never force-pushes, merges main, or deploys Production.
