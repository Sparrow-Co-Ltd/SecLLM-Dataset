## Summary

<!-- What does this PR change, and why? Link related issues (e.g. "Closes #12"). -->

## Type of change

- [ ] Documentation
- [ ] Script / CI
- [ ] Community data (`data/community/<lang>/`) — proposal issue: #
- [ ] Other:

Core data in `data/java/` is not changed through external PRs. Report data problems with the
[data error form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml) instead.

## Checklist

- [ ] `python scripts/validate.py --self-test` and `python scripts/validate.py` pass locally
- [ ] If `README.md` changed, `README.ko.md` is updated too (and vice versa)
- [ ] Every commit is signed off (`git commit -s`) under the [DCO](https://developercertificate.org/)
- [ ] For community data: every record has complete `meta`, an allowlisted `sourceLicense`, and `patchVerified: true`
