# Anki Docker
This project is made to run the latest versions of the [Anki](https://github.com/ankitects/anki) sync server.
This project contains a Docker image that at start/restart will:
1. Look at the [Anki GitHub repo](https://github.com/ankitects/anki/releases) releases and check if the current server is the latest version.
2. If no, it'll install and run the latest release, and possibly notify a [Ntfy](https://github.com/binwiederhier/ntfy) topic.
3. If yes, it'll run the currently installed version.

The image is made this way so you can create a cronjob that will restart the container daily so it can check for updates and always keep the Anki sync server updated.

# How to run
The image accepts the following environment variables:
- `ANKI_USERNAME`, `ANKI_PASSWORD` (not optional): The Anki sync server user. More about it [here](https://docs.ankiweb.net/sync-server.html#multiple-users).
  - The `ANKI_PASSWORD` should be the hashed password, more about it [here](https://docs.ankiweb.net/sync-server.html#hashed-passwords).
- `NTFY_ADDRESS`, `NTFY_TOPIC`, `NTFY_TOKEN` (optional): Ntfy configs to send notifications to a Ntfy topic when the server is updated or an error occurs.

The image stores important things in the folder `/data` that must be preserved between runs, so you **should** mount it.
- In `/data/config` is the current installed Anki sync server binary version/tag and the binary itself.
- In `/data/anki` is the Anki sync server data, more about it [here](https://docs.ankiweb.net/sync-server.html#storage-location).

The Anki sync server will run on the port `8080`.

This repository also has a `docker-compose.yml` example file.
