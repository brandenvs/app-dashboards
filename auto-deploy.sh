#!/bin/bash

# Stash any uncommitted changes
echo "Stashing uncommitted changes..."
git stash

# Fetch the latest changes from the remote
echo "Fetching changes from remote repository..."
git fetch

# Wait for 5 seconds
sleep 5

# Pull the latest changes from the remote repository
echo "Pulling the latest changes..."
git pull

# Wait for 5 seconds
sleep 5

# Check git status and save to a text file
echo "Checking git status..."
git status > git_status_output.txt

# Optional: Display the git status file
echo "Displaying git status..."
cat git_status_output.txt

# Wait for 2 seconds
sleep 2

# Restart Gunicorn service
echo "Restarting Gunicorn service..."
sudo systemctl restart gunicorn

# Wait for 10 seconds
sleep 10

# Check Gunicorn service status
echo "Checking Gunicorn service status..."
sudo systemctl status gunicorn
