---
title : "Project architecture"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 1.1. </b> "
---

![What you will do](/images/architecture.png)

### Frontend and User Management

* **Client:** Users interact with the application through a web browser.
* **CloudFront Web UI:** Amazon CloudFront acts as a content delivery network (CDN), caching static web content and accelerating delivery to users worldwide, ensuring a fast and responsive user experience.
* **Amplify:** AWS Amplify simplifies the development and deployment of the web application. It integrates seamlessly with other AWS services.
* **Cognito User Pool:** Amazon Cognito provides secure user sign-up, sign-in, and access control. It manages user identities and authenticates users before they can access backend resources.
* **Amazon S3 Bucket (Web UI Bucket):** This S3 bucket stores the static assets of the web user interface (HTML, CSS, JavaScript files), which are served via CloudFront.
* **Amazon S3 Bucket (File Storage Bucket):** A separate S3 bucket is dedicated to storing user-generated content or other application files, ensuring scalable and durable object storage.

### Backend and Data Handling

* **API Gateway:** Amazon API Gateway acts as the single entry point for all API requests from the frontend. It handles routing, security, throttling, and API versioning.
* **AWS Lambda Functions (Handlers):** A collection of AWS Lambda functions serves as the backend logic, triggered by API Gateway. Each Lambda function is designed to handle specific functionalities:
    * **UserHandler:** Manages user-related operations (e.g., user profiles, credentials).
    * **TrackHandler:** Handles operations related to individual tracks or track files.
    * **PlaylistHandler:** Manages user-created playlists.
    * **FavouriteHandler:** Processes actions related to favoriting content (like a track).
    * **HistoryHandler:** Tracks user playback history.
* **DynamoDB:** Amazon DynamoDB, a fully managed NoSQL database service, provides a highly scalable, high-performance, and durable data store for the application's data. Each Lambda handler interacts with DynamoDB to perform CRUD (Create, Read, Update, Delete) operations on relevant data.

{{% notice info %}}
In order to implement every routes and handler for a complete application, it would take several hours, so in this workshop, you will only create some of the core functions
{{% /notice %}}

### Overall Flow

Users access the web application through CloudFront, which serves the UI from the Web UI S3 bucket. Amplify and Cognito manage user authentication. Authenticated users interact with the application, making API requests that are routed through API Gateway. API Gateway then invokes the appropriate Lambda function (e.g., UserHandler, TrackHandler), which in turn interacts with DynamoDB to retrieve or store data.