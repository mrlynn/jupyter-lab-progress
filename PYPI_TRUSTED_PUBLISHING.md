# Configuring Trusted Publishing on PyPI

Follow these steps to set up trusted publishing for `jupyter-lab-progress`:

## 1. Log in to PyPI
Go to https://pypi.org and log in to your account.

## 2. Navigate to Your Project
Go to your project page: https://pypi.org/manage/project/jupyter-lab-progress/

## 3. Access Publishing Settings
1. Click on "Manage" or "Your projects" in the top menu
2. Find `jupyter-lab-progress` and click on it
3. Look for "Publishing" in the left sidebar (or similar section)

## 4. Add GitHub Publisher
Click "Add a new publisher" and fill in these exact values:

- **Owner**: `mrlynn` (your GitHub username)
- **Repository name**: `jupyter-lab-utils`
- **Workflow name**: `python-publish.yml`
- **Environment name**: `pypi` (must match the workflow file)

## 5. Save Configuration
Click "Add" to save the trusted publisher configuration.

## What This Does
- Allows GitHub Actions to publish to PyPI without storing API tokens
- Uses OpenID Connect (OIDC) for secure authentication
- Only the specified workflow from your repository can publish

## Testing
After configuration:
1. Create a new release on GitHub: https://github.com/mrlynn/jupyter-lab-utils/releases/new
2. The workflow will automatically trigger and publish to PyPI
3. No API tokens or passwords needed!

## Troubleshooting
If publishing fails:
- Verify all names match exactly (owner, repo, workflow, environment)
- Check the GitHub Actions logs for detailed error messages
- Ensure the package version in `pyproject.toml` hasn't been published already

## Benefits
✅ More secure than API tokens  
✅ No secrets to manage or rotate  
✅ Automatic publishing on releases  
✅ Full audit trail in GitHub Actions