# Anki Sync Server

1. Create a folder for anki to store its data. It should be owned by user `65532` (_the user inside the container_). You can use the following command to create the folder and set the permissions (_change the `./data` path to your desired location_):

```bash
mkdir -p ./sync_server_data && sudo chown 65532:65532 ./headless_data
```

3. Use the `docker-compose.yml` file in this repository to run the Anki sync server.

4. Add the Anki [usernames and hashed passwords](https://docs.ankiweb.net/sync-server.html#multiple-users) to the environment variables in the `docker-compose.yml` file or when running the container.

- At least one user is required.
- The `ANKI_PASSWORD` should be the hashed password, more about it [here](https://docs.ankiweb.net/sync-server.html#hashed-passwords).
- Create the environment variables enclosed in single quotes, like this: `SYNC_USER3='username3:hashed_password'`.

# Anki Desktop

# Anki Headless

This image is based on [this repository](https://github.com/ThisIsntTheWay/headless-anki).

1. Create a folder for anki to store its data. It should be owned by user `1000` (_the user inside the container_). You can use the following command to create the folder and set the permissions (_change the `./data` path to your desired location_):

```bash
mkdir -p ./headless_data && sudo chown 1000:1000 ./headless_data
```

2. Populate the `headless_data` folder with Anki necessary files, as they'll not be created automatically. You can use the content in the folder `headless/data` in this repository as a base, or use your own Anki data.

> [!WARNING]
> If you do bring your own profile, make sure you don't have the AnkiConnect plugin installed, as it will conflict with the in `/data/addons21/AnkiConnectDev` that will be installed inside the container every time it restarts!
>
> - The default AnkiConnect plugin folder is `2055492159` inside the `plugins21` folder, so if you have it installed, just delete that folder.

You can also use other QT platform plugins by setting the env var `QT_QPA_PLATFORM` to the desired value. For example, to use the offscreen platform plugin, you can run the container with:

```bash
docker run -e QT_QPA_PLATFORM="offscreen" ...
```

By default, Anki will be launched using `QT_QPA_PLATFORM="vnc"`. This will enable Anki to be accessed using a VNC viewer which might help with debugging, provided port `5900` is forwarded.

> [!INFO]
> You can set the **optional** `ANKICONNECT_API_KEY` environment variable to a custom value to use with the AnkiConnect plugin. If provided, configure your Yomichan, etc. to use this key.
>
> - Take a look at the `docker-compose.yml` file for an example of how to set this variable.
>
> If not provided, AnkiConnect will be unprotected and accessible to anyone who can access the plugin.
