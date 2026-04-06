DROP PROCEDURE IF EXISTS upsert_contact(TEXT, TEXT);
DROP PROCEDURE IF EXISTS insert_many_contacts(TEXT[], TEXT[]);
DROP PROCEDURE IF EXISTS delete_contact(TEXT);

CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO contacts(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    ii INT;
    nm TEXT;
    ph TEXT;
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR ii IN 1..array_length(p_names, 1) LOOP
        nm := trim(p_names[ii]);
        ph := trim(p_phones[ii]);

        IF ph ~ '^\+?[0-9]{10,15}$' THEN
            IF EXISTS (
                SELECT 1
                FROM contacts
                WHERE first_name = nm
            ) THEN
                UPDATE contacts
                SET phone = ph
                WHERE first_name = nm;
            ELSE
                INSERT INTO contacts(first_name, phone)
                VALUES (nm, ph);
            END IF;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$;