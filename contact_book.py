"""A small JSON-backed command-line contact book."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).with_name("contacts.json")


def load_contacts() -> list[dict[str, str]]:
    """Load contacts from disk, treating a missing file as an empty book."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data: Any = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read {DATA_FILE.name}: {error}")
        return []

    if not isinstance(data, list):
        print(f"{DATA_FILE.name} does not contain a contact list.")
        return []

    contacts: list[dict[str, str]] = []
    for item in data:
        if isinstance(item, dict):
            contact = {
                key: str(item[key]).strip()
                for key in ("name", "phone", "email")
                if key in item
            }
            if contact.get("name"):
                contacts.append(contact)
    return contacts


def save_contacts(contacts: list[dict[str, str]]) -> bool:
    """Save contacts atomically so an interrupted write does not lose the file."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            prefix=f".{DATA_FILE.stem}-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            json.dump(contacts, temporary_file, indent=2)
            temporary_file.write("\n")
            temporary_name = temporary_file.name
        os.replace(temporary_name, DATA_FILE)
        return True
    except OSError as error:
        print(f"Could not save {DATA_FILE.name}: {error}")
        return False


def prompt_required(label: str) -> str:
    """Prompt until the user enters a non-empty value."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label} is required.")


def display_contacts(contacts: list[dict[str, str]]) -> None:
    if not contacts:
        print("\nNo contacts found.")
        return

    print(f"\nContacts ({len(contacts)}):")
    print("-" * 60)
    for index, contact in enumerate(contacts, start=1):
        print(f"{index}. {contact['name']}")
        print(f"   Phone: {contact.get('phone') or '—'}")
        print(f"   Email: {contact.get('email') or '—'}")
    print("-" * 60)


def add_contact(contacts: list[dict[str, str]]) -> None:
    print("\nAdd contact")
    name = prompt_required("Name")
    if any(contact["name"].casefold() == name.casefold() for contact in contacts):
        print("A contact with that name already exists.")
        return

    phone = input("Phone (optional): ").strip()
    email = input("Email (optional): ").strip()
    contacts.append({"name": name, "phone": phone, "email": email})

    if save_contacts(contacts):
        print(f"Added {name}.")


def search_contacts(contacts: list[dict[str, str]]) -> None:
    print("\nSearch contacts")
    query = prompt_required("Search")
    query = query.casefold()
    matches = [
        contact
        for contact in contacts
        if any(query in contact.get(field, "").casefold() for field in ("name", "phone", "email"))
    ]
    display_contacts(matches)


def delete_contact(contacts: list[dict[str, str]]) -> None:
    print("\nDelete contact")
    if not contacts:
        print("No contacts to delete.")
        return

    query = prompt_required("Name")
    matches = [
        (index, contact)
        for index, contact in enumerate(contacts)
        if query.casefold() in contact["name"].casefold()
    ]

    if not matches:
        print("No matching contacts found.")
        return

    if len(matches) == 1:
        index, contact = matches[0]
    else:
        print("\nMatching contacts:")
        for option, (_, contact) in enumerate(matches, start=1):
            print(f"{option}. {contact['name']}")
        choice = input("Choose a contact number (or press Enter to cancel): ").strip()
        if not choice:
            print("Delete cancelled.")
            return
        try:
            selected = int(choice) - 1
            index, contact = matches[selected]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

    confirmation = input(f"Delete {contact['name']}? [y/N]: ").strip().casefold()
    if confirmation != "y":
        print("Delete cancelled.")
        return

    contacts.pop(index)
    if save_contacts(contacts):
        print(f"Deleted {contact['name']}.")


def show_menu() -> None:
    print("\nContact Book")
    print("============")
    print("1. Add contact")
    print("2. Search contacts")
    print("3. Delete contact")
    print("4. List contacts")
    print("5. Exit")


def main() -> None:
    contacts = load_contacts()
    print("Welcome to Contact Book.")

    while True:
        show_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contacts(contacts)
        elif choice == "3":
            delete_contact(contacts)
        elif choice == "4":
            display_contacts(contacts)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Please choose an option from 1 to 5.")


if __name__ == "__main__":
    main()