---
title : "Create a S3 bucket to serve UI"
date : "`r Sys.Date()`"
weight : 1
chapter : false
pre : " <b> 3.1. </b> "
---

To serve the frontend (React build) over CloudFront, we first need an S3 bucket configured for static website hosting.

1. Open AWS Console, search for Amazon S3
   ![Search for S3](/images/3.cloudfront/3.1-create-ui-bucket/search-s3.png)
2. Click ***Create Bucket***
   ![Click Create Bucket](/images/3.cloudfront/3.1-create-ui-bucket/1.s3-create-ui-bucket.png)
3. In **General configuration**:
   1. Choose **General purpose** for Bucket type
   2. Specify a bucket name that is globally unique, e.g. `serverless-ui-bucket`
   ![General configuration](/images/3.cloudfront/3.1-create-ui-bucket/2.s3-ui-general-info.png)
4. Scroll down, in **Block Public Access settings for this bucket**, make sure the **Block *all* public access** checkbox is checked
   ![Block all public access](/images/3.cloudfront/3.1-create-ui-bucket/3.s3-ui-block-access.png)
5. Scroll down, leave everything as is, and click **Create Bucket**
   ![Create Bucket](/images/3.cloudfront/3.1-create-ui-bucket/4.s3-ui-create.png)
6. Wait a few seconds for the bucket to be created, then click on the bucket name to open it
   ![Bucket created](/images/3.cloudfront/3.1-create-ui-bucket/5.s3-create-done.png)