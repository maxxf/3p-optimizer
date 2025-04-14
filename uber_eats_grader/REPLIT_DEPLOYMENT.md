# Deploying Uber Eats Grader to Replit

This guide provides step-by-step instructions for deploying the Uber Eats Grader application to Replit after you've pushed it to GitHub.

## Prerequisites

- A GitHub account with the Uber Eats Grader repository pushed to it
- A Replit account (free or paid)

## Step 1: Import from GitHub to Replit

1. Go to [Replit](https://replit.com) and sign in to your account
2. Click the "+ Create" button in the top-right corner
3. Select the "Import from GitHub" tab
4. Paste your GitHub repository URL: `https://github.com/YOUR_USERNAME/uber-eats-grader`
5. Click "Import from GitHub"
6. Wait for Replit to import all files (this may take a minute)

## Step 2: Install Dependencies

Once the repository is imported, you need to install the required dependencies:

1. Click on the "Shell" tab in the bottom panel of Replit
2. Run the following commands:

```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

This will install all the Python packages needed for the application and download the required NLTK resources.

## Step 3: Configure the Run Command

To ensure Replit knows how to start your application:

1. Click on the "⚙️" icon in the sidebar to open Settings
2. Find the "Run" section
3. Set the "Run command" to: `python run.py --host 0.0.0.0 --port 443`
4. Click "Save"

## Step 4: Run the Application

1. Click the "Run" button at the top of the Replit interface
2. Wait for the application to start (this may take a minute)
3. Once running, you'll see the Uber Eats Grader interface in the webview
4. You can access the public URL by clicking on the URL at the top of the webview

## Step 5: Make It Always On (Optional)

By default, Replit will shut down your application after a period of inactivity. If you want it to run continuously:

1. Click on the "⚙️" icon in the sidebar to open Settings
2. Scroll down to "Always On"
3. Toggle it to "On"

Note: This feature may require a paid Replit subscription.

## Troubleshooting

### Memory Issues

If you encounter memory issues in Replit:

1. Remove unnecessary files like test fixtures or large data files
2. Optimize the application by reducing memory usage in heavy operations
3. Consider upgrading your Replit plan for more resources

### NLTK Data Errors

If you see errors related to NLTK data:

1. Run the NLTK download commands again:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```
2. Verify the downloads were successful by checking the output

### Application Not Loading

If the application doesn't load properly:

1. Check the console output for error messages
2. Verify that all dependencies were installed correctly
3. Try refreshing the webview or accessing the URL directly
4. Restart the Repl by clicking "Stop" and then "Run" again

## Customizing Your Deployment

### Environment Variables

You can set environment variables in Replit:

1. Go to the "Secrets" tab in the sidebar
2. Add any environment variables your application needs

### Custom Domain (Optional)

If you have a custom domain and a paid Replit plan:

1. Go to the "Settings" tab
2. Scroll to the "Custom Domain" section
3. Follow the instructions to connect your domain

## Updating Your Application

When you make changes to your GitHub repository:

1. In Replit, go to the "Version Control" tab in the sidebar
2. Click "Pull" to fetch the latest changes
3. Restart your application by clicking "Stop" and then "Run"
