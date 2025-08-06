---
title : "Test API on the Frontend UI"
date :  "`r Sys.Date()`"
weight : 1
chapter : false
pre : " <b> 6.1. </b> "
---

In this step, you will:

- Make API requests to your backend from the React UI
- Test the full flow: login -> upload track -> fetch tracks

---

### Step 1: Setup Amplify in Frontend

Make sure you have added the Amplify configuration to your React project (you should have done this when you test for the register/login function before). In `src/amplify_outputs.json`, Amplify should be initialized in `/src/main.tsx` like this:

```tsx
import outputs from "../amplify_outputs.json";
import { Amplify } from "aws-amplify";

Amplify.configure(outputs);
```

This allows your React app to use authentication API by Amplify.

---

### Step 2: Sign Up and Sign In

Now login to the app using the Login form (if you have logged in before, log out by clicking the "Logout" button on the top right).

After login, Amplify will store the access token in the browser automatically. You can now make authenticated requests.

---

### Step 3: Upload a Track

On the left sidebar, click on the "My Tracks" tab. This will show you the list of tracks you have uploaded (it should be empty at this point).
![My Track page](/images/6.finalize/6.1.test-ui/1.my-tracks.png)

Click on the "Upload Track" button (the button with the upload icon). This will open a form where you can upload a track file and provide a title.
![Upload Track Form](/images/6.finalize/6.1.test-ui/2.upload-button.png)
![Upload Track Form](/images/6.finalize/6.1.test-ui/3.upload-page.png)

Fill in the form with a title and select a track file from your computer (you might want to wait a while until the `Duration` field is not 0). Then click the "Upload Track" button.

![Upload](/images/6.finalize/6.1.test-ui/4.input-name-upload.png)

---

### Step 4: Fetch Tracks
After uploading a track, you should see the track listed in the "My Tracks" section.
![My Tracks](/images/6.finalize/6.1.test-ui/5.my-tracks-with-track.png)

### Step 5: Listen to a Track
Click on the play button next to the track you have uploaded title to listen to it. The audio player should start playing the track.

![Audio Player](/images/6.finalize/6.1.test-ui/6.audio-player.png)

### Step 6: Create a Playlist
Now, let's create a playlist. Click on the "My Playlists" tab in the left sidebar. 
![My Playlists](/images/6.finalize/6.1.test-ui/7.my-playlists.png)

This will show you the list of playlists (it should be empty at this point).

Click on the "Create Playlist" button (the button with the plus icon). This will open a form where you can create a new playlist.
![New playlist](/images/6.finalize/6.1.test-ui/8.click-create-playlist.png)

Fill in the form with a name for your playlist and click the "Create Playlist" button.
![New playlist](/images/6.finalize/6.1.test-ui/9.input-playlist-name.png)

### Step 7: Add Tracks to Playlist
After creating a playlist, you can add tracks to it.

On the player, click on the "Add to Playlist" button (the button with the plus icon). This will open a modal where you can select the playlist you want to add the track to.
![Add to Playlist Modal](/images/6.finalize/6.1.test-ui/10.add-to-playlist-button.png)

Select the playlist you just created and click the "Add" button. The track should now be added to your playlist.
![Track Added to Playlist](/images/6.finalize/6.1.test-ui/11.add-to-playlist-modal.png)

### Step 8: View Playlist
You can view the playlist by clicking on the playlist name in the "My Playlists" section. 
![Playlist Details](/images/6.finalize/6.1.test-ui/12.click-playlist.png)

You should see the tracks you have added to it.
![Playlist Details](/images/6.finalize/6.1.test-ui/13.playlist-detail.png)