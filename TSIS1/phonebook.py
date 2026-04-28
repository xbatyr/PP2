from connect import get_connection
import csv
import json


# phonebook with postgres
class PhoneBook:
    def __init__(self):
        pass

    def add_extended_contact(self):
        # add one contact with many phones
        name = input("Enter name: ").strip()
        email = input("Enter email: ").strip()
        birthday = input("Enter birthday (YYYY-MM-DD): ").strip()
        group_name = input("Enter group: ").strip()
        main_phone = input("Enter main phone: ").strip()
        main_type = input("Enter main phone type (home/work/mobile): ").strip().lower()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        row = cur.fetchone()

        if row is None:
            # make group if needed
            cur.execute(
                "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                (group_name,)
            )
            group_id = cur.fetchone()[0]
        else:
            group_id = row[0]

        cur.execute(
            """
            INSERT INTO contacts(first_name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                name,
                main_phone,
                email if email else None,
                birthday if birthday else None,
                group_id
            )
        )
        contact_id = cur.fetchone()[0]

        # save main phone here too
        cur.execute(
            """
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, main_phone, main_type)
        )

        while True:
            # add more phones if needed
            phone = input("Enter extra phone (or empty to stop): ").strip()
            if phone == "":
                break

            p_type = input("Enter phone type (home/work/mobile): ").strip().lower()

            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                """,
                (contact_id, phone, p_type)
            )

        conn.commit()
        cur.close()
        conn.close()

        print("Contact added.")

    def add_phone(self):
        # add one more phone
        name = input("Contact name: ").strip()
        phone = input("New phone: ").strip()
        p_type = input("Phone type (home/work/mobile): ").strip().lower()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))

        conn.commit()
        cur.close()
        conn.close()

        print("Phone added.")

    def move_to_group(self):
        # move contact to new group
        name = input("Contact name: ").strip()
        group_name = input("New group: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

        conn.commit()
        cur.close()
        conn.close()

        print("Group changed.")

    def show_all_contacts(self):
        # show main contact data
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.phone,
                c.email,
                c.birthday,
                g.name,
                c.created_at
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            """
        )
        rows = cur.fetchall()

        if len(rows) == 0:
            print("No contacts.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def show_full_contacts(self):
        # show contacts with all phones
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.phone,
                c.email,
                c.birthday,
                g.name,
                p.phone,
                p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id, p.id
            """
        )
        rows = cur.fetchall()

        if len(rows) == 0:
            print("No contacts.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def filter_by_group(self):
        # show contacts from one group
        group_name = input("Enter group: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.phone,
                c.email,
                c.birthday,
                g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            WHERE g.name = %s
            ORDER BY c.id
            """,
            (group_name,)
        )
        rows = cur.fetchall()

        if len(rows) == 0:
            print("Nothing found.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def search_by_email(self):
        # search by email part
        part = input("Enter email pattern: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.phone,
                c.email,
                c.birthday
            FROM contacts c
            WHERE COALESCE(c.email, '') ILIKE %s
            ORDER BY c.id
            """,
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

    def search_all_fields(self):
        # search in all fields
        txt = input("Enter search text: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM search_contacts(%s)", (txt,))
        rows = cur.fetchall()

        if len(rows) == 0:
            print("Nothing found.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def sort_contacts(self):
        # choose sort type
        print("Sort by:")
        print("1 - name")
        print("2 - birthday")
        print("3 - date added")
        choice = input("Choose: ").strip()

        if choice == "1":
            order_by = "c.first_name"
        elif choice == "2":
            order_by = "c.birthday"
        elif choice == "3":
            order_by = "c.created_at"
        else:
            print("Wrong choice.")
            return

        # use safe sort field
        conn = get_connection()
        cur = conn.cursor()

        query = f"""
            SELECT
                c.id,
                c.first_name,
                c.phone,
                c.email,
                c.birthday,
                c.created_at
            FROM contacts c
            ORDER BY {order_by} NULLS LAST, c.id
        """
        cur.execute(query)
        rows = cur.fetchall()

        if len(rows) == 0:
            print("No contacts.")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    def paginated_navigation(self):
        # show contacts by pages
        limit_value = int(input("Enter page size: ").strip())
        offset_value = 0

        while True:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT
                    c.id,
                    c.first_name,
                    c.phone,
                    c.email
                FROM contacts c
                ORDER BY c.id
                LIMIT %s OFFSET %s
                """,
                (limit_value, offset_value)
            )
            rows = cur.fetchall()

            print("\nCurrent page:")
            if len(rows) == 0:
                print("No contacts on this page.")
            else:
                for row in rows:
                    print(row)

            cur.close()
            conn.close()

            cmd = input("\nnext / prev / quit: ").strip().lower()

            # move to next or prev page
            if cmd == "next":
                offset_value += limit_value
            elif cmd == "prev":
                offset_value -= limit_value
                if offset_value < 0:
                    offset_value = 0
            elif cmd == "quit":
                break
            else:
                print("Wrong command.")

    def export_to_json(self):
        # save contacts to json
        file_name = "TSIS1/contacts.json"

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.first_name,
                c.phone,
                c.email,
                c.birthday,
                g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            """
        )
        contacts = cur.fetchall()

        arr = []

        for one in contacts:
            c_id = one[0]

            # load extra phones
            cur.execute(
                """
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
                ORDER BY id
                """,
                (c_id,)
            )
            phs = cur.fetchall()

            phones_list = []
            for ph in phs:
                phones_list.append({
                    "phone": ph[0],
                    "type": ph[1]
                })

            # make one json item
            arr.append({
                "name": one[1],
                "main_phone": one[2],
                "email": one[3],
                "birthday": str(one[4]) if one[4] is not None else None,
                "group": one[5],
                "phones": phones_list
            })

        with open(file_name, "w", encoding="utf-8") as ff:
            json.dump(arr, ff, ensure_ascii=False, indent=4)

        cur.close()
        conn.close()

        print("Exported to JSON.")

    def import_from_json(self):
        # load contacts from json
        file_name = "TSIS1/contacts.json"

        with open(file_name, "r", encoding="utf-8") as ff:
            arr = json.load(ff)

        conn = get_connection()
        cur = conn.cursor()

        for one in arr:
            name = one.get("name")
            email = one.get("email")
            birthday = one.get("birthday")
            group_name = one.get("group")
            phones_list = one.get("phones", [])
            main_phone = one.get("main_phone")

            if (main_phone is None or main_phone == "") and len(phones_list) > 0:
                main_phone = phones_list[0].get("phone")

            # check old contact
            cur.execute(
                "SELECT id FROM contacts WHERE first_name = %s ORDER BY id LIMIT 1",
                (name,)
            )
            old_row = cur.fetchone()

            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            g_row = cur.fetchone()

            if g_row is None:
                # make group if missing
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]
            else:
                group_id = g_row[0]

            if old_row is not None:
                print(f"Duplicate found for {name}")
                ans = input("skip or overwrite? ").strip().lower()

                if ans == "skip":
                    continue
                elif ans == "overwrite":
                    # replace old contact data
                    contact_id = old_row[0]

                    cur.execute(
                        """
                        UPDATE contacts
                        SET phone = %s,
                            email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE id = %s
                        """,
                        (main_phone, email, birthday, group_id, contact_id)
                    )

                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

                    for ph in phones_list:
                        cur.execute(
                            """
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            """,
                            (contact_id, ph.get("phone"), ph.get("type"))
                        )
                else:
                    print("Skipped.")
                    continue
            else:
                # add new contact
                cur.execute(
                    """
                    INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (name, main_phone, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]

                for ph in phones_list:
                    cur.execute(
                        """
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s, %s, %s)
                        """,
                        (contact_id, ph.get("phone"), ph.get("type"))
                    )

        conn.commit()
        cur.close()
        conn.close()

        print("Imported from JSON.")

    def import_csv_extended(self):
        # load contacts from csv
        file_name = "TSIS1/contacts.csv"

        conn = get_connection()
        cur = conn.cursor()

        with open(file_name, "r", encoding="utf-8") as ff:
            rr = csv.DictReader(ff)

            for row in rr:
                # read one csv row
                name = row["name"].strip()
                email = row["email"].strip()
                birthday = row["birthday"].strip()
                group_name = row["group"].strip()
                phone = row["phone"].strip()
                p_type = row["phone_type"].strip().lower()

                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                g_row = cur.fetchone()

                if g_row is None:
                    # make group if needed
                    cur.execute(
                        "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                        (group_name,)
                    )
                    group_id = cur.fetchone()[0]
                else:
                    group_id = g_row[0]

                cur.execute(
                    "SELECT id FROM contacts WHERE first_name = %s ORDER BY id LIMIT 1",
                    (name,)
                )
                c_row = cur.fetchone()

                if c_row is None:
                    # make contact if needed
                    cur.execute(
                        """
                        INSERT INTO contacts(first_name, phone, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            name,
                            phone,
                            email if email else None,
                            birthday if birthday else None,
                            group_id
                        )
                    )
                    contact_id = cur.fetchone()[0]
                else:
                    contact_id = c_row[0]

                # save csv phone
                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    """,
                    (contact_id, phone, p_type)
                )

        conn.commit()
        cur.close()
        conn.close()

        print("CSV imported.")

    def menu(self):
        # main menu
        while True:
            print("\nTSIS 1 PhoneBook")
            print("1 - Add extended contact")
            print("2 - Add phone")
            print("3 - Move contact to group")
            print("4 - Show all contacts")
            print("5 - Show full contacts with phones")
            print("6 - Filter by group")
            print("7 - Search by email")
            print("8 - Search all fields")
            print("9 - Sort contacts")
            print("10 - Paginated navigation")
            print("11 - Export to JSON")
            print("12 - Import from JSON")
            print("13 - Import extended CSV")
            print("0 - Exit")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.add_extended_contact()
            elif choice == "2":
                self.add_phone()
            elif choice == "3":
                self.move_to_group()
            elif choice == "4":
                self.show_all_contacts()
            elif choice == "5":
                self.show_full_contacts()
            elif choice == "6":
                self.filter_by_group()
            elif choice == "7":
                self.search_by_email()
            elif choice == "8":
                self.search_all_fields()
            elif choice == "9":
                self.sort_contacts()
            elif choice == "10":
                self.paginated_navigation()
            elif choice == "11":
                self.export_to_json()
            elif choice == "12":
                self.import_from_json()
            elif choice == "13":
                self.import_csv_extended()
            elif choice == "0":
                print("Bye")
                break
            else:
                print("Wrong choice")


# start the app
app = PhoneBook()
app.menu()
