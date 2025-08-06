---
title : "Project Initialization "
date : "`r Sys.Date()`"
weight : 2
chapter : false
pre : " <b> 2. </b> "
---

### Clone the project

Start by cloning the starter repository to your local machine:

```bash
git clone https://github.com/your-username/music-platform-serverless.git
cd music-platform-serverless
```

If you're using a fork, replace the URL with your own.

### Install dependencies

Make sure you're in the root folder of the project, then install all required packages for both the frontend and backend:

```bash
# Install dependencies
npm i
```

### Start the local web UI

The web UI has been built for you, and you can start it with the following command:

```bash
npm run dev
```

This will start the web UI on [http://localhost:5173](http://localhost:5173). You can access it in your browser to see the UI.

### Set up AWS credentials

Before deploying anything, ensure your AWS credentials are configured. If you haven't already, run:

```bash
aws configure
```

You'll be prompted for your access key, secret key, region, and output format. If you're using named profiles, remember to export the profile:

```bash
export AWS_PROFILE=your-profile-name # On UNIX
$env:AWS_PROFILE = "your-profile-name" # On Windows Powershell
set AWS_PROFILE=your-profile-name # On CMD
```

{{% notice info %}}
Please refer to the [lab 000011. Getting Started with the AWS CLI](https://000011.awsstudygroup.com/) for more information
{{% /notice %}}
