# ACE Music for Dify

Source: [AceDataCloud/ACEMusicDify](https://github.com/AceDataCloud/ACEMusicDify). Contact: [dev@acedata.cloud](mailto:dev@acedata.cloud).

Package the plugin and import its local .difypkg under Plugins → Install → Local Package. Set the application API key on the ACE Music provider.

This source release is not listed or verified on Dify Marketplace. Use your workspace's permitted local-plugin installation flow; official distribution is being consolidated with the Ace media tools.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/fetch_icon.py
python3 -m unittest discover
dify plugin package . -o ../acemusic.difypkg
```

Get an [application API key](https://platform.acedata.cloud/console/applications) with ACE Music access. Enter the raw key in the host's credential setting or server environment. Keep keys out of prompts, shared workflows and commits.

Saving credentials performs a read-only task-history check. The plugin sends requests to the fixed HTTPS endpoint at `api.acedata.cloud`; reference MP3 URLs are passed to that API for the requested import.

| Action | Inputs or result |
| --- | --- |
| Create song from idea | Prompt and optional ACE Music model. |
| Create song from lyrics | Lyrics, style and title. |
| Import reference MP3 | Public HTTPS MP3 URL. Save the delivered track ID. |
| Cover a track | One owned track ID, lyrics and style. |
| Blend two tracks | Two distinct compatible owned track IDs, lyrics and style. |
| Generate lyrics | Prompt and optional style. Returns lyrics or a pending task ID. |
| Retrieve task / multiple tasks | Use the original task IDs. |
| List task history | Optional page and items per page. |

Audio creation, reference import and writing lyrics are separately priced. Use the creation tool once, save its `task_id`, then retrieve the same task. If the connection breaks before a task ID arrives, inspect task history before resubmitting. The task state and `response` carry completion and partial failures. A partial result can contain one usable track. Play delivered tracks from `response.data[].audio_url`. Read [ACE Music API documentation](https://github.com/AceDataCloud/ACEMusicAPI) and [current pricing](https://platform.acedata.cloud/services/024e09b4-52cf-5e98-a91a-efedf43104c4).
