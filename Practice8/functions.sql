DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);
DROP FUNCTION IF EXISTS get_invalid_contacts(TEXT[], TEXT[]);

CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE (
    contact_id INT,
    contact_name VARCHAR,
    contact_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (
    contact_id INT,
    contact_name VARCHAR,
    contact_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;


CREATE OR REPLACE FUNCTION get_invalid_contacts(p_names TEXT[], p_phones TEXT[])
RETURNS TABLE (
    bad_name TEXT,
    bad_phone TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    ii INT;
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR ii IN 1..array_length(p_names, 1) LOOP
        IF trim(p_phones[ii]) !~ '^\+?[0-9]{10,15}$' THEN
            bad_name := trim(p_names[ii]);
            bad_phone := trim(p_phones[ii]);
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$;