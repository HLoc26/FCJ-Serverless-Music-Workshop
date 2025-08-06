---
title: "Function Folder Structure"
date: "`r Sys.Date()`"
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

Before implementing and deploying your Lambda functions, it's important to understand how the function code is organized in the project.

In this section, you will:

- Explore the folder structure of `amplify/functions`
- Understand the responsibilities of `handler.ts`, `resource.ts`, and `services/`
- Reuse this pattern for adding new logic

---

### Overview

Your Amplify backend project includes five main Lambda functions, each in its own folder under `amplify/functions`:

```bash
amplify/
└── functions/
    ├── FavouriteHandler/
    ├── ListeningHistoryHandler/
    ├── PlaylistHandler/
    ├── TrackHandler/
    ├── UserHandler/
    └── utils/
```

Each function folder contains the following:

| File/Folder   | Description                                                                            |
| ------------- | -------------------------------------------------------------------------------------- |
| `handler.ts`  | Entry point for the Lambda function. Amplify uses this as the function's main handler. |
| `resource.ts` | Amplify configuration for building and deploying the function.                         |
| `services/`   | All actual business logic. This folder contains one file per HTTP route.               |

---

### Example: `TrackHandler`

Let's look at the structure for the `TrackHandler` function:

```bash
TrackHandler/
├── services/
│   ├── deleteTrackById.ts
│   ├── getAllTracks.ts
│   ├── getTrackById.ts
│   └── postUploadTrack.ts
├── handler.ts
└── resource.ts
```

- `handler.ts` dispatches incoming requests to the appropriate file in `services/`.
- Each file in `services/` corresponds to one REST endpoint. For example:
  - `GET /tracks` → `getAllTracks.ts`
  - `POST /tracks/upload` → `postUploadTrack.ts`

This structure allows you to keep the Lambda entry point simple and organize logic into small, testable units.

---

### Example: handler.ts

Below is a sample version of a typical handler:

```ts
// TrackHandler/handler.ts
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

### Shared Utilities

Common helper functions like standardized response with headers formatting are stored in:

```bash
amplify/utils/
└── response.ts
```

```ts
export const jsonResponse = (statusCode: number, data: any) => {
    const corsHeaders = {
        'Access-Control-Allow-Origin': 'http://localhost:5173', // You should replace this with your actual frontend URL
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
        'Access-Control-Allow-Credentials': 'true',
        'Content-Type': 'application/json'
    };
    return {
        statusCode,
        headers: corsHeaders,
        body: JSON.stringify(data),
    }
};

```

This keeps repeated code out of your business logic files.

---

### Your Task

In the next steps, you will:

1. Implement `TrackHandler` and `PlaylistHandler` using this structure
2. Wire them to API Gateway routes
3. Deploy and test your endpoints

![Amplify Lambda function structure](/images/5.api/functions-structure.png)

{{% notice tip %}}
You only need to touch `handler.ts` and the `services/` folder. Avoid editing `resource.ts` unless you’re changing function config.
{{% /notice %}}
