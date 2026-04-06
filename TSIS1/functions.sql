DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INT,
    contact_name VARCHAR,
    contact_email VARCHAR,
    contact_birthday DATE,
    group_name VARCHAR,
    phone_value VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g
        ON c.group_id = g.id
    LEFT JOIN phones p
        ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
       OR COALESCE(p.phone, '') ILIKE '%' || p_query || '%'
       OR COALESCE(g.name, '') ILIKE '%' || p_query || '%'
    ORDER BY c.id, p.id;
END;
$$;