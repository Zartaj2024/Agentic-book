#!/bin/bash

# Deployment script for Physical AI Book frontend to GitHub Pages

set -e  # Exit on any error

echo "Building Docusaurus site for GitHub Pages..."

# Build the site
npm run build

echo "Build completed successfully!"

# Check if we're in the right directory
if [ ! -d "build" ]; then
    echo "Error: build directory not found. Make sure to run 'npm run build' first."
    exit 1
fi

# Get the current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Save the current state
git add .
git commit -m "Site build $(date)" || true

# Create or update the gh-pages branch
if git show-ref --verify --quiet refs/heads/gh-pages; then
    # gh-pages branch exists, update it
    echo "Updating existing gh-pages branch..."
    git subtree push --prefix build origin gh-pages
else
    # gh-pages branch doesn't exist, create it
    echo "Creating new gh-pages branch..."
    git subtree push --prefix build origin gh-pages
fi

echo "Deployment to GitHub Pages completed!"
echo "Your site should be available at: https://$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///' | sed 's/.git$//' | cut -d'/' -f1).github.io/$(basename $(git config --get remote.origin.url | sed 's/.*\///' | sed 's/\.git$//'))/"

echo ""
echo "To setup GitHub Pages manually if the above doesn't work:"
echo "1. Go to your repository on GitHub"
echo "2. Navigate to Settings > Pages"
echo "3. Under 'Source', select 'Deploy from a branch'"
echo "4. Select 'gh-pages' branch and '/root' folder"
echo "5. Click 'Save'"