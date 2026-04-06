from connect import get_connection
import csv


class PhoneBook:
    def __init__(self):
        pass

    def add_contact(self):
        name = input("Enter name: ").strip()
        phone = input("Enter phone: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL upsert_contact(%s::text, %s::text)", (name, phone))

        conn.commit()
        cur.close()
        conn.close()

        print("Contact added or updated.")

    def import_csv(self):
        file_name = "Practice8/contacts.csv"

        names = []
        phones = []

        with open(file_name, "r", encoding="utf-8") as ff:
            rr = csv.reader(ff)
            next(rr, None)

            for row in rr:
                if len(row) >= 2:
                    nm = row[0].strip()
                    ph = row[1].strip()
                    names.append(nm)
                    phones.append(ph)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_invalid_contacts(%s::text[], %s::text[])",
            (names, phones)
        )
        bad_rows = cur.fetchall()

        if len(bad_rows) > 0:
            print("\nIncorrect data:")
            for one in bad_rows:
                print(one)

        cur.execute(
            "CALL insert_many_contacts(%s::text[], %s::text[])",
            (names, phones)
        )

        conn.commit()
        cur.close()
        conn.close()

        print("CSV import finished.")

    def show_all(self):
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

    def find_by_pattern(self):
        patt = input("Enter pattern: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM search_contacts(%s::text)", (patt,))
        rows = cur.fetchall()

        if len(rows) == 0:
            print("Nothing found.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def show_paginated(self):
        lim = int(input("Enter limit: ").strip())
        offs = int(input("Enter offset: ").strip())

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s::int, %s::int)",
            (lim, offs)
        )
        rows = cur.fetchall()

        if len(rows) == 0:
            print("No contacts.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def remove_contact(self):
        val = input("Enter name or phone to delete: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL delete_contact(%s::text)", (val,))

        conn.commit()
        cur.close()
        conn.close()

        print("Deleted.")

    def menu(self):
        while True:
            print("\nPhoneBook")
            print("1 - Add or update contact")
            print("2 - Import from csv")
            print("3 - Show all contacts")
            print("4 - Search by pattern")
            print("5 - Show paginated contacts")
            print("6 - Delete by name or phone")
            print("0 - Exit")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.import_csv()
            elif choice == "3":
                self.show_all()
            elif choice == "4":
                self.find_by_pattern()
            elif choice == "5":
                self.show_paginated()
            elif choice == "6":
                self.remove_contact()
            elif choice == "0":
                print("Bye")
                break
            else:
                print("Wrong choice")


app = PhoneBook()
app.menu()