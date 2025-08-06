---
title : "Create a CloudFront Distribution"
date : "`r Sys.Date()`"
weight : 3
chapter : false
pre : " <b> 3. </b> "
---

To serve static assets like images, audio files, or frontend builds efficiently across the globe, we'll set up a CloudFront distribution in front of an S3 bucket. CloudFront acts as a content delivery network (CDN), caching content at edge locations for faster delivery and reduced latency.

In this step, we'll configure the S3 bucket and connect it to CloudFront so that your music app's assets can be delivered quickly and reliably, no matter where your users are.

![What you will create: CloudFront and UI web bucket](/images/3.cloudfront/what-you-will-do.png)


{{% notice info %}}
We'll test everything locally first, so you will not upload the website files yet
{{% /notice %}}
