---
title : "Preparation"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 1.2. </b> "
---

Before diving into the code, let's make sure you've got the right tools and background to get the most out of this workshop.

#### What you should already know

You don't need to be a cloud guru, but you should be comfortable with:

* **JavaScript / TypeScript**: especially in the context of React and Node.js
* **Basic React**: hooks, props, and component structure
* **REST APIs**: how frontend talks to backend
* **Git & CLI**: you'll be running some commands
* **AWS Services**: AWS Console to browse through all the resources you will be creating in the workshop

If you've built a basic CRUD app before, you're good to go.

#### Tools you'll need installed

Make sure you have the following installed on your machine:

* [Node.js (v18+)](https://nodejs.org/en/): for building and running frontend/backend code
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html): for deploying and managing AWS resources (please refer to [lab 000011. Getting Started with the AWS CLI](https://000011.awsstudygroup.com/))
* [Git](https://git-scm.com/): for cloning the repo and version control

#### AWS Setup

You'll also need:

* An **AWS account**
* A configured **IAM user** with programmatic access
* `aws configure` run in your terminal with valid access keys

{{% notice tip %}}
If this is your first time using AWS CLI, set aside 15–20 minutes for setup. It's a one-time thing.
{{% /notice %}}
