# MusiCoco Bot
Make public playlists with friends on the MusiCoco Spotify Account, or authorisethe bot to manage your account.

## Using the Bot to make Public Playlists on Discord

### Setup
You can directly use the bot by inviting it to your server on this [link](<>)

Alternatively, you can customise the bot for your usage, or run locally by changing the `.env`. 

- Update your `SPOTIFY_USER_ID`
- Update your `SPOTIFY_AUTHORIZATION_TOKEN`
- Update your `CLIENT_ID`
- Update your `CLIENT_SECRET`

You will also require a refresh token incase you want to change the auth token. You can get it [here](https://getyourspotifyrefreshtoken.herokuapp.com/)

  
### Usage 
  All commands are preceded by a `!`
  - `!help` to view help regarding the commands
  
  - `!join` to join the userbase. This is required the first time you use the bot. 
  
  - `!set <playlist name>` to set current playlist to `<playlist name>`. You will be prompted to add <playlist name> if it doesn't exist.
  
  - `!add <song name>` to add a song to the set playlist.  
  
  - `!list` to list your playlist.
  
  - `!list<number>` to list playlists on page number <number>.
  
  - `!list all` to list ALL the playlists in the userbase, haha, just don't use this :)
  
  - `!rename <new_name>` to rename the set playlist to <new_name>
  
  - `!describe` to add a describe the set playlist to the specified description.
  
  
  
 
