# Security policy

Strategic Advisor is pre-release software. It has no supported connectors or production service, and this policy does not promise a response time, remediation date, fitness guarantee, or absence of vulnerabilities.

## Report privately

Please use [GitHub private vulnerability reporting](https://github.com/johndetlefs/strategic-advisor/security/advisories/new) for a suspected vulnerability. Do not include secrets, credentials, proprietary documents, real message histories, or unnecessary personal case data. Provide the smallest synthetic reproduction that still demonstrates the issue.

If GitHub does not offer the private reporting form for this repository, do not disclose exploit details in a public issue. Open a public issue containing only the statement that you need a private maintainer contact path.

## Scope

Useful reports include packaging that exposes evaluation material, prompt or retrieved-content paths that can override the skill's authority or data boundaries, committed secret exposure, and validation bypasses. Questions about strategic quality without a security consequence belong in ordinary contribution discussion.

The deterministic privacy scanner checks bounded representative patterns only. A passing scan is not proof that the repository contains no sensitive, proprietary, or re-identifiable information. See [CONTRIBUTING.md](CONTRIBUTING.md) for the repository data boundary and [PRODUCT-CONTRACT.md](PRODUCT-CONTRACT.md) for current capability claims.
