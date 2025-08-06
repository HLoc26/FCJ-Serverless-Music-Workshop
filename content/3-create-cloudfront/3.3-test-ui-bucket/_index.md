---
title : "Upload a Test File to the UI Bucket"
date : "`r Sys.Date()`"
weight : 3
chapter : false
pre : " <b> 3.3. </b> "
---

Before wiring up the full frontend, we'll do a quick sanity check: upload a simple `index.html` file to the S3 UI bucket and make sure it's accessible via CloudFront.

This ensures that:

- Your S3 bucket is correctly configured for static website hosting
- CloudFront is correctly pointing to the UI bucket
- Public access and caching are working as expected

---

#### Create a test file

In your local project folder (or anywhere), create a basic `index.html`:

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Serverless Music App</title>
  </head>
  <body>
    <h1>Hello from CloudFront</h1>
  </body>
</html>
```
![Sample index.html file](/images/3.cloudfront/3.3-test-ui-bucket/1.index.html-file.png)
![Sample index.html content](/images/3.cloudfront/3.3-test-ui-bucket/2.index.html-content.png)

---

#### Option 1: Upload via AWS CLI

```bash
aws s3 cp index.html s3://your-ui-bucket-name/index.html
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

Replace `your-ui-bucket-name` with your actual bucket name.

![Upload via AWS CLI](/images/3.cloudfront/3.3-test-ui-bucket/3.upload-via-s3-cli.png)
![Upload via AWS CLI - Result](/images/3.cloudfront/3.3-test-ui-bucket/3.upload-via-s3-cli-result.png)

---

#### Option 2: Upload via AWS Console

1. Go to the [S3 Console](https://s3.console.aws.amazon.com/s3)
2. Click on your **UI bucket name**
   ![Click on UI bucket](/images/3.cloudfront/3.3-test-ui-bucket/4.click-ui-bucket.png)
3. Click **Upload**
   ![Click Upload](/images/3.cloudfront/3.3-test-ui-bucket/5.click-upload.png)
   ![Upload Page](/images/3.cloudfront/3.3-test-ui-bucket/6.upload-page.png)
4. Drag and drop your `index.html` file (or use **Add files**)
   ![Drag and Drop](/images/3.cloudfront/3.3-test-ui-bucket/7.drag-n-drop.png)
5. Click **Upload**
   ![Click Upload](/images/3.cloudfront/3.3-test-ui-bucket/8.click-upload.png)

After upload completes, the file should appear in your bucket as `index.html`.
   ![Click Upload](/images/3.cloudfront/3.3-test-ui-bucket/9.file-in-s3.png)

---

#### Test in browser

Now open your **CloudFront distribution domain**, which looks like:

```
https://dxxxxx.cloudfront.net/
```

You should see your "Hello from CloudFront" message rendered.

![Test in Browser](/images/3.cloudfront/3.3-test-ui-bucket/10.test-ok.png)

{{% notice info %}}
Once this test passes, you're ready to move on to deploying the real UI and configuring the audio file origin after Amplify is initialized.
{{% /notice %}}

---