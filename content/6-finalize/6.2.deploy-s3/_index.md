---
title : "Deploy the UI to S3"
date :  "`r Sys.Date()`"
weight : 2
chapter : false
pre : " <b> 6.2. </b> "
---

Once your UI is tested locally and working with the Amplify backend, it's time to push it to the cloud. The web UI will be hosted on the S3 bucket you configured earlier, and accessed via the CloudFront CDN.

In this step, you will:

- Build your React app
- Deploy the UI to S3
- Test the full flow: login → upload track → fetch tracks

---

### Step 1. Build your React App

Make sure you are in your UI project directory, then run:

```
npm run build
```

This will generate a `dist` (depending on your setup), containing the static files for production.

### Step 2. Sync to the S3 Bucket

You should already created an S3 bucket created for web hosting. Get its name from the AWS console if you don't remember.

Then run:

```
aws s3 sync ./dist s3://your-web-ui-bucket-name --delete
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

Replace `your-web-ui-bucket-name` with your bucket’s name. The `--delete` flag ensures outdated files are removed from the bucket.

### Step 3. Access Your Web App

Go to your CloudFront domain (e.g., `https://d1234example.cloudfront.net`) and test the full app functionality (just like you did locally):

* Login/signup should work via Cognito
* Upload and view tracks
* Create and fetch playlists
* Verify authenticated requests

---

> At this point, your entire serverless music app—from Cognito authentication to Lambda APIs and React UI—is fully deployed and testable in the cloud.
