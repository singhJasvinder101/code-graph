##!/bin/bash
#set -e

#NEW_NAME="singhJasvinder101"
#NEW_EMAIL="131908922+singhJasvinder101@users.noreply.github.com"
#REPO_NAME="code-graph"

## Verify git-filter-repo is installed
#if ! command -v git-filter-repo &> /dev/null; then
#    echo "⚠️ git-filter-repo not found. Installing via pip..."
#    pip install git-filter-repo
#fi

#echo "🚀 Completely purging Copilot from all commit history..."

## Using modern git-filter-repo with python callbacks
#git filter-repo --force --commit-callback "
#if b'Copilot' in commit.author_email or b'copilot' in commit.author_email:
#    commit.author_name = b'$NEW_NAME'
#    commit.author_email = b'$NEW_EMAIL'
#if b'Copilot' in commit.committer_email or b'copilot' in commit.committer_email:
#    commit.committer_name = b'$NEW_NAME'
#    commit.committer_email = b'$NEW_EMAIL'

## Clean up any automated agent lines from commit messages
#if b'Agent-Logs-Url' in commit.message:
#    lines = commit.message.split(b'\n')
#    commit.message = b'\n'.join([l for l in lines if not l.startswith(b'Agent-Logs-Url:')])
#"

#echo "🔗 Safe-checking origin remote..."
## Check if remote exists instead of blindly trying to add it and crashing
#if git remote | grep -q "^origin$"; then
#    git remote set-url origin "git@github-personal:$NEW_NAME/$REPO_NAME"
#else
#    git remote add origin "git@github-personal:$NEW_NAME/$REPO_NAME"
#fi

#echo "✅ Local history scrubbed clean!"
#echo "👉 Run: git push origin --force --all"



#!/bin/bash
set -e

OLD_EMAIL="jasvinder.singh@omniful.ai"
NEW_NAME="singhJasvinder101"
NEW_EMAIL="131908922+singhJasvinder101@users.noreply.github.com"
REPO_NAME="code-graph"

# Verify git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "git-filter-repo not found. Installing via pip..."
    pip install git-filter-repo
fi

echo "Rewriting author/committer from $OLD_EMAIL to $NEW_EMAIL ..."

git filter-repo --force --commit-callback "
old = b'$OLD_EMAIL'
if commit.author_email == old:
    commit.author_name = b'$NEW_NAME'
    commit.author_email = b'$NEW_EMAIL'
if commit.committer_email == old:
    commit.committer_name = b'$NEW_NAME'
    commit.committer_email = b'$NEW_EMAIL'

if b'Agent-Logs-Url' in commit.message:
    lines = commit.message.split(b'\n')
    commit.message = b'\n'.join([l for l in lines if not l.startswith(b'Agent-Logs-Url:')])
"

echo "Checking origin remote..."
if git remote | grep -q "^origin$"; then
    git remote set-url origin "git@github-personal:$NEW_NAME/$REPO_NAME.git"
else
    git remote add origin "git@github-personal:$NEW_NAME/$REPO_NAME.git"
fi

echo "Done. Verify with: git log --format='%an <%ae>'"
echo "Then push: git push --force-with-lease origin main"
