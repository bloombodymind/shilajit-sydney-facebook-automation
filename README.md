# shilajit-sydney-facebook-automation
Automated Facebook posting system for Shilajit Sydney. Schedules 30 days of posts using GitHub Actions, running daily at 11 AM AEDT.

## 🔧 Setup Instructions

### Prerequisites
- Facebook Developer Account
- Admin access to your Facebook Page
- Facebook App created at https://developers.facebook.com/apps

### Getting a Permanent Facebook Page Access Token

**⚠️ IMPORTANT: The token you're currently using is expiring daily. Follow these steps to generate a permanent token that never expires.**

#### Step 1: Generate a Short-Lived User Access Token
1. Go to [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer)
2. Select your app from the dropdown menu (top right)
3. Click "Generate Access Token"
4. Grant the following permissions:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
5. Click "Generate Access Token" and authorize
6. Copy the token that appears (this is a short-lived token, valid for ~1 hour)

#### Step 2: Convert to Long-Lived User Access Token
1. Go to [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
2. Paste your short-lived token and click "Debug"
3. Click the "Extend Access Token" button at the bottom
4. Copy the new long-lived token (valid for 60 days)

#### Step 3: Generate Permanent Page Access Token
1. Go back to [Graph API Explorer](https://developers.facebook.com/tools/explorer)
2. Paste your long-lived user token into the "Access Token" field
3. In the query field, enter: `YOUR_PAGE_ID?fields=access_token`
   - Replace `YOUR_PAGE_ID` with your actual Facebook Page ID
4. Click "Submit"
5. Copy the `access_token` from the response - **This is your permanent page access token!**

#### Step 4: Verify the Token Never Expires
1. Go to [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
2. Paste your page access token
3. Click "Debug"
4. Look for "Expires:" - it should say "Never"

#### Step 5: Update GitHub Secrets
1. Go to your repository: Settings → Secrets and variables → Actions
2. Update the `FACEBOOK_ACCESS_TOKEN` secret with your new permanent token
3. Make sure `FACEBOOK_PAGE_ID` is also set correctly

### Alternative Method: Using System User (Recommended for Business Pages)

If you have Facebook Business Manager access, you can use a System User token:

1. Go to [Business Settings](https://business.facebook.com/settings)
2. Navigate to Users → System Users
3. Click "Add" to create a new system user
4. Assign your Facebook Page as an asset to the system user
5. Grant necessary permissions (Manage Page, Create Content)
6. Click "Generate New Token"
7. Select your app and required permissions
8. Copy the system user token and use it to generate a page access token (Step 3 above)

## 🐛 Troubleshooting

### Token Expires Daily
**Problem:** Your automation fails every day with "Session has expired" error

**Solution:** You're using a short-lived or user access token instead of a permanent page access token. Follow the setup instructions above to generate a permanent token.

### Error: "Invalid OAuth access token"
**Solution:** Your token may have been invalidated. Regenerate a new permanent page access token.

### Workflow Runs Successfully But Post Doesn't Appear
**Solution:** Check that:
- Your Page ID is correct
- The token has `pages_manage_posts` permission
- You're an admin of the page

## 📝 How It Works

1. GitHub Actions triggers daily at 11 AM AEDT
2. Script loads posts from `posts.json`
3. Selects post based on current day of month (cycles through 30 posts)
4. Posts to Facebook using the Graph API

## 🔐 Required GitHub Secrets

- `FACEBOOK_PAGE_ID`: Your Facebook Page ID
- `FACEBOOK_ACCESS_TOKEN`: Your permanent page access token (never expires)

## 📚 Resources

- [Facebook Access Tokens Documentation](https://developers.facebook.com/docs/facebook-login/guides/access-tokens)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
