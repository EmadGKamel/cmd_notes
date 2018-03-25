#!/usr/bin/env python3
from collections import OrderedDict
import sys
import os
from time import sleep
import datetime

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """adding new entery"""
    print("Enter your entry. Press ctrl+d when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('\nSave entry [Y/n]? ').lower().strip() != 'n':
            Entry.create(content=data)
            print("Saved successfully!")
            sleep(1)


def view_enteries(query=None):
    """viewing the entreies"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if query:
        entries = entries.where(Entry.content.contains(query))

    for entry in entries:
        timestamp = entry.timestamp.strftime("%a %b %d %Y, %H:%M")
        clear()
        print('\n' + timestamp)
        print('=' * len(timestamp))
        print(entry.content + "\n" + '=' * len(timestamp))
        print("n) next d) delete or q) return")
        next_action = input('Action [n/d/q]: ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search for a query"""
    view_enteries(input("Search query: "))


def delete_entry(entery):
    """delete an entery"""
    if input("Are you sure [y/n]? ").lower() == 'y':
        entery.delete_instance()
        print("Deleted successfully!")
        sleep(1)


menu = OrderedDict([
        ('a', add_entry),
        ('v', view_enteries),
        ('s', search_entries),
    ])


if __name__ == '__main__' :
    db.connect()
    db.create_tables([Entry], safe=True)
    menu_loop()
