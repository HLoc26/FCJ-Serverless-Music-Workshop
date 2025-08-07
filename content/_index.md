---
title : "Building a simple Serverless Music Streaming Website"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
---
# Building a simple Serverless Music Streaming Website

---

### 1. Introduction

Building a full-featured music platform used to mean provisioning servers, setting up databases, handling file storage, scaling traffic, and writing tons of boilerplate code just to get started. But not anymore.

In this guide, I'll show you how to build a (mostly) complete web music platform, without managing a single server. The entire backend runs on serverless services from AWS, and the frontend is built with React and TypeScript. You'll learn how to wire the core functionalities of a music streaming platform such as user authentication, uploading tracks, streaming tracks, create playlists,...

Whether you're a developer exploring serverless for the first time or someone looking to modernize how you build apps, this project will give you hands-on experience with production-grade patterns - all in the context of a real-world app.

---

### 2. Reasons for chosing the project
Imagine you have a website. Without 3rd party resources, you will have to build your own server, configuring your router to open your website to the world, and so so many other technical things to care about. Let's be honest, managing infrastructure isn't fun: keeping them alive, scaling them, patching them, or even just monitoring them can become a huge time sink. That's where serverless comes in.

With serverless, you can:
- **Skip the servers**: Everything runs on demand using AWS Lambda.
- **Scale automatically**: Whether you have 10 users or 10,000, your app adjusts with no manual effort.
- **Only pay for what you use**: No idle cost. No wasted resources.
- **Move fast**: Focus on product features, not backend maintenance.
- **Build modern apps**: Serverless plays well with React, APIs, and microservices.
For something like a music app, which can be unpredictable in load, media-heavy, and user-driven, serverless is a perfect match.

---

### 3. Objective

By the end of this lab, you'll have a simple serverless music platform where users can:

- Sign up and log in using Cognito (with secure token-based auth)
- Create and manage playlists
- Upload and stream music tracks via S3
- Browse everything through a clean React + TypeScript frontend

And all of this will be powered by:
- **AWS Lambda** for backend logic
- **API Gateway** for routing HTTP requests
- **DynamoDB** for storing playlists, tracks information
- **S3** for file storage
- **Amplify** for infrastructure and deployment

You'll walk away with a solid foundation for building modern, scalable, cloud-native applications.

---

### 4. Content

1. [Introduction](./1-introduction/_index.md)
2. [Project Initialization](./2-project-initialization/_index.md)
3. [Create a CloudFront Distribution](./3-create-cloudfront/_index.md)
4. [Set up Amplify for Backend](./4-set-up-amplify/_index.md)
5. [Deploying API Gateway and Lambda Functions](./5-api/_index.md)
6. [The final step: Deploy and Test the UI](./6-finalize/_index.md)
7. [Clean up resources](./7-cleanup/_index.md)





