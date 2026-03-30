from connect import get_connection
import csv
import os

def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added.")

def import_csv():
    file_name = "Practice7/contacts.csv"

    conn = get_connection()
    cur = conn.cursor()

    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if len(row) >= 2:
                name = row[0].strip()
                phone = row[1].strip()

                cur.execute(
                    "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
                    (name, phone)
                )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported.")

def show_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id")
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No contacts.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def find_by_name():
    part = input("Enter name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE first_name ILIKE %s ORDER BY id",
        ("%" + part + "%",)
    )

    rows = cur.fetchall()

    if len(rows) == 0:
        print("Nothing found.")
    else:
        for row in rows:
            print(row)
    cur.close()
    conn.close()

def find_by_prefix():
    prefix = input("Enter phone prefix: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s ORDER BY id",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    if len(rows) == 0:
        print("Nothing found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def change_name():
    old_name = input("Old name: ").strip()
    new_name = input("New name: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET first_name = %s WHERE first_name = %s",
        (new_name, old_name)
    )
    conn.commit()
    print("Updated:", cur.rowcount)
    cur.close()
    conn.close()

def change_phone():
    name = input("Contact name: ").strip()
    new_phone = input("New phone: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET phone = %s WHERE first_name = %s",
        (new_phone, name)
    )
    conn.commit()
    print("Updated:", cur.rowcount)
    cur.close()
    conn.close()

def remove_by_name():
    name = input("Name to delete: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM contacts WHERE first_name = %s",
        (name,)
    )
    conn.commit()
    print("Deleted:", cur.rowcount)
    cur.close()
    conn.close()

def remove_by_phone():
    phone = input("Phone to delete: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE phone = %s",
        (phone,)
    )

    conn.commit()
    print("Deleted:", cur.rowcount)
    cur.close()
    conn.close()

def menu():
    while True:
        print("\nPhoneBook")
        print("1 - Add contact")
        print("2 - Import from csv")
        print("3 - Show all contacts")
        print("4 - Search by name")
        print("5 - Search by phone prefix")
        print("6 - Update name")
        print("7 - Update phone")
        print("8 - Delete by name")
        print("9 - Delete by phone")
        print("0 - Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_contact()
        elif choice == "2":
            import_csv()
        elif choice == "3":
            show_all()
        elif choice == "4":
            find_by_name()
        elif choice == "5":
            find_by_prefix()
        elif choice == "6":
            change_name()
        elif choice == "7":
            change_phone()
        elif choice == "8":
            remove_by_name()
        elif choice == "9":
            remove_by_phone()
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Wrong choice")

menu()