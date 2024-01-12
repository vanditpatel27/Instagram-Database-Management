import cx_Oracle
connection = cx_Oracle.connect("system", "tiger", "localhost:1521/XEPDB1")

# Create a cursor
cursor = connection.cursor()

# Define the SQL statements for creating triggers

like_trigger_sql = """
CREATE OR REPLACE TRIGGER like_post_trigger
BEFORE INSERT ON "Like" FOR EACH ROW
BEGIN
    UPDATE Post
    SET NoOfLikes = NoOfLikes + 1
    WHERE PostID = :new.PostID;
END;
/
"""

comment_trigger_sql = """
CREATE OR REPLACE TRIGGER comment_post_trigger
AFTER INSERT ON "Comment" FOR EACH ROW
BEGIN
    UPDATE Post
    SET NoOfComments = NoOfComments + 1
    WHERE PostID = :new.PostID;
END;
/
"""
share_trigger_sql = """
CREATE OR REPLACE TRIGGER share_post_trigger
AFTER INSERT ON "Share" FOR EACH ROW
BEGIN
    DECLARE
        shared_users_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO shared_users_count
        FROM SharedWith
        WHERE ShareID = :new.ShareID;

        UPDATE Post
        SET NoOfShares = NoOfShares + shared_users_count
        WHERE PostID = :new.PostID;
    END;
END;
/
"""
trigger_like_deleted = """
CREATE OR REPLACE TRIGGER update_like_count
AFTER DELETE ON "Like"
FOR EACH ROW
BEGIN
    UPDATE Post
    SET NoOfLikes = NoOfLikes - 1
    WHERE PostID = :old.PostID;
END;
/
"""

# Define a trigger for updating comment count when a comment is deleted
trigger_comment_deleted = """
CREATE OR REPLACE TRIGGER update_comment_count
AFTER DELETE ON "Comment"
FOR EACH ROW
BEGIN
    UPDATE Post
    SET NoOfComments = NoOfComments - 1
    WHERE PostID = :old.PostID;
END;
/
"""

# Execute the trigger creation
cursor.execute(trigger_like_deleted)
cursor.execute(trigger_comment_deleted)

# Execute the trigger creation
cursor.execute(share_trigger_sql)
# Execute the SQL statements to create triggers
cursor.execute(like_trigger_sql)
cursor.execute(comment_trigger_sql)
# Commit the changes to the database
connection.commit()

# Close the cursor and the connection
cursor.close()
connection.close()

print("Triggers created successfully.")
