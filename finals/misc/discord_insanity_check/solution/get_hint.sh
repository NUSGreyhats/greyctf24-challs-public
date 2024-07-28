curl 'https://discord.com/api/v9/guilds/1246139154241425561/channels' \
  -H 'authorization: <insert_auth_token_here>'  | jq | grep name
