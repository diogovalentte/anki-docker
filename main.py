import logging
import os

import requests
from pytfy import NtfyPublisher

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)-8s :: %(name)s :: %(message)s",
)
logger = logging.getLogger()

# Need to be absolute paths
CONFIG_FOLDER = os.getenv("CONFIG_FOLDER", "/data/config/")
ANKI_STORAGE_FOLDER = os.getenv("ANKI_STORAGE_FOLDER", "/data/anki/")


def create_default_folders():
    os.makedirs(CONFIG_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(CONFIG_FOLDER, "sync_server/"), exist_ok=True)
    os.makedirs(ANKI_STORAGE_FOLDER, exist_ok=True)


def get_github_tags():
    github_token = os.getenv("GITHUB_TOKEN", "")
    headers = {}
    if github_token:
        headers = {"Authorization": f"Bearer {github_token}"}
    url = "https://api.github.com/repos/ankitects/anki/tags"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tags = response.json()
    return [tag["name"] for tag in tags]


def get_last_valid_tag(tags):
    last_tag = None
    for tag in tags:
        parts = tag.split(".")
        try:
            for part in parts:
                int(part)
            last_tag = tag
            break
        except Exception:
            continue

    if last_tag is None:
        raise Exception("Could not find the last GitHub repository tag")

    return last_tag


def is_tag_greater_than(tag_1, tag_2) -> bool:
    """Checks if tag_1 is greater than tag_2. Tags should be like 1.25.3"""
    tag_1_parts = tag_1.split(".")
    tag_2_parts = tag_2.split(".")

    tag_1_len = len(tag_1_parts)
    tag_2_len = len(tag_2_parts)
    biggest_len = max(tag_1_len, tag_2_len)
    for i in range(biggest_len):
        try:
            tag_1_part = int(tag_1_parts[i])
        except IndexError:
            return False
        try:
            tag_2_part = int(tag_2_parts[i])
        except IndexError:
            return True

        if tag_1_part > tag_2_part:
            return True
        elif tag_1_part == tag_2_part:
            continue
        else:
            return False

    return False


def get_current_tag():
    tag = ""
    file_path = os.path.join(CONFIG_FOLDER, "current_tag.txt")
    try:
        with open(file_path, "r") as file:
            tag = file.read().strip()
    except FileNotFoundError:
        open(file_path, "w").close()

    if not tag:
        tag = "0"

    return tag


def save_tag(version):
    file_path = os.path.join(CONFIG_FOLDER, "current_tag.txt")
    with open(file_path, "w") as file:
        file.write(version)


def update_rust():
    try:
        status_code = os.system("rustup update stable")
    except Exception as e:
        logger.error(f"Error while updating rust: {e}")
        raise e
    else:
        if status_code != 0:
            raise Exception("Error while updating rust")


def install_anki_server_bin(tag):
    bin_root_folder = os.path.join(CONFIG_FOLDER, "sync_server")
    script_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "install_anki_sync_server.sh"
    )
    status_code = os.system(f"{script_path} {tag} {bin_root_folder}")
    if status_code != 0:
        raise Exception("Error while installing anki-sync-server")


def start_anki_server():
    username = os.getenv("ANKI_USERNAME")
    password = os.getenv("ANKI_PASSWORD")
    if not username or not password:
        raise Exception("Anki username and/or password environment variables not set")

    anki_storage_folder_path = ANKI_STORAGE_FOLDER

    bin_path = os.path.join(CONFIG_FOLDER, "sync_server/bin/anki-sync-server")
    command = f"PASSWORDS_HASHED=1 SYNC_BASE={anki_storage_folder_path} SYNC_USER1='{username}:{password}' {bin_path}"
    status_code = os.system(command)
    if status_code != 0:
        raise Exception("Error while starting/executing the anki-sync-server")
    else:
        logger.info("Anki sync server started and ended successfully")


def main():
    logger.info("Starting the anki sync server install/update/initialization process")

    create_default_folders()
    tags = get_github_tags()
    last_tag = get_last_valid_tag(tags)
    current_tag = get_current_tag()
    if is_tag_greater_than(last_tag, current_tag):
        logger.info(f"New version found: {last_tag}")
        logger.info("Updating rust...")
        update_rust()
        logger.info("Installing anki-sync-server...")
        install_anki_server_bin(last_tag)
        logger.info("Saving the new tag info...")
        save_tag(last_tag)
        logger.info("Installation completed")
        if ntfy:
            ntfy.post(
                title="Anki Sync Server Updated!",
                message=f"New version: {last_tag}\nOld version: {current_tag}\nMore about it here: https://github.com/ankitects/anki/releases",
                click="https://github.com/ankitects/anki/releases",
            )

    logger.info(f"Starting anki-sync-server with tag {last_tag}...")
    start_anki_server()


if __name__ == "__main__":
    ntfy_address = os.getenv("NTFY_ADDRESS", "")
    ntfy_topic = os.getenv("NTFY_TOPIC", "")
    ntfy_token = os.getenv("NTFY_TOKEN", "")

    ntfy = None
    if ntfy_address and ntfy_topic and ntfy_token:
        ntfy = NtfyPublisher(ntfy_address, ntfy_topic, ntfy_token)

    main()
