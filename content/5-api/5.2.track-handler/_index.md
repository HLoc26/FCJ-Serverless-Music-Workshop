---

title: "Implement TrackHandler"
date: "`r Sys.Date()`"
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
----------------------

In this section, you will explore the implementation of the `TrackHandler` Lambda function, which handles requests related to music tracks in the app.

---

### Current Handler Code

The `TrackHandler` function routes incoming HTTP requests to specific service functions:

```ts
import { APIGatewayProxyEvent } from "aws-lambda";

import { getTrackById } from './services/getTrackById';
import { deleteTrackById } from "./services/deleteTrackById";
import { postUploadTrack } from './services/postUploadTrack';

export const handler = async (event: APIGatewayProxyEvent) => {
    // GET /tracks/{id}
    if (event.httpMethod === 'GET' && event.resource === '/tracks/{id}') return await getTrackById(event);
    // DELETE /tracks/{id}
    else if (event.httpMethod === 'DELETE' && event.resource === '/tracks/{id}') return await deleteTrackById(event)
    // POST /tracks/upload
    else if (event.httpMethod === 'POST' && event.path === '/tracks/upload') return await postUploadTrack(event);
    // INVALID REQUEST
    return { statusCode: 404, body: JSON.stringify({ message: 'Not Found' }) };
};
```

---

### Your Task: Implement GET /tracks

To encourage hands-on learning, the route for `GET /tracks` and its service function `getAllTracks` have been removed from the codebase.

Your goal is to:

* **Implement the `GET /tracks` route handler** inside `TrackHandler/handler.ts`.
* **Create the corresponding `getAllTracks` function** inside `TrackHandler/services/getAllTracks.ts`.
* Ensure your function queries the `TrackTable` in DynamoDB to return a list of all tracks.


{{% notice note %}}
Remember to use the `jsonResponese` utility function to format your responses consistently.
You can browse the existing codebase to see how other routes are implemented, such as `getTrackById` and `postUploadTrack`.
Alternatively, you can read the [aws-sdk documentation](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) for DynamoDB to understand how to perform a scan operation.
{{% /notice %}}

{{<details summary="Click to view the solution">}}
```ts
// services/getAllTracks.ts
import { APIGatewayProxyResult } from "aws-lambda";
import { DynamoDB } from "aws-sdk";
import { jsonResponse } from "../../utils/response";
import { env } from "$amplify/env/TrackHandler";

const dynamoDb = new DynamoDB.DocumentClient();

export const getAllTracks = async (): Promise<APIGatewayProxyResult> => {
    const params = {
        TableName: env.TRACK_TABLE_NAME,
    };
    try {
        const result = await dynamoDb.scan(params).promise();
        return jsonResponse(200, result.Items);
    } catch (error: any) {
        return jsonResponse(500, { message: error.message });
    }
};

```

```ts
// TrackHandler/handler.ts
import { APIGatewayProxyEvent } from "aws-lambda"

import { getTrackById } from './services/getTrackById';
import { getAllTracks } from './services/getAllTracks';
import { postUploadTrack } from './services/postUploadTrack';
import { deleteTrackById } from "./services/deleteTrackById";

export const handler = async (event: APIGatewayProxyEvent) => {
    // GET /tracks
    if (event.httpMethod === 'GET' && event.path === '/tracks') return await getAllTracks()
    // GET /tracks/{id}
    else if (event.httpMethod === 'GET' && event.resource === '/tracks/{id}') return await getTrackById(event)
    // DELETE /tracks/{id}
    else if (event.httpMethod === 'DELETE' && event.resource === '/tracks/{id}') return await deleteTrackById(event)
    // POST /tracks/upload
    else if (event.httpMethod === 'POST' && event.path === '/tracks/upload') return await postUploadTrack(event)
    // INVALID REQUEST
    return { statusCode: 404, body: JSON.stringify({ message: 'Not Found' }) };
};
```
{{</details>}}

---

### Set up environment variables

In order for the TrackHandler to run correctly and access the DynamoDB table, you need to set up the environment variables.

In the `/amplify/environments` directory, there is a file named `track.env.ts` with the following content:

```ts
import { BackendType } from "../backend";
import { Tables } from "../interfaces/Tables";

export function addTrackEnv(backend: BackendType, tables: Tables) { }
```

You need to implement the `addTrackEnv` function to set up the following environment variables for the TrackHandler.

* `CLOUDFRONT_DOMAIN`: The domain of your CloudFront distribution.
* `S3_UPLOAD_BUCKET`: The name of the S3 bucket used for file uploads.
* `TRACK_TABLE_NAME`: The name of the DynamoDB table that stores tracks.
* `PLAYLIST_TABLE_NAME`: The name of the DynamoDB table that stores playlists.
* `PLAYLIST_TRACK_TABLE_NAME`: The name of the DynamoDB table that stores the relationship between playlists and tracks.
* `FAVOURITE_TABLE_NAME`: The name of the DynamoDB table that stores user favourites.
* `PLAYBACK_HISTORY_TABLE_NAME`: The name of the DynamoDB table that stores playback history.

{{% notice note %}}
You can check the other .env.ts files in the `/amplify/environments` directory for examples of how to set up environment variables for other handlers.
{{% /notice %}}

{{<details summary="Click to view the solution">}}
```ts
// amplify/environments/track.env.ts
import { BackendType } from "../backend";
import { Tables } from "../interfaces/Tables";

export function addTrackEnv(backend: BackendType, tables: Tables) {
    backend.trackHandler.addEnvironment("CLOUDFRONT_DOMAIN", "https://abcxyz.cloudfront.net"); // Replace with yours
    backend.trackHandler.addEnvironment("S3_UPLOAD_BUCKET", backend.fileBucket ? backend.fileBucket.resources.bucket.bucketName : "your-bucket-name");
    backend.trackHandler.addEnvironment("TRACK_TABLE_NAME", tables.trackTable ? tables.trackTable.tableName : "TrackTable");
    backend.trackHandler.addEnvironment("PLAYLIST_TABLE_NAME", tables.playlistTable ? tables.playlistTable.tableName : "PlaylistTable");
    backend.trackHandler.addEnvironment("PLAYLIST_TRACK_TABLE_NAME", tables.playlistTrackTable ? tables.playlistTrackTable.tableName : "PlaylisTrackTable");
    backend.trackHandler.addEnvironment("FAVOURITE_TABLE_NAME", tables.favouriteTable ? tables.favouriteTable.tableName : "FavouriteTable");
    backend.trackHandler.addEnvironment("PLAYBACK_HISTORY_TABLE_NAME", tables.playbackHistoryTable ? tables.playbackHistoryTable.tableName : "PlaybackHistoryTable");
}
```
{{</details>}}

---

### Allow TrackHandler to access DynamoDB
To allow the `TrackHandler` to access the DynamoDB tables, you need to add the necessary permissions in the `amplify/permissions/lambdaPerms.ts` file.

In detail, you need to add the following permissions for the `TrackHandler` to access:
* `fileBucket`: Put and Delete for uploading and deleting files.
* `TrackTable`: For reading and writing track data.
* `PlaylistTable`: For reading and writing playlist data.
* `PlaylistTrackTable`: To reading and writing the relationship between playlists and tracks.
* `FavouriteTable`: For reading and writing user favourites.
* `PlaybackHistoryTable`: For reading and writing playback history data. 


{{<details summary="Click to view the solution">}}
```ts
    // Track Handler permissions
    backend.fileBucket.resources.bucket.grantPut(backend.trackHandler.resources.lambda);
    backend.fileBucket.resources.bucket.grantDelete(backend.trackHandler.resources.lambda);
    tables.trackTable.grantReadWriteData(backend.trackHandler.resources.lambda);
    tables.playlistTable?.grantReadWriteData(backend.trackHandler.resources.lambda);
    tables.playlistTrackTable?.grantReadWriteData(backend.trackHandler.resources.lambda);
    tables.favouriteTable?.grantReadWriteData(backend.trackHandler.resources.lambda);
    tables.playbackHistoryTable?.grantReadWriteData(backend.trackHandler.resources.lambda);
```
{{</details>}}

### Deploying Your Changes

After implementing the `GET /tracks` route and the `getAllTracks` service function, you need to deploy your changes to AWS Lambda by running the following command in your terminal at the root of the project:

```bash
npx ampx sandbox
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

### Testing Your Endpoint

* Go to the [API Gateway console](https://console.aws.amazon.com/apigateway).
    ![API Gateway Console](/images/5.api/5.2.track-handler/1.api-gateway-console.png)
* On the left sidebar, click on `APIs`.
    ![Click APIs](/images/5.api/5.2.track-handler/2.click-apis.png)
* Select the API named `fcjmusicrestapi`.
    ![Select API name](/images/5.api/5.2.track-handler/3.click-api-name.png)
* Now you will see several endpoints have been defined. Click on the `/tracks` resource and select the `GET` method.
    ![Select GET](/images/5.api/5.2.track-handler/4.select-get.png)
* On the right side, click on `Test` tab.
    ![Test tab](/images/5.api/5.2.track-handler/5.test-tab.png)
* In Query String Parameters and Headers, you can leave it empty.
* Click on `Test` to execute the request.
    ![Click test button](/images/5.api/5.2.track-handler/6.click-test.png)
* You will see the response in the `Response` section, which should contain an empty list of tracks in JSON format. 
    ![API Gateway Test Response](/images/5.api/5.2.track-handler/7.response.png)
