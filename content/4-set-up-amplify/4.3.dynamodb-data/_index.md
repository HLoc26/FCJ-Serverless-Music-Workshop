---
title : "Set Up Database with DynamoDB"
date : "`r Sys.Date()`"
weight : 3
chapter : false
pre : " <b> 4.3. </b> "
---
In this step, you'll set up a DynamoDB table to store your music app data using **AWS Amplify Gen 2**. We'll define the table schema, connect it to the backend.

![What you will create: DynamoDB tables](/images/4.amplify/4.3.dynamodb-data/what-you-will-do.png)
---

### Step 1: Define DynamoDB Resource
We've already added a partial `dynamodb.ts` file for you in the Amplify backend at `amplify/database/tables.ts`:

```ts
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { BackendType } from '../backend';
import { Tables } from '../interfaces/Tables';

export function createDynamoDBTables(backend: BackendType): Tables {
    const userTable = new dynamodb.TableV2(backend.stack, 'UserTable', {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        tableName: 'UserTable',
    });

    const trackTable = new dynamodb.TableV2(backend.stack, 'TrackTable', {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        tableName: 'TrackTable',
        globalSecondaryIndexes: [
            {
                indexName: 'byUserId',
                partitionKey: { name: 'uploadedBy', type: dynamodb.AttributeType.STRING },
            },
        ],
    });

    return {
        userTable,
        trackTable,
    };
}
```
{{% notice note %}}
The `createDynamoDBTables` function is already called in the `amplify/backend.ts` file for you.
{{% /notice %}}

{{< details summary="Click to show how to write DynamoDB tables" >}}

Let's walk through the structure of the two sample tables in your code:

**1. `UserTable` – basic table with only a partition key**

```ts
const userTable = new dynamodb.TableV2(backend.stack, 'UserTable', {
  partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
  tableName: 'UserTable',
});
```

* **`UserTable`** is the logical ID used by CDK.
* **`partitionKey`** is required. Here it's a string field named `"id"`.
* **`tableName`** is the actual name that will appear in the AWS Console.

This is the simplest kind of table: 1 partition key, no sort key, no secondary indexes.

**2. `TrackTable` – has a partition key and a global secondary index (GSI)**

```ts
const trackTable = new dynamodb.TableV2(backend.stack, 'TrackTable', {
  partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
  tableName: 'TrackTable',
  globalSecondaryIndexes: [
    {
      indexName: 'byUserId',
      partitionKey: { name: 'uploadedBy', type: dynamodb.AttributeType.STRING },
    },
  ],
});
```

* Similar to `UserTable`, the **partitionKey** is `"id"`.
* The **GSI** named `"byUserId"` lets you query tracks by the user who uploaded them (`uploadedBy`).
* GSIs are defined in the `globalSecondaryIndexes` array. Each needs an `indexName` and a `partitionKey`.

Once you understand these two patterns, you'll be able to define the rest of the tables: some will add a `sortKey`, others may use a GSI or both.

{{< /details >}}

#### Now it's your turn
Based on the structure of UserTable and TrackTable, define the remaining DynamoDB tables by yourself:
- `PlaylistTable`: Use id as primary key and owner as a GSI.
- `PlaylistTrackTable`: Use playlistId as partition key and trackId as sort key.
- `FavouriteTable`: Use userId as partition key and trackId as sort key.
- `PlaybackHistoryTable`: Use userId as partition key and timestamp as sort key.
Add them to the `createDynamoDBTables()` function.
When you're done, return the new tables in the final object so they can be used in the rest of the backend logic.

{{< details summary="Click to show solution" >}}
You can copy all the code below to your `amplify/database/tables.ts` file, replacing the existing content. This will create all the necessary DynamoDB tables for your music app.
```ts
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { BackendType } from '../backend';
import { Tables } from '../interfaces/Tables';

export function createDynamoDBTables(backend: BackendType): Tables {
    const userTable = new dynamodb.TableV2(backend.stack, 'UserTable', {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        tableName: 'UserTable',
    });

    const trackTable = new dynamodb.TableV2(backend.stack, 'TrackTable', {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        tableName: 'TrackTable',
        globalSecondaryIndexes: [
            {
                indexName: 'byUserId',
                partitionKey: { name: 'uploadedBy', type: dynamodb.AttributeType.STRING },
            },
        ],
    });

    const playlistTable = new dynamodb.TableV2(backend.stack, 'PlaylistTable', {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        tableName: 'PlaylistTable',
        globalSecondaryIndexes: [
            {
                indexName: 'byUserId',
                partitionKey: { name: 'owner', type: dynamodb.AttributeType.STRING },
            },
        ],
    });

    const playlistTrackTable = new dynamodb.TableV2(backend.stack, 'PlaylistTrackTable', {
        partitionKey: { name: 'playlistId', type: dynamodb.AttributeType.STRING },
        sortKey: { name: 'trackId', type: dynamodb.AttributeType.STRING },
        tableName: 'PlaylistTrackTable',
    });


    const favouriteTable = new dynamodb.TableV2(backend.stack, 'FavouriteTable', {
        partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING },
        sortKey: { name: 'trackId', type: dynamodb.AttributeType.STRING },
        tableName: 'FavouriteTable',
    });

    const playbackHistoryTable = new dynamodb.TableV2(backend.stack, 'PlaybackHistoryTable', {
        partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING },
        sortKey: { name: 'timestamp', type: dynamodb.AttributeType.STRING },
        tableName: 'PlaybackHistoryTable',
    });

    return {
        userTable,
        trackTable,
        playlistTable,
        playlistTrackTable,
        favouriteTable,
        playbackHistoryTable
    };
}
```
{{< /details >}}

#### Deploy the Changes
After defining the tables, you can deploy your changes to see them in the AWS Console. Run the following in the root folder:

```bash
npx ampx sandbox
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

This command will deploy your backend changes, including the new DynamoDB tables you just defined. Once the deployment is complete, you can check the AWS Console to see your newly created tables.

### Step 2: Check the Tables in AWS Console
After defining the tables, you can deploy your changes to see them in the AWS Console.

1. Go to the [AWS Management Console](https://aws.amazon.com/console/) and search for DynamoDB.
    ![Search DynamoDB](/images/4.amplify/4.3.dynamodb-data/1.search-dynamo.png)
2. Navigate to the **DynamoDB** service. On the left sidebar, click on **Tables**.
    ![Left side bar > Tables](/images/4.amplify/4.3.dynamodb-data/2.click-tables.png)
1. You should see the tables you defined: `UserTable`, `TrackTable`, `PlaylistTable`, `PlaylistTrackTable`, `FavouriteTable`, and `PlaybackHistoryTable`.
    ![Newly created tables](/images/4.amplify/4.3.dynamodb-data/3.tables.png)

### Step 3: Set up IAM Permissions

To allow your frontend app to access these DynamoDB tables securely, you'll define IAM permissions for authenticated users.

We've prepared a helper function `setupIAMPermissions` in `amplify/permissions/iamPerms.ts`, with some lines commented out for you to complete (those lines only works after you have defined the tables). This function will be called automatically when you deploy your backend:

```ts
import { PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Tables } from '../interfaces/Tables';
import { BackendType } from '../backend';

export function setupIAMPermissions(backend: BackendType, tables: Tables) {
    const authRole = backend.auth.resources.authenticatedUserIamRole;
    if (!authRole) return;

    // Read permissions for all tables
    authRole.addToPrincipalPolicy(
        new PolicyStatement({
            actions: ['dynamodb:GetItem', 'dynamodb:Query', 'dynamodb:Scan'],
            resources: [
                tables.userTable.tableArn,
                tables.trackTable.tableArn,
                // tables.playlistTable.tableArn,
                // tables.playlistTrackTable.tableArn,
                // `${tables.playlistTrackTable.tableArn}/index/*`,
                // tables.favouriteTable.tableArn,
                // tables.playbackHistoryTable.tableArn,
            ],
        })
    );

    // Write permissions for user-specific tables
    // authRole.addToPrincipalPolicy(
    //     new PolicyStatement({
    //         actions: ['dynamodb:PutItem', 'dynamodb:UpdateItem', 'dynamodb:DeleteItem'],
    //         resources: [
    //             tables.favouriteTable.tableArn,
    //             tables.playbackHistoryTable.tableArn,
    //         ],
    //         conditions: {
    //             'ForAllValues:StringEquals': {
    //                 'dynamodb:LeadingKeys': ['${aws:username}'],
    //             },
    //         },
    //     })
    // );

    // Write permissions for general tables
    authRole.addToPrincipalPolicy(
        new PolicyStatement({
            actions: ['dynamodb:PutItem', 'dynamodb:UpdateItem', 'dynamodb:DeleteItem'],
            resources: [
                tables.userTable.tableArn,
                tables.trackTable.tableArn,
                // tables.playlistTable.tableArn,
                // tables.playlistTrackTable.tableArn,
                // `${tables.playlistTrackTable.tableArn}/index/*`,
            ],
        })
    );
}
```

{{< details summary="" >}}

This policy configuration is split into three parts:

1. **Read access** for all tables
   Authenticated users can read any table using `GetItem`, `Query`, or `Scan`.

2. **Write access for user-specific data**
   Users can write only to rows where the partition key matches their own `aws:username` — this ensures they can't update others' data in `FavouriteTable` or `PlaybackHistoryTable`.

3. **Write access for system-owned tables**
   Backend logic (like creating new tracks or playlists) needs write access to shared tables, so this is granted without condition.

This strikes a balance between security and flexibility for your app.

{{< /details >}}

Now uncomment those lines, and run the following command to apply the permissions:

```bash
npx ampx sandbox
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

The function is already called in `amplify/permissions/index.ts`, so you don't need to do anything extra to apply it.

### Recap

By now, you've:

* Defined and deployed all DynamoDB tables needed for your music app
* Verified them in the AWS Console
* Applied permission rules for authenticated users to interact with the tables securely

You're ready to start building out APIs to read and write music data.

