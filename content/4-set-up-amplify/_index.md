---
title : "Set up Amplify for Backend"
date : "`r Sys.Date()`"
weight : 4
chapter : false
pre : " <b> 4. </b> "
---

In this section, you will deploy the backend of your music app using [AWS Amplify Gen 2](https://docs.amplify.aws/gen2/).

![What you will create: Amplify with Cognito Auth, S3 file bucket, and DynamoDB](/images/4.amplify/what-you-will-do.png)

We already have working backend code ready for authentication, database tables, and file storage. However, in this lab, you will not copy everything. Instead, you will be given partial code and expected to complete the rest.

The goal is to help you understand how Amplify connects to AWS services like Cognito, DynamoDB, and S3 — and how to pass environment variables to Lambda functions.

{{% notice info %}}
If you haven't completed the CloudFront and S3 setup in the previous section, do that first.
{{% /notice %}}
