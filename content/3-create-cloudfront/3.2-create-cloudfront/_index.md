---
title : "Create a CloudFront Distribution"
date : "`r Sys.Date()`"
weight : 2
chapter : false
pre : " <b> 3.2. </b> "
---

Now that the S3 bucket for hosting the UI is ready, it's time to create a **CloudFront distribution** that will serve your static web app to users — fast, globally, and securely.

In this step, we'll set up **a single CloudFront distribution** with a default behavior pointing to the UI bucket you just created. This distribution will later also be used to serve audio files (from another S3 bucket that will be created by Amplify in upcoming steps).

{{% notice info %}}
At this point, the CloudFront distribution will **only serve the UI bucket**. Once Amplify is deployed, we'll come back and **add a new origin and behavior** for streaming audio from the second bucket.
{{% /notice %}}

---

#### Create the distribution

You can create the CloudFront distribution manually via the AWS Console, or use the AWS CLI (JSON config required). For most users, the Console is easier at this stage:

1. Search for **CloudFront** in the AWS Management Console and go to the **CloudFront Console**.
   ![Search for Cloudfront](/images/3.cloudfront/3.2-create-cloudfront/1.search-cloudfront.png)
2. Click **Create Distribution**
   ![Create distribution](/images/3.cloudfront/3.2-create-cloudfront/2.create-distribution.png)
3. Under **Distribution name**, enter a name like `serverless-music-distribution`
   ![Set distribution name](/images/3.cloudfront/3.2-create-cloudfront/3.distribution-name.png)
4. Click **Next** to go to the **Specify Origin** step.
   ![Click Next](/images/3.cloudfront/3.2-create-cloudfront/4.next-to-origin.png)
5. Under **Origin Type**, select **S3 Origin**.
   ![Select S3 as origin type](/images/3.cloudfront/3.2-create-cloudfront/5.specify-origin-type.png)
6. For **Origin Domain Name**, select browse and choose the S3 bucket you created for the UI (e.g., `serverless-ui-bucket`).
   ![Click Browse S3](/images/3.cloudfront/3.2-create-cloudfront/6.s3-origin-browse.png)
   ![Select your UI bucket](/images/3.cloudfront/3.2-create-cloudfront/7.select-bucket.png)
7. Under **Origin Path**, leave it empty.
8. Click **Next**
   ![Search for S3](/images/3.cloudfront/3.2-create-cloudfront/8.origin-path-empty-next.png)
9.  Under **Web Application Firewall**, leave it disabled (choose **Do not enable security protections**) for now and click **Next**.
   ![Search for S3](/images/3.cloudfront/3.2-create-cloudfront/9.disable-waf.png)
10. Finally, review the settings and click **Create Distribution**.
   ![Search for S3](/images/3.cloudfront/3.2-create-cloudfront/10.review.png)

Once the distribution is created, note the **CloudFront domain name**, you'll use this to access your UI later.
    ![Distribution name](/images/3.cloudfront/3.2-create-cloudfront/11.distribution-name.png)

#### Specify the default root project
In the CloudFront distribution settings, you can specify a default root object (like `index.html`) that will be served when users access the root URL of your distribution.

1. From the Distribution detail page (from the last section), go to the **General** tab.
2. Click on **Edit** in the **Settings** section
    ![Edit settings](/images/3.cloudfront/3.2-create-cloudfront/12.edit-settings.png)
3. Find the **Default Root Object** section and enter `index.html`.
    ![Specify index.html as the default root object](/images/3.cloudfront/3.2-create-cloudfront/13.default-root-object.png)
4. Click **Save Changes** to save the changes.
    ![Click save changes](/images/3.cloudfront/3.2-create-cloudfront/14.save-changes.png)

---

Now wait for the distribution to deploy. This can take a few minutes. Once it's ready, you can access your UI via the CloudFront domain name.

Under the **General** tab of your distribution, you should see some useful information, including:
- **Domain Name**: This is the URL you will use to access your UI (e.g., `d1234example.cloudfront.net`).
- **Status**: Should be a datetime format when ready (if you just made some changes, it should be "Deploying").

{{% notice tip %}}
You won't upload the real UI yet. In the next step, we'll test the setup by uploading a simple `index.html` file to the UI bucket and verifying that CloudFront serves it correctly.
{{% /notice %}}

---


