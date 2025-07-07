# Anki Docker

1. Create a folder for the anki to store its data. It should be owned by user `65532` (_the user inside the container_). You can use the following command to create the folder and set the permissions (_change the `./data` path to your desired location_):

```bash
mkdir -p ./data && sudo chown 65532:65532 ./data
```

3. Use the `docker-compose.yml` file in this repository to run the Anki sync server.

4. Add the Anki [usernames and hashed passwords](https://docs.ankiweb.net/sync-server.html#multiple-users) to the environment variables in the `docker-compose.yml` file or when running the container.

- At least one user is required.
- The `ANKI_PASSWORD` should be the hashed password, more about it [here](https://docs.ankiweb.net/sync-server.html#hashed-passwords).
- Create the environment variables enclosed in single quotes, like this: `SYNC_USER3='username3:hashed_password'`.
