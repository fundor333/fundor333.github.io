---
title: "Hacking My Kobo with KOReader"
date: 2026-04-09T12:10:12+02:00
draft: true
feature_link: "https://www.midjourney.com/home/"
feature_text: "by IA Midjourney"
description: "A little diary about my expirience "
tags:
- kobo
- koreader
- ebook
- ereader

categories:
- tinkering
- Hacking stuffs
---

A long long time ago I start using a EBook Reader, the first Kindle PaperWhite (2012) and I never stop using EReader.

The last one I own is a Kobo Clara Colour, this one.

![Kobo Clara Colour](kobo.jpg)

[Install Tread part1](https://www.mobileread.com/forums/showpost.php?p=3797095&postcount=1)

[Install Tread part2](https://www.mobileread.com/forums/showpost.php?p=3797096&postcount=2)

[KOReader](https://github.com/koreader/koreader)

[Customisable Sleep Screen](https://github.com/pxlflux/customisablesleepscreen.koplugin)

[Hardcover.app for KOReader](https://github.com/Billiam/hardcoverapp.koplugin)

[ProjectTitle KOReader](https://github.com/joshuacant/ProjectTitle)


~~~ python
#!/usr/bin/env python3

import os
import sys
import shutil
from datetime import datetime

KOREADER_DIR = ".adds"
BACKUP_DESTINATION = "~/BackUp/KoReader"
BACKUP_FILENAME = "koreader_backup_{date}.zip"


def find_kobo_device():
    """Find the path to the Kobo"""
    volumes_path = "/Volumes"

    if os.path.exists(volumes_path):
        for entry in os.listdir(volumes_path):
            full_path = os.path.join(volumes_path, entry)
            if os.path.isdir(full_path):
                try:
                    contents = os.listdir(full_path)
                    if ".kobo" in contents:
                        return full_path
                except PermissionError:
                    continue

    return None


def get_koreader_path(kobo_path):
    """Returns the path to KoReader on the Kobo."""
    return os.path.join(kobo_path, KOREADER_DIR)


def create_backup(source_path, backup_destination):
    """Creates a zip backup of KoReader."""
    if not os.path.exists(source_path):
        print(f"Error: KoReader not found in {source_path}")
        return False

    print(f"Creating backup from: {source_path}")

    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = BACKUP_FILENAME.format(date=date_str)
    backup_path = os.path.join(backup_destination, backup_filename)

    print(f"Backup to: {backup_path}")

    try:
        shutil.make_archive(
            backup_path.replace(".zip", ""), "zip", root_dir=source_path, base_dir="."
        )
        print(f"Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"Error during backup creation: {e}")
        return False


def main():
    kobo_path = find_kobo_device()

    if not kobo_path:
        print("Kobo not found. Connect the device and try again.")
        sys.exit(1)

    print(f"Kobo found at: {kobo_path}")

    koreader_path = get_koreader_path(kobo_path)
    backup_destination = os.path.expanduser(BACKUP_DESTINATION)
    os.makedirs(backup_destination, exist_ok=True)

    success = create_backup(koreader_path, backup_destination)

    if success:
        print("Backup completed successfully!")
    else:
        print("Backup failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

~~~
