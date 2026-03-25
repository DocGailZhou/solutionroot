# Working with GitHub Branches

## Switching from main branch to a remote branch and pulling content

This document outlines the process to switch from the main branch to a remote branch and pull content from another remote branch.

### Step 1: Setup - Create gz_fabric_dev branch from fabric_dev (or your own branch)
```bash
# You maybe on main branch initially when you did a git clone. 
git branch
# * main

# 1. Fetch latest remote information
git fetch origin

# 2. Check what branches are available 
git branch -a

# 3. Now create your branch from latest fabric_dev
git checkout -b gz_fabric_dev origin/fabric_dev

# 4. Push and set up tracking
git push -u origin gz_fabric_dev

```

### Step 2: Daily Sync - Pull latest content from fabric_dev
```bash
# Before starting work each day - sync with latest fabric_dev changes
git checkout gz_fabric_dev  # Make sure you're on your branch
git pull origin fabric_dev   # Pull and merge latest fabric_dev into your branch
```

### Step 3: Make changes and commit to gz_fabric_dev branch, and push changes to remote

You can also use Visual Studio Code UI to perform below tasks, just commit and sync up! 

```bash
# After making your changes, check what files were modified
git status

# Add all changed files to staging
git add .

# Or add specific files
git add path/to/specific/file.txt

# Commit your changes with a descriptive message
git commit -m "Add your commit message here describing the changes"

# Push your local gz_fabric_dev branch with commits to remote
git push origin gz_fabric_dev

```

### **Step 4: Create Pull Request via GitHub Web Portal:**

1. Go to your GitHub repository in web browser
2. You'll see a notification about your recently pushed `gz_fabric_dev` branch
3. Click "Compare & pull request" button
4. Set the PR to merge **from** `gz_fabric_dev` **into** `fabric_dev`
   - Base branch: `fabric_dev`
   - Compare branch: `gz_fabric_dev`
5. Add PR title and description
6. Click "Create pull request"
7. Wait for review and approval, then merge

### Verification Commands
```bash
# Check current branch
git branch

# View all branches (local and remote)
git branch -a

# Check branch status and tracking
git status
```

## Summary
- Started on `main` branch
- Switched to `gz_fabric_dev` branch (created local tracking branch from remote)
- Pulled content from remote `fabric_dev` branch into `gz_fabric_dev` branch
- Made changes and committed them to `gz_fabric_dev` branch
- Pushed `gz_fabric_dev` branch to remote
- Created Pull Request via GitHub web portal to merge `gz_fabric_dev` → `fabric_dev`

## Branch Cleanup (If Things Go Wrong)
```bash
# If you need to delete a wrongly-created branch:
git push origin --delete branch_name  # Delete remote branch
git branch -d branch_name              # Delete local branch (use -D to force)

# Example: If you created gz_dev from main by mistake:
git push origin --delete gz_dev
git branch -d gz_dev
```

## Git Command Notes
- `git fetch origin` - Downloads latest info from remote (always run before creating branches)
- `git pull origin fabric_dev` command fetches and merges changes from fabric_dev into the current branch
- `git push origin gz_fabric_dev` command pushes your local branch and commits to remote
- `git checkout -b gz_fabric_dev origin/fabric_dev` creates a local branch from fabric_dev (corrected)
- `git pull origin fabric_dev` merges fabric_dev changes into your current branch (gz_fabric_dev)
- Always commit your changes before pushing with `git add` and `git commit`
- When creating PR, make sure to set correct base branch (fabric_dev) and compare branch (gz_fabric_dev)
- After PR is merged, you can safely delete the gz_fabric_dev branch locally: `git branch -d gz_fabric_dev`