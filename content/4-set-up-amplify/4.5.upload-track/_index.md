---
title : "Upload Music Tracks to S3"
date : "`r Sys.Date()`"
weight : 5
chapter : false
pre : " <b> 4.5. </b> "
---

In this part, we will manually upload a music file to the S3 bucket and verify that it can be streamed via the CloudFront CDN. This ensures that music files are publicly accessible (if permitted) and served efficiently from edge locations.

First, download the following sample `.mp3` file to your local machine:

{{<attachments title="Sample mp3 file" pattern="mp3"/>}}

![Sample MP3 file](/images/4.amplify/4.5.upload-track/1.sample-file.png)


### Step 1. Upload a test `.mp3` file to S3

- Go to the AWS Console
![Upload test file to S3](/images/4.amplify/4.5.upload-track/2.search-s3.png)
- Open **S3**, and navigate to your music file bucket (created via Amplify earlier)
![Select file bucket](/images/4.amplify/4.5.upload-track/3.select-file-bucket.png)
- Currently it should be empty, so we need to create a `tracks` folder. Select **Create folder** to create new folder 
![Select Create Folder](/images/4.amplify/4.5.upload-track/4.select-create-folder.png)
- Name the folder `tracks`
![Set the folder's name to tracks](/images/4.amplify/4.5.upload-track/5.name-tracks.png)
- Select **Create folder**
![Click create folder](/images/4.amplify/4.5.upload-track/6.click-create.png)
- Click on the newly created `tracks` folder
![Select the newly created folder](/images/4.amplify/4.5.upload-track/7.click-tracks.png)
- Click **Upload**
![Select Upload](/images/4.amplify/4.5.upload-track/8.click-upload.png)
- Drag the `.mp3` file downloaded from your local machine and drop to the upload area
![Drag n drop file](/images/4.amplify/4.5.upload-track/9.drag.png)
- Select **Upload**
![Upload test file to S3](/images/4.amplify/4.5.upload-track/10.click-upload.png)

### Step 2. Get the CloudFront URL

- Return to the CloudFront distribution created for this bucket and copy the **Domain name**, e.g. `d123456abcdef8.cloudfront.net`
![Upload test file to S3](/images/4.amplify/4.5.upload-track/11.copy-domain.png)
- Construct the file URL as:

  ```
  https://<CloudFrontDomain>/tracks/<filename>.mp3
  ```

  Example (if you use the sample file):

  ```
  https://d123456abcdef8.cloudfront.net/tracks/Lost_in_the_Night-1.mp3
  ```

### Step 3. Test the audio playback

You can quickly test the streaming by pasting the URL in your browser. Alternatively, create a simple HTML page like:

```
<audio controls>
  <source src="https://d123456abcdef8.cloudfront.net/tracks/Lost_in_the_Night-1.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
```

Save this as `test.html` and open in your browser and you will have a simple audio player that streams the file from CloudFront (the below audio is just an example, it does not use the actual CloudFront URL):

{{< audio src="./_index.files/Lost_in_the_Night-1.mp3" >}}

![Test audio playback](/images/4.amplify/4.5.upload-track/12.track-playing.png)
