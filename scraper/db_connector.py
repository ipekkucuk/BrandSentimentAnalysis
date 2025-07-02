DROP_TABLE_QUERY = """DROP TABLE IF EXISTS Reviews"""

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name TEXT NOT NULL,
    category_name TEXT NOT NULL,
    parent_company TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    comment_date TEXT NOT NULL,
    comment_rating INTEGER NOT NULL
)
"""

INSERT_COMMENT_QUERY = "INSERT INTO Reviews (brand_name,category_name,parent_company, comment_text, comment_date, comment_rating) VALUES (? ,?, ?, ?, ?, ?)"
