---
title : "Clean up resources"
date :  "`r Sys.Date()`"
weight : 7
chapter : false
pre : " <b> 7. </b> "
---

Once you're done testing and exploring the app, it's a good practice to clean up your AWS resources to avoid incurring unnecessary charges.

This section walks you through deleting all the Amplify-managed and manually-created resources for this workshop.

---

### Step 1. Delete the Amplify Project

Navigate to the root of your Amplify app and run:

```
npx ampx sandbox delete
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

You will be prompted to confirm the deletion. This command will:

* Delete the Amplify project from your local machine
* Remove associated backend resources in the cloud (Cognito, S3 buckets, DynamoDB, Lambda, etc.)
* Remove the Amplify app from the AWS Console

---

### Step 2. Empty and Delete UI Bucket

#### Step 2.1. Empty the bucket contents:

1. Go to the S3 console.
2. Find the bucket used for your web UI (the one you deployed in the previous steps).
3. Select all files and click "Actions" → "Delete".
4. Confirm the deletion.

#### Step 2.2. Delete the bucket:
1. In the S3 console, select the bucket.
2. Click "Delete bucket" from the "Actions" menu.
3. Confirm the deletion by typing the bucket name.

---

### 3. Delete CloudFront Distribution
1. Navigate to the CloudFront service in the AWS Console.
2. Find the distribution created for your web UI.
3. Select it and click "Actions" → "Delete".
4. Confirm the deletion.
5. Wait for the distribution to be fully deleted (this can take a few minutes).

### 4. Delete CloudFormation Stacks (optional)
If you want to ensure all resources are cleaned up, you can manually delete any remaining CloudFormation stacks that were created during the workshop.
1. Go to the CloudFormation service in the AWS Console.
2. Find any stacks related to the workshop (e.g., `amplify-fcjmusicrestapi-*`).
3. Select each stack and click "Delete".
4. Confirm the deletion.

### 5. Delete CDK bucket
1. Navigate to the S3 service in the AWS Console.
2. Find the CDK bucket used for storing deployment artifacts (usually named `cdk-bootstrap-*`).
3. Select the bucket and click "Empty".
4. Confirm the emptying of the bucket by typing "permanently delete".
5. After emptying, click "Delete bucket" from the "Actions" menu.
6. Confirm the deletion by typing the bucket name.

---

### You're Done!

You have now fully deployed — and responsibly torn down — a serverless music app using AWS Amplify Gen 2.

This concludes the workshop.
