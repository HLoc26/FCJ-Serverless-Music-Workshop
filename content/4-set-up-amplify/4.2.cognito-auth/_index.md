---
title : "Set Up Auth with Cognito"
date : "`r Sys.Date()`"
weight : 2
chapter : false
pre : " <b> 4.2. </b> "
---


In this step, you'll configure authentication for your music app using **AWS Amplify Gen 2** and **Amazon Cognito**. We'll create a User Pool, configure registration/login settings, and test the flow manually using the AWS Console.

![What you will do](/images/4.amplify/4.2.cognito-auth/what-you-will-do.png)

---

### Step 1: Define Auth Resource

We've already added a partial `auth.ts` file for you in the Amplify backend at amplify/backend/auth/resource.ts:

```ts
import { defineAuth } from '@aws-amplify/backend';

/**
 * Define and configure your auth resource
 * @see https://docs.amplify.aws/gen2/build-a-backend/auth
 */
export const auth = defineAuth({
  loginWith: {
    email: true,
  },
  userAttributes: {
    preferredUsername: {
      mutable: true,
      required: true
    }
  }
});
```


You need to check the following configuration:

- `email` login is enabled: This enables login with an email address and password. Users will register and sign in using their email as their username.
- `preferredUsername`: This defines a user attribute for a preferred display name or username, which is different from the login email.

---

### Step 2: Connect Auth to Backend

Now that you've defined the `auth` resource in `resource.ts`, you need to connect it to your Amplify backend by importing it in `amplify/backend.ts`.

Open `backend.ts` and add the following import statement:

```ts
import { auth } from './auth/resource';
```

This line tells Amplify to include the `auth` configuration when you deploy your backend.

Your `backend.ts` file should now have this line:

```ts
// amplify/backend/backend.ts
import { auth } from './auth/resource';

// You can import other resources here as needed
```

Below, you can see a constant named `backend` is being defined. It is missing the `auth` resource. Can you add it in?


{{< details summary="Click to show solution" >}}
Your backend definition should look like this:
```ts
const backend = defineBackend({
  	auth,
	// .. Other resources
});
```
{{< /details >}}

After saving the file, you're ready to deploy the authentication setup.

---

### Step 3: Deploy Auth with Amplify

Run the following in the root folder:

```bash
npx ampx sandbox
```

{{% notice tip %}}
If you are using a profile other than the default profile, remember to add `--profile <your-profile>`.
{{% /notice %}}

This will create a Cognito User Pool and related resources in your AWS account.

Once deployment finishes, go to **AWS Console > Cognito > User Pools** and verify your pool is created. You will see a new User pool with name `amplifyAuthUserPool...`

![Newly created User Pool](/images/4.amplify/4.2.cognito-auth/0.new-user-pool.png)

---

### Step 4: Using Amplify for User Registration and Login in UI

Now that the User Pool is set up, you can use Amplify's authentication API to handle user registration and login in your web app.

#### Step 4.1: Install Amplify Auth Library
Run the following command to install the Amplify Auth library:

```bash
npm install @aws-amplify/auth
```

This library provides methods to interact with the Cognito User Pool for user registration, login, and management.

#### Step 4.2: Configure Amplify Auth in the application
In the main application file (`src/main.ts`), ensure you have import and configure Amplify Auth:

```ts
import { Amplify } from "aws-amplify";
import outputs from "../amplify_outputs.json";
Amplify.configure(outputs);
```

#### Step 4.3: Edit the Register hook
In the `src/hooks/useRegister.ts` file, you can use Amplify's Auth API to handle user registration. The existing code already has the necessary logic to register a user with email and preferred username. This hook will be used in the registration form to create a new user in the Cognito User Pool.

In the `useRegister.ts` file, you can see the following code being commented out:

```ts
await Auth.signUp({
	username: email,
	password,
	options: {
		userAttributes: {
			preferred_username: username,
		},
	},
});
```
This code is responsible for registering a new user in the Cognito User Pool. It uses the `Auth.signUp` method from the Amplify Auth library, passing the user's email as the username, their password, and any additional attributes like `preferred_username`.

Uncomment this code to enable user registration functionality.

#### Step 4.4: Edit the Login hook
In the `src/hooks/useLogin.ts` file, you can use Amplify's Auth API to handle user login. The existing code already has the necessary logic to log in a user with email and password.
In the `useLogin.ts` file, you can see the following code being commented out:

```ts
await Auth.signIn({
	username: email,
	password: password,
});
```
This code is responsible for logging in a user using their email and password. It uses the `Auth.signIn` method from the Amplify Auth library, passing the user's email as the username and their password.

Similarly, uncomment this code to enable user login functionality.

### Step 5: Test Registration

#### Step 5.1: Check User Pool
Click on the User pool created by Amplify. 
![User list](/images/4.amplify/4.2.cognito-auth/0.user-pool-interface.png)

On the left side bar, select Users under User Management.
![User list](/images/4.amplify/4.2.cognito-auth/1.click-on-user.png)
![User list](/images/4.amplify/4.2.cognito-auth/1.user-list.png)

#### Step 5.2: Register a New User

Now, go to the web app's [register page](http://localhost:5173/register) and try registering a new user with:

- Email (your real email to receive confirm OTP)
- Preferred username
- Password

![Resiger form](/images/4.amplify/4.2.cognito-auth/2.register-page-fill.png)

And click **Register**. After registration, you will be redirected to the email confirmation page.

{{%notice tip%}}
You can check the User Pool in the AWS Console to see the new user appears in the User Pool with the status `UNCONFIRMED`.
![Unconfirmed User](/images/4.amplify/4.2.cognito-auth/3.unconfirmed-user.png)
{{% /notice %}}

#### Step 5.3: Confirm User

Now, you need to confirm the user email.

Go to your mailbox and find the confirmation email sent by Cognito. It should look like this:
![Confirmation email](/images/4.amplify/4.2.cognito-auth/4.email-otp-confirm.png)

Now, enter the confirmation code in the web app's confirmation page and click **Confirm**.
![Confirmation form](/images/4.amplify/4.2.cognito-auth/5.confirm-form.png)

{{% notice tip %}}
If you don't receive the email, check your spam folder or ensure you entered the correct email address. If you accidentally registered with a wrong email, you can delete the user from the User Pool in the AWS Console and try again.
{{% /notice %}}

In the AWS Console, you should now see the user status updated to `CONFIRMED`.
![Confirmed User](/images/4.amplify/4.2.cognito-auth/6.user-confirmed.png)

---

### Step 6: Test Login

Now you can use your email and password to log in through the web UI.
![Login page](/images/4.amplify/4.2.cognito-auth/7.login.png)
After successful login, you will be redirected to the home page, and you should see a welcome message with your preferred username.
![Home page after login](/images/4.amplify/4.2.cognito-auth/8.home-page.png)

---

Next, we'll connect DynamoDB tables to your backend logic.
