---
title : "Define API Gateway"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 5.4. </b> "
---

The Test feature in API Gateway is a powerful tool that allows you to test your Lambda functions directly from the AWS console. However, when the Lambda function requires Authorization provided by Cognito (as in our project), you need to send the request through the API Gateway to ensure the request is authenticated properly.

In this section, you will learn how to set up the API Gateway that connects your Lambda functions to the HTTP endpoints. This will allow you to interact with your backend services using RESTful API calls.

We won’t be implementing this from scratch. Instead, you will review the code and understand how it maps API routes to the backend logic you’ve seen in the `PlaylistHandler`, and `TrackHandler` functions.

The following files are used to set up the API Gateway:

```
amplify/
└── api/
    ├── gateway.ts
    └── routes/
        ├── favourites.ts
        ├── history.ts
        ├── playlists.ts
        ├── tracks.ts
        └── user.ts
```

## `gateway.ts`

The gateway.ts file defines the entire API and attaches all Lambda handlers and route files to the API Gateway.

Here’s what it does:
* Creates the API Gateway with CORS enabled.
* Uses Cognito for authentication on routes.
* Maps route files (tracks.ts, playlists.ts, etc.) to their respective Lambda integrations.

```ts
import {
    CognitoUserPoolsAuthorizer,
    Cors,
    LambdaIntegration,
    RestApi
} from "aws-cdk-lib/aws-apigateway";
import { Stack } from "aws-cdk-lib";

import { BackendType } from "../backend"
import { createUserRoutes } from './routes/user';
import { createTrackRoutes } from './routes/tracks';
import { createPlaylistRoutes } from './routes/playlists';
import { createFavouriteRoutes } from './routes/favourites';
import { createHistoryRoutes } from './routes/history';

export function createApiGateway(backend: BackendType): { restApi: RestApi, apiStack: Stack } {
    const apiStack = backend.createStack("api-stack");

    const restApi = new RestApi(apiStack, "RestApi", {
        restApiName: "fcjmusicrestapi",
        deploy: true,
        deployOptions: {
            stageName: "dev"
        },
        defaultCorsPreflightOptions: {
            allowOrigins: Cors.ALL_ORIGINS,
            allowMethods: Cors.ALL_METHODS,
            allowHeaders: Cors.DEFAULT_HEADERS
        }
    });

    const cognitoAuth = new CognitoUserPoolsAuthorizer(apiStack, "CognitoAuth", {
        cognitoUserPools: [backend.auth.resources.userPool],
    });

    // Create Lambda integrations
    const integrations = {
        favourite: new LambdaIntegration(backend.favouriteHandler.resources.lambda),
        listeningHistory: new LambdaIntegration(backend.listeningHistoryHandler.resources.lambda),
        playlist: new LambdaIntegration(backend.playlistHandler.resources.lambda),
        track: new LambdaIntegration(backend.trackHandler.resources.lambda),
        user: new LambdaIntegration(backend.userHandler.resources.lambda)
    };

    // Create routes
    createUserRoutes(restApi, integrations.user, cognitoAuth);
    createTrackRoutes(restApi, integrations.track, cognitoAuth);
    createPlaylistRoutes(restApi, integrations.playlist, cognitoAuth);
    createFavouriteRoutes(restApi, integrations.favourite, cognitoAuth);
    createHistoryRoutes(restApi, integrations.listeningHistory, cognitoAuth);

    return { restApi, apiStack };
}
```

Notice how each route module like `playlistsRouter` is imported and mounted to the main router. This makes it easy to scale the API by keeping logic modular.

## Example Route File: `routes/tracks.ts`

This file defines what happens when the API receives requests at `/tracks`.

```ts
import { AuthorizationType, CognitoUserPoolsAuthorizer, LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";

export function createTrackRoutes(restApi: RestApi, trackIntegration: LambdaIntegration, cognitoAuth: CognitoUserPoolsAuthorizer) {
    const tracksPath = restApi.root.addResource("tracks");

    // GET /tracks
    tracksPath.addMethod("GET", trackIntegration, {
        authorizationType: AuthorizationType.COGNITO,
        authorizer: cognitoAuth
    });

    const trackIdResource = tracksPath.addResource("{id}");
    // GET /tracks/{id}
    trackIdResource.addMethod("GET", trackIntegration, {
        authorizationType: AuthorizationType.COGNITO,
        authorizer: cognitoAuth
    });

    // DELETE /tracks/{id}
    trackIdResource.addMethod("DELETE", trackIntegration, {
        authorizationType: AuthorizationType.COGNITO,
        authorizer: cognitoAuth
    });

    // POST /tracks/upload
    tracksPath.addResource("upload").addMethod("POST", trackIntegration, {
        authorizationType: AuthorizationType.COGNITO,
        authorizer: cognitoAuth
    });
}
```

Those endpoints are then linked to the `TrackHandler` functions you defined earlier:

```ts
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

## Testing API Gateway

### Step 1. Retrieve the API URL
After deployment (using `npx ampx sandbox`), check the API Gateway console to see your new API.
1. Go to the [API Gateway console](https://console.aws.amazon.com/apigateway).
   ![API Gateway Console](/images/5.api/5.4.api-gateway/1.api-gateway-console.png)
2. Click on `APIs` in the left sidebar.
   ![Click APIs](/images/5.api/5.4.api-gateway/2.click-apis.png)
3. Select your API (e.g., `fcjmusicrestapi`).
   ![Click API name](/images/5.api/5.4.api-gateway/3.click-api-name.png)
4. On the left sidebar, click on `Stages`, and choose the `dev` stage.
   ![Click Stages](/images/5.api/5.4.api-gateway/4.click-stages-dev.png)
5. You will see the base URL for your API, which you can use to test endpoints. 
   ![Invoke URL](/images/5.api/5.4.api-gateway/5.invoke-url.png)
6. Save the URL
7. Now you can test your endpoints using tools like Postman.

### Step 2. Test the Endpoints

{{% notice note %}}
The following steps require Postman to make requests to the API, so make sure you have the software installed.
{{% /notice %}}

#### Step 2.1. Get the JWT Token
Before you can upload files, you need to authenticate and obtain a JWT token. You can use the Login function in the web UI to retrieve the token.
1. Open the web's [login page](http://localhost:5173/login).
2. Login with your credentials.
    ![Login Form](/images/5.api/5.4.api-gateway/6.login.png)
3. After logging in, press F12 on your keyboard, choose tab Console, you can find the JWT token.
    ![JWT Token](/images/5.api/5.4.api-gateway/7.jwt.png)
4. Save the JWT token for use in the next steps.

#### Step 2.2. Test the GET /tracks Endpoint
1. Open Postman and create a new request.
    ![New request](/images/5.api/5.4.api-gateway/8.new-request.png)
2. Set the request type to `GET`.
    ![Method GET](/images/5.api/5.4.api-gateway/9.select-get.png)
3. Enter the URL: `<your-api-url>/tracks`.
    ![Enter URL](/images/5.api/5.4.api-gateway/10.input-url.png)
4. In the Authorization tab, select `Bearer Token` for **Auth Type**.
    ![Bearer Token](/images/5.api/5.4.api-gateway/11.bearer-token.png)
5. Paste the JWT token you obtained earlier into the **Token** field.
    ![Paste Token](/images/5.api/5.4.api-gateway/12.paste-token.png)
5. Click `Send`, and you will receive the response (it should be an empty array by now).
    ![Send - Response](/images/5.api/5.4.api-gateway/13.response.png)

### Step 3. Test the API using UI

#### Step 3.1. Update the API endpoint in the UI
1. Open `src/api/client.ts`.
    ![client.ts](/images/5.api/5.4.api-gateway/14.client.ts.png)
2. On line 4, replace the `API_URL` with your API URL.
    ```ts
        baseURL: "https://<your-api-url>/dev",
    ```
    ![Replace with API Gateway Invoke URL](/images/5.api/5.4.api-gateway/15.replace)
3. Open UI in your browser (e.g., `http://localhost:5173`) to see if the UI is working correctly with the API.
    ![On UI](/images/5.api/5.4.api-gateway/16.api-work.png)
