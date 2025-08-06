---
title : "Set up Storage with S3"
date : "`r Sys.Date()`"
weight : 4
chapter : false
pre : " <b> 4.4. </b> "
---

In this section, you'll learn how to configure Amplify to support uploading music files to Amazon S3.

We'll first set up a storage resource using the Amplify. This creates a dedicated S3 bucket that allows authenticated users to upload and store audio files securely. You will also verify the setup using the AWS Console.

Later in this section, you'll test the existing `/tracks/upload` endpoint to generate a signed URL, upload a file via that URL, and finally store track metadata to DynamoDB using the `/tracks` endpoint.

![What you will create: S3 file bucket](/images/4.amplify/4.4.s3-storage/what-you-will-do.png)

---

### Step 1. Create a Music Storage Bucket
To store user-uploaded music files, we will use Amazon S3, provisioned through Amplify.


#### Step 1.1. Create a Storage Resource
Go to the `amplfy` directory and create a new storage resource `storage/resource.ts`

![Create Storage Resource](/images/4.amplify/4.4.s3-storage/1.resource.png)

Now in `resource.ts`, you can use Amplify's Storage module to create a new S3 bucket. This bucket will be used to store the music files uploaded by users.

```typescript
import { defineStorage } from "@aws-amplify/backend";

export const fileBucket = defineStorage({
    name: "your-bucket-name",
})
```

{{% notice note %}}
Replace `your-bucket-name` with a unique name for your S3 bucket. This name must be globally unique across all AWS accounts.
{{% /notice %}}

#### Step 1.2. Deploy the Storage Resource
Now go to `backend.ts` and add the storage resource to the Amplify backend configuration below the existing `auth` resources (don't forget to import the storage resource first).

{{<details summary="Your backend.ts should look like this">}}
```typescript
import { defineBackend } from '@aws-amplify/backend';
import { auth } from './auth/resource';
import { fileBucket } from './storage/resource';

const backend = defineBackend({
	auth,
	fileBucket,
});
```
{{</details>}}

Now, deploy the backend resources by running the following command in your terminal at the root of the project:

```bash
npx ampx sandbox
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

#### Step 1.3. Verify the S3 Bucket
After the deployment is complete, you can verify that the S3 bucket has been created successfully.
1. Go to the [AWS Management Console](https://console.aws.amazon.com/).
    ![AWS Management Console](/images/4.amplify/4.4.s3-storage/2.search-s3.png)
2. Navigate to the S3 service. You should see the bucket you created listed there (with the prefix `amplify-`). Click on it to view its details.
    ![Bucket created](/images/4.amplify/4.4.s3-storage/3.your-bucket-name.png)
4. Save the bucket name, as you will need it later to configure the CloudFront distribution.

### Step 2. Configure CloudFront Distribution to serve music files
To serve the music files efficiently, we will set up the earlier CloudFront distribution that points to the S3 bucket. This will allow for faster content delivery and caching.

#### Step 2.1. Navigate to the existing CloudFront Distribution
1. Go to the [AWS Management Console](https://console.aws.amazon.com/) and search for CloudFront.
    ![Search CloudFront](/images/4.amplify/4.4.s3-storage/4.search-cloudfront.png)
2. Find the CloudFront distribution you created earlier for serving web UI.
    ![CloudFront Distribution](/images/4.amplify/4.4.s3-storage/5.created-distribution.png)
3. Click on the distribution ID to view its details.
    ![Distribution details](/images/4.amplify/4.4.s3-storage/6.distribution-detail.png)

#### Step 2.2. Add a new origin for the S3 bucket
1. In the "Origins" tab, you should see an origin pointing to your S3 web UI bucket.
    ![Origins](/images/4.amplify/4.4.s3-storage/7.s3-ui-origin.png)
2. Click **Create origin** to add a new origin for the S3 bucket.
    ![Create Origin](/images/4.amplify/4.4.s3-storage/8.click-create-origin.png)
3. Add a new origin for the S3 bucket you created in Step 1.1.
   - Set the origin domain to the S3 bucket URL (e.g., `your-bucket-name.s3.amazonaws.com`).
   - Ensure that the origin path is set to `/` (or leave empty) to serve files from the root of the bucket.
   - Remember the origin name (it should be the same as the S3 bucket URL by default), as you will need it when creating a new behavior for the music files.
        ![Origin domain](/images/4.amplify/4.4.s3-storage/9.origin-settings-1.png)
   - In **Origin access**, select **Origin access control settings (recommended)**, and an **Origin access control** field will appear.
        ![Origin access](/images/4.amplify/4.4.s3-storage/10.oac.png)
   - Select **Create new OAC** to create a new Origin Access Control (OAC) for the S3 bucket.
        ![Create OAC](/images/4.amplify/4.4.s3-storage/11.select-create-new-oac.png)
   - In the **Create Origin Access Control** dialog, set the following:
     - **Name**: `OAC-for-S3-file-bucket` (or any name you prefer)
     - **Signing Behavior**: Sign requests (recommended)
   - Select **Create** to create the OAC.
        ![Create OAC dialog](/images/4.amplify/4.4.s3-storage/12.create-dialog.png)  
   - Choose **Copy Policy** and save it in a text editor for later use. 
            ![Copy policy](/images/4.amplify/4.4.s3-storage/13.copy-policy.png)  
   - The policy you copied should look similar to this (with proper values replaced):
        ```json
        {
            "Version": "2008-10-17",
            "Id": "PolicyForCloudFrontPrivateContent",
            "Statement": [
                {
                    "Sid": "AllowCloudFrontServicePrincipal",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudfront.amazonaws.com"
                    },
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::<your-bucket-name>/*",
                    "Condition": {
                        "StringEquals": {
                        "AWS:SourceArn": "<your-distrobution-arn>"
                        }
                    }
                }
            ]
        }
        ```

   - Choose *Go to S3 bucket permissions* to open the S3 bucket permissions page.
        ![S3 permissions](/images/4.amplify/4.4.s3-storage/14.to-perm-page.png)
4. In the S3 bucket permissions page, in the **Bucket policy** section, you will need to set the bucket policy to allow CloudFront to access the S3 bucket contents.
   - Select **Edit**.
   - Use the above saved OAC policy to set the bucket policy. You only need the statement with the `AllowCloudFrontServicePrincipal` Sid. 
   - Or you can use the following policy as a template:
        ```json
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<your-bucket-name>/*",
            "Condition": {
                "StringEquals": {
                "AWS:SourceArn": "<your-distrobution-arn>"
                }
            }
        }
        ```
   - Paste the policy into the bucket policy editor, replacing `<your-bucket-name>` with your actual S3 bucket name and `<your-distrobution-arn>` with your CloudFront distribution ARN.
        ![S3 Bucket Policy](/images/4.amplify/4.4.s3-storage/15.paste-policy.png)
   - Select **Save changes** to apply the policy.

5.  Back to the Distribution Origin edit tab, save the changes to the origin settings.
    ![Create origin success](/images/4.amplify/4.4.s3-storage/16.create-origin.png)
#### Step 2.3. Create a new behaviour for the S3 origin
1. In the "Behaviors" tab, create a new behavior for the new S3 origin.
    ![Create behaviour](/images/4.amplify/4.4.s3-storage/17.create-behaviour.png)
2. Set the **Path pattern** to `/tracks/*` to match the music files you will upload.
3. Set the origin to the new S3 bucket origin you just created.
4. In **Compress objects automatically**, select **No** since audio files are already compressed.
    ![Basic info](/images/4.amplify/4.4.s3-storage/18.behaviour-settings.png)
5. Leave the other settings as default.
6. Click **Create** to save the new behaviour.
    ![Create new behavior](/images/4.amplify/4.4.s3-storage/19.create.png)
