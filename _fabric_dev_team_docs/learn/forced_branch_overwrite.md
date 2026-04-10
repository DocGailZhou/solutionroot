# Steps to Recreate gz_fabric_dev from fabric_dev

## Overview
Purpose: Sometimes you have a branch that is too out of date and just want to take in content from another branch. In this doc, we will show you the steps to complete this task. Using `gz_fabric_dev` branch as an example, we'll show how you can overwrite it from another example branch named `fabric_dev`, as if you just created a new branch `gz_fabric_dev` and take in all contents from `fabric_dev`. 

To recreate your `gz_fabric_dev` branch to be based on the latest `fabric_dev` branch, essentially starting fresh. This follows a hierarchical workflow where `gz_fabric_dev` → `fabric_dev` → `main`.

## Important Notes

- **Warning**: Force pushing will overwrite the remote `gz_fabric_dev` branch completely
- Any commits that were only on the old `gz_fabric_dev` will be lost
- Make sure no one else is working on the `gz_fabric_dev` branch
- If you have any important changes on the current `gz_fabric_dev`, back them up first

## Result

This approach gives you a clean `gz_fabric_dev` that's identical to `fabric_dev` and ready for your new development work. Your workflow will be: work on `gz_fabric_dev` → submit PR to `fabric_dev` → team merges `fabric_dev` to `main`.

## Steps

### 1. **Fetch latest changes**
```bash
git fetch origin  # Download latest changes from remote without merging them
```
This ensures you have the latest changes from all remote branches, including `fabric_dev`.

### 2. **Switch to main and delete gz_fabric_dev**
```bash
git checkout main           # Switch to the main branch
git branch -D gz_fabric_dev # Force delete the gz_fabric_dev branch locally
```
You must switch to `main` before deleting `gz_fabric_dev`. It's best practice to switch to the main/default branch when deleting other branches, as you cannot delete the branch you're currently on. Use `-D` (capital D) for force delete since the branch might not be fully merged.

### 3. **Switch to fabric_dev and create new gz_fabric_dev branch from it**
```bash
git checkout fabric_dev        # Switch to the fabric_dev branch locally
git pull origin fabric_dev     # Pull latest changes from remote fabric_dev to update local copy
git checkout -b gz_fabric_dev  # Create new gz_fabric_dev branch from current branch (fabric_dev) and switch to it
```
Now switch to `fabric_dev` and pull the latest changes to ensure you have the most recent version. Then create and switch to a new `gz_fabric_dev` branch based on the current `fabric_dev` branch. This maintains your team's workflow where `gz_fabric_dev` → `fabric_dev` → `main`.

**Result**: `gz_fabric_dev` will have identical contents to `fabric_dev` because `git checkout -b` creates the new branch from whatever branch you're currently on, copying all commits and file contents.

### 4. **Force push the new branch to remote**
```bash
git push origin gz_fabric_dev --force  # Force push to overwrite remote gz_fabric_dev branch
```
Since you're replacing the remote branch with a completely different history, you need `--force`.

## Alternative Single-Command Approach

You could also do this in one command sequence:
```bash
git fetch origin                        # Download latest changes from remote
git checkout main                       # Switch to main branch
git branch -D gz_fabric_dev            # Force delete local gz_fabric_dev branch
git checkout fabric_dev                 # Switch to fabric_dev branch
git pull origin fabric_dev             # Pull latest changes from remote fabric_dev
git checkout -b gz_fabric_dev          # Create new gz_fabric_dev from fabric_dev and switch to it
git push origin gz_fabric_dev --force  # Force push to overwrite remote gz_fabric_dev
```

