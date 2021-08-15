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
  All commands are preceded by a `!`. In the following commands, if set prefix is different, replace `!` by that prefix.
  - `!help` to view help regarding the commands
  
  - `!join` to join the userbase. This is required the first time you use the bot. 
  
  - `!set <playlist name>` to set current playlist to `<playlist name>`. You will be prompted to add <playlist name> if it doesn't exist.
  
  - `!show` displays the set playlist.
  
  - `!add <song name>` to add a song to the set playlist.  
  
  - `!list` to list your playlists
  
  - `!list @<username>` to list <username>'s playlists. 
  
  - `!list<number>` to list playlists on page number <number>.
  
  - `!list all` to list ALL the playlists in the userbase, haha, just don't use this :slight_smile:
  
  - `!rename <new_name>` to rename the set playlist to <new_name>
  
  - `!describe` to add a description to the set playlist to the specified description.
  
  - `!lock` to lock the set playlist, so nobody except you can modify the playlist
  
  - `!unlock` to unlock the set playlist, so anyone who knows the playlist name can modify it.
  
  - `!private` to hide the set playlist, only you can view it in the `!list @<your_username>` command
  
  - `!public` to make the set playlist visible to everyone on `!list @<your_username>`

