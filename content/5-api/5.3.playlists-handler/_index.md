---
title: "Implement PlaylistHandler"
date :  "`r Sys.Date()`" 
weight : 3 
chapter : false
pre : " <b> 5.3. </b> "
---

In this step, you will implement the core logic for managing user playlists in your backend.

You are required to complete two Lambda function routes inside `PlaylistHandler`:

* `POST /playlists`: Create a new playlist
* `GET /playlists/{id}`: Retrieve a playlist by its ID

A skeleton handler has already been created for you at: `amplify/functions/PlaylistHandler/services/postPlaylists.ts` and `amplify/functions/PlaylistHandler/services/getPlaylistById.ts`

---
### Implement the POST /playlists Route

#### Step 1. Create the service
A file named `postPlaylists.ts` has already been created in `amplify/functions/PlaylistHandler/services/` for you. Your misson is to implement the logic to create a new playlist.

{{<details summary="View the code snippet">}}
```ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDB } from 'aws-sdk';
import { v4 as uuidv4 } from 'uuid';
import { jsonResponse } from '../../utils/response';
import { env } from "$amplify/env/PlaylistHandler"

const db = new DynamoDB.DocumentClient();

export const postPlaylists = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    const userId = event.requestContext.authorizer?.claims?.sub;
    if (!userId) return jsonResponse(401, { message: 'Unauthorized' });

    const body = JSON.parse(event.body || '{}');
    try {
        const playlistId = uuidv4();
        const item = {
            id: playlistId,
            owner: userId,
            name: body.name,
            trackCount: 0,
            createdAt: new Date().toISOString(),
        };

        await db.put({ TableName: env.PLAYLIST_TABLE_NAME!, Item: item }).promise();
        return jsonResponse(201, { playlist: item });
    } catch (error: any) {
        return jsonResponse(500, { message: error.message })
    }
};
```
{{< /details >}}

#### Step 2. Define the Route
In your `amplify/backend/function/PlaylistHandler/handler.ts`, add the route POST /playlists to your function (remember to import the service at the top of the file):

```ts
else if (httpMethod === 'POST' && path === '/playlists') return postPlaylists(event);
```

### Implement the GET /playlists/{id} Route

#### Step 1: Create the service
A file named `getPlaylistById.ts` has already been created in `amplify/functions/PlaylistHandler/services/` for you. Your misson is to implement the logic to retrieve a playlist by its ID.

{{<details summary="View the code snippet">}}
```ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDB } from 'aws-sdk';
import { jsonResponse } from '../../utils/response';
import { env } from '$amplify/env/PlaylistHandler';

const db = new DynamoDB.DocumentClient();

export const getPlaylistById = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    const playlistId = event.pathParameters?.id;
    if (!playlistId) return jsonResponse(400, { message: 'Missing playlist ID' });

    const params = {
        TableName: env.PLAYLIST_TABLE_NAME,
        Key: { id: playlistId },
    };

    try {
        const result = await db.get(params).promise();
        if (!result.Item) {
            return jsonResponse(404, { message: 'Playlist not found' });
        }
        return jsonResponse(200, result.Item);
    } catch (error: any) {
        console.error('Error fetching playlist:', error);
        return jsonResponse(500, { message: error.message });
    }
};
```
{{< /details >}}

#### Step 2. Define the Route
In your `amplify/backend/function/PlaylistHandler/resource.ts`, add the route GET /playlists/{id} to your function (remember to import the service at the top of the file):

```ts
else if (httpMethod === 'GET' && resource === '/playlists/{id}') return getPlaylistById(event);
```

### Set up environment variables
Similar to the `TrackHandler`, you need to set up the environment variables for the `PlaylistHandler` in `/amplify/environments/track.env.ts`.

You will need:
- `PLAYLIST_TABLE_NAME`: The name of the DynamoDB table for playlists.
- `PLAYLIST_TRACK_TABLE_NAME`: The name of the DynamoDB table for playlist tracks.
- `TRACK_TABLE_NAME`: The name of the DynamoDB table for tracks.

{{<details summary="Click to view the solution">}}
```ts
import { BackendType } from "../backend";
import { Tables } from "../interfaces/Tables";

export function addPlaylistEnv(backend: BackendType, tables: Tables) {
    backend.playlistHandler.addEnvironment("PLAYLIST_TABLE_NAME", tables.playlistTable ? tables.playlistTable.tableName : "PlaylistTable");
    backend.playlistHandler.addEnvironment("PLAYLIST_TRACK_TABLE_NAME", tables.playlistTrackTable ? tables.playlistTrackTable.tableName : "PlaylistTrackTable");
    backend.playlistHandler.addEnvironment("TRACK_TABLE_NAME", tables.trackTable ? tables.trackTable.tableName : "TrackTable");
}
```
{{</details>}}

### Allow PlaylistHandler to access DynamoDB

Again, similar to the `TrackHandler`, you need to allow the `PlaylistHandler` to access the DynamoDB tables.

In detail, you need to add the following permissions for the `PlaylistHandler` to access:
- `playlistTable`: Allow read/write access to the playlist table.
- `trackTable`: Allow read access to the track table.
- `playlistTrackTable`: Allow read/write access to the playlist track table.

{{<details summary="Click to view the solution">}}
```ts
    tables.playlistTable?.grantReadWriteData(backend.playlistHandler.resources.lambda);
    tables.trackTable.grantReadData(backend.playlistHandler.resources.lambda);
    tables.playlistTrackTable?.grantReadWriteData(backend.playlistHandler.resources.lambda);
```
{{</details>}}

---

### Deploy and Test Your Changes
#### Deploy Your Changes
After implementing the above routes, deploy your changes:

```bash
npx ampx sandbox
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

In the next part, you will learn how to deploy API Gateway and test your newly created endpoints.