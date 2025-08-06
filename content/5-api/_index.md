---
title : "Deploying API Gateway and Lambda"
date :  "`r Sys.Date()`" 
weight : 5 
chapter : false
pre : " <b> 5. </b> "
---
Each feature in our music app is powered by a dedicated AWS Lambda function. These functions handle different business logic and will be wired to an API Gateway in the next step.


In this section, you will:

- Learn how to define multiple Lambda functions using Amplify Gen 2
- Define IAM permissions for each function
- Connect functions to DynamoDB and S3 using environment variables
- Understand how code is structured and passed to the cloud
- Deploy your functions and test them individually

---

### What You Will Deploy

![What you will do](/images/5.api/what-you-will-do.png)

You will set up five Lambda functions:

| Function Name             | Purpose                              | Your Task                                       |
| ------------------------- | ------------------------------------ | ----------------------------------------------- |
| `UserHandler`             | Manage user profiles                 | -                                               |
| `TrackHandler`            | Handle uploading and querying tracks | Create handler for getting tracks               |
| `PlaylistHandler`         | Manage playlists                     | Create handler for create and getting playlists |
| `FavouriteHandler`        | Add/remove tracks from favourites    | -                                               |
| `ListeningHistoryHandler` | Store user listening activity        | -                                               |

{{% notice note %}}
Since defining all functions at once can be overwhelming, you only need to implement the `TrackHandler` and `PlaylistHandler` functions in this step. The others are already implemented for you.
{{% /notice %}}