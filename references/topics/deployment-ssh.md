# SSH And SCP Deployment Baseline

## Purpose

> **Scope:** Checkable patterns for SSH-based deployment paths found in audit subjects
> **Key items:** key handling, StrictHostKeyChecking posture, scp/rsync patterns, agent
> forwarding risk, host-key verification class

This file consolidates deployment-path knowledge proven across audit sessions. It has no
single external owner. The patterns below are the checkable residue of recurring findings.

Snapshot date: 2026-09-30.

Feeds `assessment/deployment-review.md` and the delivery surface of self-hosted subjects.

## Key Material Handling

- Deploy keys live outside the repository: `~/.ssh/`, a secrets manager, or CI secret store.
  a committed private key (`id_rsa`, `*.pem`, `deploy_key`) is a finding, not config drift.
- Public keys in-repo (`authorized_keys` templates, `*.pub`) are acceptable evidence of the
  deployment surface. Private halves are not.
- Keys embedded in scripts (`ssh -i ./key.pem` where `key.pem` is tracked) make the artifact
  and the credential one finding.
- Passphrase-free keys are fine for automation when their scope is narrow (single host,
  deploy-only user). A passphrase-free root-capable key is a severity-raising context.

## Host Key Verification

- `StrictHostKeyChecking=no` or `accept-new`-without-pinning in scripts/CI bypasses
  MITM protection.`StrictHostKeyChecking=yes` with a pinned `known_hosts` or
  `ssh-keyscan`-captured fingerprint committed to the repo is the verifiable posture.
- `UserKnownHostsFile=/dev/null` combined with disabling verification is the same finding.
- A scripted `ssh-keyscan` at deploy time TOFU-trusts whatever answers. Acceptable only when
  the fingerprint is compared to a stored value afterwards.

## Transfer Patterns

- `scp -r` and `rsync -avz` over SSH are the common shapes.`rsync --delete` without a
  staging confirmation can remove the live tree - its use belongs behind a reviewed script,
  not an ad-hoc command.
- Transfers that pipe archives (`tar | ssh host tar -x`) skip integrity verification of the
  received tree. A checksum or signature step after transfer is the checkable hardening.
- `curl | ssh host bash` / `wget -O- | ssh` combines unsigned fetch with remote execution - 
  see `references/topics/git-integrity.md` CWE-494.

## SSH Agent And Config Surface

- `ForwardAgent yes` in committed `.ssh/config` or deploy scripts exposes the agent socket
  to the remote host. Acceptable for jump hosts, a finding for direct deploy targets.
- Deploy users should be least-privilege: a dedicated user with write access only to the
  deployment path.`ssh root@` in scripts is an observation escalating with context.
- `PermitRootLogin`, `PasswordAuthentication`, and port settings in committed
  `sshd_config`/Ansible playbooks are auditable deployment posture.
- Bastion/jump patterns (`-J`, `ProxyJump`) declare the network path. Undocumented jump
  hosts in scripts reveal topology worth recording in the deployment description.

## Live Check

These patterns are session-derived. No authoritative external source owns them. Cross-check
the MITM/TOFU reasoning against `references/topics/git-integrity.md` when a signed-update
claim accompanies the SSH path.

The file updates when audit sessions produce new deployment-path patterns.
