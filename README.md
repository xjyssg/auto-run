# Notification System

This repository contains a Python script that runs every 5 minutes via GitHub Actions and sends an email notification.

## Setup Instructions

### 1. Email Configuration

To enable email notifications, you need to set up the following environment variables in your GitHub repository:

1. Go to your GitHub repository settings
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Add the following repository secrets:
   - `SENDER_EMAIL`: Your Gmail address
   - `SENDER_PASSWORD`: Your Gmail app-specific password (not your regular Gmail password)

#### Creating an App-Specific Password for Gmail

1. Go to your Google Account settings
2. Navigate to "Security" > "2-Step Verification" > "App passwords"
3. Generate a new app password for "Mail"
4. Use this password in the `SENDER_PASSWORD` secret

### 2. Troubleshooting Scheduled Workflows

If the scheduled workflow is not running automatically every 5 minutes:

1. Ensure the repository is on the default branch (main)
2. Verify that scheduled workflows are enabled in repository settings
3. Check the GitHub Actions logs for any errors
4. Make sure the cron syntax is correct: `*/5 * * * *` (every 5 minutes)

### 3. Manual Testing

You can manually trigger the workflow using the "workflow_dispatch" option in the GitHub Actions interface.

## Files

- `run.py`: Main Python script that prints "hello world" and sends an email
- `.github/workflows/scheduled-run.yml`: GitHub Actions workflow configuration
