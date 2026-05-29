# GitHub setup commands

Replace `IgnacyJurkowski` with your GitHub username or organization.

## 1. Create the local repository

```bash
mkdir web-audit-squad
cd web-audit-squad
# Copy the generated pack contents into this folder first, then:
git init
git branch -M main
git add .
git commit -m "Initial Web Audit Squad Claude Code skill"
```

## 2. Create the GitHub repository with GitHub CLI

```bash
gh auth login
gh repo create IgnacyJurkowski/web-audit-squad \
  --public \
  --description "Token-light seven-subagent Claude Code skill for web app audits" \
  --source=. \
  --remote=origin \
  --push
```

## 3. Create a release zip

```bash
zip -r web-audit-squad.zip .claude README.md LICENSE SECURITY.md CONTRIBUTING.md CHANGELOG.md install.sh docs examples \
  -x "*.git*" "*/__pycache__/*" "*.pyc"

git tag v2.0.0
git push origin v2.0.0
gh release create v2.0.0 web-audit-squad.zip \
  --title "Web Audit Squad v2.0.0" \
  --notes "Token-light Claude Code skill with seven read-only web audit subagents, state files, route mapping, and backlog workflow."
```

## 4. Installation command for users

```bash
curl -L -o web-audit-squad.zip https://github.com/IgnacyJurkowski/web-audit-squad/releases/latest/download/web-audit-squad.zip
unzip -o web-audit-squad.zip
```

Then restart Claude Code and run:

```text
/web-audit-squad init
```

## 5. Alternative: install from git checkout

```bash
git clone https://github.com/IgnacyJurkowski/web-audit-squad.git
cd web-audit-squad
./install.sh /path/to/target/web-app
```
