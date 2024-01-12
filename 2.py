import datetime
import cx_Oracle
from prettytable import PrettyTable
connection = cx_Oracle.connect("system", "tiger", "localhost:1521/XEPDB1")
today = datetime.date.today()
cursor = connection.cursor()
def user_registration():    
    cursor.execute("SELECT UserID FROM  UserRegistration")
    uservalue=[row[0] for row in cursor.fetchall()]
    user_id = input("Enter User ID: ") 
    if not user_id.isdigit():
        print("User ID must be an integer.")
        return False
    if int(user_id) in uservalue:
        print ("User_id already exists")
        return False
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    try:
        dob_datetime = datetime.datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        print("Date of Birth should be in the format YYYY-MM-DD.")
        return False
    if(today.year<dob_datetime.year and today.month<dob_datetime.month and today.day<dob_datetime.day):
        print("enter appropriate dateofbirth")
        return False
    age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
    password = input("Enter Password:(must be greater than or equal to 8 characters) ")
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    email = input("Enter Valid Email: ")
    if "@" not in email:
        print("Email must contain the @ symbol.")
        return False
    phone_no = input("Enter valid Phone Number: ")
    if not phone_no.isdigit() or len(phone_no) != 10:
        print("Phone Number must be a 10-digit integer.")
        return False
    date_of_registration = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
    INSERT INTO UserRegistration
    (UserID, FirstName, LastName, DOB, Age, Password, Email, PhoneNo, DateOfRegistration)
    VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8, TO_DATE(:9, 'YYYY-MM-DD'))
    """,(user_id, first_name, last_name, dob, age, password, email, phone_no, date_of_registration))
    uservalue.append(user_id)
    connection.commit()
    print("User registered successfully!")
def follow_user():
    cursor.execute("SELECT UserID FROM  UserRegistration")
    uservalue=[row[0] for row in cursor.fetchall()]
    follower_id = int(input("Enter Follower's User ID: "))
    if follower_id not in uservalue:
        print("User does not exist!")
        return False
    following_id = int(input("Enter Following User ID: "))
    if following_id not in uservalue:
        print("User does not exist!")
        return False
    cursor.execute("INSERT INTO Followers (FollowerID, FollowingID) VALUES (:1, :2)", (follower_id, following_id))
    connection.commit()
    print(f"{follower_id} started following {following_id}")
def post():
    cursor.execute("SELECT UserID FROM  UserRegistration")
    uservalue = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT PostID FROM  Post")
    postvalue = [row[0] for row in cursor.fetchall()]
    post_id = int(input("Enter Post ID: "))
    no_of_likes = 0
    no_of_comments = 0
    no_of_shares = 0
    if post_id in postvalue:
        print("PostId already exists!")
        return False 
    user_id = int(input("Enter User ID: "))
    if user_id not in uservalue:
        print("UserID does not exist!")
        return False
    description = input("Enter Description: ")
    video = input("Enter Video  ")
    image = input("Enter Image")
    tagged_user_ids = int(input("Enter the number of tagged users: "))
    taggedwith = []
    flag = 0
    for i in range(tagged_user_ids):
        tagged_user_id = int(input(f"Enter user id for tagged user {i + 1}: "))
        if tagged_user_id not in uservalue:
            flag = 1
            print("UserID does not exist!")
            break
        taggedwith.append(tagged_user_id)
    if flag == 1:
        return False
    try:
        date_of_post = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO Post (PostID, UserID, Description, Video, Image, NoOfLikes, DateOfPost, NoOfComments, NoOfShares)
        VALUES (:1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'), :8, :9)
    """, (post_id, user_id, description, video, image, no_of_likes, date_of_post, no_of_comments, no_of_shares))
        connection.commit()
        for tagged_user_id in taggedwith:
            cursor.execute("INSERT INTO TaggedUser (PostID, TaggedUserID) VALUES (:post_id, :tagged_user_id)",
                           (post_id, tagged_user_id))
        connection.commit()
        print("Post posted successfully!")
    except cx_Oracle.Error as error:
        print("Error:", error)
def like_post():
    cursor.execute("SELECT UserID FROM UserRegistration")
    uservalue = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT PostID FROM Post")
    postvalue = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT LikeID FROM "Like"')
    likevalue = [row[0] for row in cursor.fetchall()]
    like_id = int(input("Enter Like ID: "))
    if like_id in likevalue:
        print("Like ID already exists!")
        return False
    post_id = int(input("Enter Post ID: "))
    if post_id not in postvalue:
        print("Post ID doesn't exist!")
        return False
    user_id = int(input("Enter User ID: "))
    if user_id not in uservalue:
        print("User ID doesn't exist!")
        return False
    cursor.execute("""
    SELECT 1 FROM "Like"
    WHERE PostID = :post_id AND UserID = :user_id
""", {"post_id": post_id, "user_id": user_id})
    existing_row = cursor.fetchone()
    if existing_row:
        print("User already liked the post")
        return False
    date_of_like = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        cursor.execute("""
            INSERT INTO "Like" (LikeID, PostID, UserID, DateOfLike)
            VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
        """, (like_id, post_id, user_id, date_of_like))
        cursor.execute("""
            UPDATE Post
            SET NoOfLikes = NoOfLikes + 1
            WHERE PostID = :1
            """, (post_id,))
        connection.commit()
        print("Post liked successfully!")
    except cx_Oracle.Error as error:
        print("Error:", error)
def comment_post():
    cursor.execute("SELECT UserID FROM UserRegistration")
    uservalue = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT PostID FROM Post")
    postvalue = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT CommentID FROM "Comment"')
    commentvalue = [row[0] for row in cursor.fetchall()]
    comment_id = int(input("Enter Comment ID: "))
    if comment_id  in commentvalue:
        print("Comment  ID already exist!")
        return False
    date_of_comment = datetime.datetime.now().strftime("%Y-%m-%d")
    post_id = int(input("Enter Post ID: "))
    if post_id not in postvalue:
        print("Post ID doesn't exist!")
        return False
    user_id = int(input("Enter User ID: "))
    if user_id not in uservalue:
        print("User ID doesn't exist!")
        return False
    description = input("Enter Comment: ")
    cursor.execute("""
        INSERT INTO "Comment" (CommentID, DateOfComment, PostID, UserID, Description)
        VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5)
    """, (comment_id, date_of_comment, post_id, user_id, description))
    cursor.execute("""
            UPDATE Post
            SET NoOfComments = NoOfComments + 1
            WHERE PostID = :1
            """, (post_id,))
    connection.commit()
    print("Comment added successfully!")
def share_post():
    cursor.execute("SELECT UserID FROM UserRegistration")
    uservalue = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT PostID FROM Post")
    postvalue = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT ShareID FROM "Share"')
    sharevalue = [row[0] for row in cursor.fetchall()]
    share_id = int(input("Enter Share ID: "))
    if share_id  in sharevalue:
        print("ShareID already exist!")
        return False
    date_of_share = datetime.datetime.now().strftime("%Y-%m-%d")
    post_id = int(input("Enter Post ID: "))
    if post_id not in postvalue:
        print("Post ID doesn't exist!")
        return False
    user_id = int(input("Enter User ID: "))
    if user_id not in uservalue:
        print("User ID doesn't exist!")
        return False
    shared_user_ids = int(input("Enter the number of shared users: "))
    sharewith = []
    flag = 0
    for i in range(shared_user_ids):
        shared_user_id = int(input(f"Enter user id for tagged user {i + 1}: "))
        if shared_user_id not in uservalue:
            flag = 1
            print("UserID does not exist!")
            break
        sharewith.append(shared_user_id)
    if flag == 1:
        return False
    cursor.execute("""
        INSERT INTO "Share" (ShareID, DateOfShare, PostID, UserID)
        VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4)
    """, (share_id, date_of_share, post_id, user_id))
    connection.commit()
    for share_user_id in sharewith:
            cursor.execute("INSERT INTO SharedWith (ShareID, SharedUserID) VALUES (:post_id, :share_user_id)",
                           (post_id, share_user_id))
    cursor.execute("""
           UPDATE Post
        SET NoOfShares = NoOfShares + :1
        WHERE PostID = :2
    """, (shared_user_ids, post_id))        
    connection.commit()
    print("Post shared successfully!")
def update_user_info():
    user_id = int(input("Enter User ID: "))
    cursor.execute("SELECT UserID FROM UserRegistration")
    uservalue = [row[0] for row in cursor.fetchall()]
    if user_id not in uservalue:
        print("User does not exist!")
        return False
    print("Select attribute to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Date of Birth")
    print("4. Password")
    print("5. Email")
    print("6. Phone Number")
    choice = input("Enter your choice: ")
    if choice == "1":
        new_first_name = input("Enter new First Name: ")
        cursor.execute("UPDATE UserRegistration SET FirstName = :1 WHERE UserID = :2", (new_first_name, user_id))
    elif choice == "2":
        new_last_name = input("Enter new Last Name: ")
        cursor.execute("UPDATE UserRegistration SET LastName = :1 WHERE UserID = :2", (new_last_name, user_id))
    elif choice == "3":
        new_dob = input("Enter new Date of Birth (YYYY-MM-DD): ")
        try:
            dob_datetime = datetime.datetime.strptime(new_dob, "%Y-%m-%d")
        except ValueError:
            print("Date of Birth should be in the format YYYY-MM-DD.")
            return False
        new_age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
        cursor.execute("UPDATE UserRegistration SET DOB = TO_DATE(:1, 'YYYY-MM-DD'), Age = :2 WHERE UserID = :3",
                       (new_dob, new_age, user_id))
    elif choice == "4":
        new_password = input("Enter new Password (must be greater than or equal to 8 characters): ")
        if len(new_password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        cursor.execute("UPDATE UserRegistration SET Password = :1 WHERE UserID = :2", (new_password, user_id))
    elif choice == "5":
        new_email = input("Enter new Email: ")
        if "@" not in new_email:
            print("Email must contain the @ symbol.")
            return False
        cursor.execute("UPDATE UserRegistration SET Email = :1 WHERE UserID = :2", (new_email, user_id))
    elif choice == "6":
        new_phone_no = input("Enter new Phone Number: ")
        if not new_phone_no.isdigit() or len(new_phone_no) != 10:
            print("Phone Number must be a 10-digit integer.")
            return False
        cursor.execute("UPDATE UserRegistration SET PhoneNo = :1 WHERE UserID = :2", (new_phone_no, user_id))
    else:
        print("Invalid choice. Please try again.")
        return False
    connection.commit()
    print("User information updated successfully!")
def delete_user_account():
    user_id = input("Enter User ID to delete: ")
    if not user_id.isdigit():
        print("User ID must be an integer.")
        return False
    cursor.execute("SELECT * FROM UserRegistration WHERE UserID = :1", (user_id,))
    user_info = cursor.fetchone()
    cursor.execute("SELECT PostID FROM Post where USERID = :1", (user_id,))
    postvalue = [row[0] for row in cursor.fetchall()]
    print(postvalue)
    if user_info is None:
        print("User does not exist!")
        return False
    confirmation = input("Are you sure you want to delete this user and related data (Y/N)? ").strip().lower()
    if confirmation != "y":
        print("User deletion canceled.")
        return
    cursor.execute("DELETE FROM Followers WHERE FollowerID = :1 OR FollowingID = :1", (user_id,))
    cursor.execute('DELETE FROM "Comment" WHERE UserID = :1', (user_id,))
    cursor.execute('DELETE FROM "Like" WHERE UserID = :1', (user_id,))
    cursor.execute('DELETE FROM "Share" WHERE UserID = :1', (user_id,))
    cursor.execute("DELETE FROM SharedWith WHERE ShareID IN (SELECT ShareID FROM  \"Share\" WHERE UserID = :1)", (user_id,))
    cursor.execute("DELETE FROM TaggedUser WHERE TaggedUserID = :1", (user_id,))
    cursor.execute("DELETE FROM Post WHERE UserID = :1", (user_id,))
    cursor.execute("DELETE FROM SharedWith WHERE ShareID NOT IN (SELECT PostID FROM Post)")
    cursor.execute("DELETE FROM TaggedUser WHERE PostID NOT IN (SELECT PostID FROM Post)")
    cursor.execute("DELETE FROM UserRegistration WHERE UserID = :1", (user_id,))
    for i in postvalue:
        cursor.execute("DELETE FROM Post WHERE PostID = :1", (i,))
        cursor.execute("DELETE FROM \"Like\" WHERE PostID = :1", (i,))
        cursor.execute('DELETE FROM "Comment" WHERE PostID = :1', (i,))
        cursor.execute('DELETE FROM "Share" WHERE PostID = :1', (i,))
        cursor.execute("DELETE FROM SharedWith WHERE ShareID NOT IN (SELECT PostID FROM Post)")
        cursor.execute("DELETE FROM TaggedUser WHERE PostID NOT IN (SELECT PostID FROM Post)")
    connection.commit()
    print("User account and related data deleted successfully!")
def delete_post():
    post_id = int(input("Enter Post ID to delete: "))
    cursor.execute("SELECT * FROM Post WHERE PostID = :1", (post_id,))
    post_info = cursor.fetchone()
    if post_info is None:
        print("Post does not exist!")
        return False
    confirmation = input("Are you sure you want to delete this post and related data (Y/N)? ").strip().lower()
    if confirmation != "y":
        print("Post deletion canceled.")
        return
    cursor.execute("DELETE FROM Post WHERE PostID = :1", (post_id,))
    cursor.execute("DELETE FROM \"Like\" WHERE PostID = :1", (post_id,))
    cursor.execute('DELETE FROM "Comment" WHERE PostID = :1', (post_id,))
    cursor.execute('DELETE FROM "Share" WHERE PostID = :1', (post_id,))
    cursor.execute("DELETE FROM SharedWith WHERE ShareID NOT IN (SELECT PostID FROM Post)")
    cursor.execute("DELETE FROM TaggedUser WHERE PostID NOT IN (SELECT PostID FROM Post)")
    connection.commit()
    print(f"Post with ID {post_id} and related data deleted successfully!")
def update_comment_description():
    comment_id = int(input("Enter Comment ID to update: "))
    cursor.execute("SELECT * FROM \"Comment\" WHERE CommentID = :1", (comment_id,))
    comment_info = cursor.fetchone()
    if comment_info is None:
        print("Comment does not exist!")
        return False
    new_description = input("Enter the updated comment: ")
    cursor.execute("UPDATE \"Comment\" SET Description = :1 WHERE CommentID = :2", (new_description, comment_id))
    connection.commit()
    print("Comment description updated successfully!")
def delete_comment():
    comment_id = int(input("Enter Comment ID to delete: "))
    cursor.execute("SELECT * FROM \"Comment\" WHERE CommentID = :1", (comment_id,))
    comment_info = cursor.fetchone()
    cursor.execute("SELECT PostID FROM \"Comment\" WHERE CommentID = :1", (comment_id,))
    post_id = cursor.fetchone()
    if comment_info is None:
        print("Comment does not exist!")
        return False
    confirmation = input("Are you sure you want to delete this comment (Y/N)? ").strip().lower()
    if confirmation != "y":
        print("Comment deletion canceled.")
        return
    cursor.execute("DELETE FROM \"Comment\" WHERE CommentID = :1", (comment_id,))
    cursor.execute("""
        UPDATE Post
        SET NoOfComments = NoOfComments - 1
        WHERE PostID = :1
    """, (post_id[0],))
    connection.commit()
    print(f"Comment with ID {comment_id} deleted successfully!")
def delete_like():
    like_id = int(input("Enter Like ID to delete: "))
    cursor.execute("SELECT * FROM \"Like\" WHERE LikeID = :1", (like_id,))
    like_info = cursor.fetchone()
    cursor.execute("SELECT PostID FROM \"Like\" WHERE LikeID = :1", (like_id,))
    post_id = cursor.fetchone()
    if like_info is None:
        print("Like does not exist!")
        return False
    confirmation = input("Are you sure you want to delete this like (Y/N)? ").strip().lower()
    if confirmation != "y":
        print("Like deletion canceled.")
        return
    cursor.execute("DELETE FROM \"Like\" WHERE LikeID = :1", (like_id,))
    cursor.execute("""
        UPDATE Post
        SET NoOfLikes = NoOfLikes - 1
        WHERE PostID = :1
    """, (post_id[0],))
    connection.commit()
    print(f"Like with ID {like_id} deleted successfully!")
def display_user_info():
    user_id = int(input("Enter User ID to display information: "))
    cursor.execute("SELECT * FROM UserRegistration WHERE UserID = :1", (user_id,))
    user_info = cursor.fetchone()
    if user_info is None:
        print("User does not exist!")
        return False
    cursor.execute("SELECT FollowingID FROM Followers WHERE FollowerID = :1", (user_id,))
    followers = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT FollowerID FROM Followers WHERE FollowingID = :1", (user_id,))
    following = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*) FROM Post WHERE UserID = :1", (user_id,))
    post_count = cursor.fetchone()[0]
    print("User Information:")
    print(f"User ID: {user_info[0]}")
    print(f"First Name: {user_info[1]}")
    print(f"Last Name: {user_info[2]}")
    print(f"Date of Birth: {user_info[3].strftime('%Y-%m-%d')}")
    print(f"Age: {user_info[4]}")
    print(f"No Of Followers: {len(followers)}")
    print(f"No Of Following: {len(following)}")
    print(f"Followers: {', '.join(map(str, followers))}")
    print(f"Following: {', '.join(map(str, following))}")
    print(f"Number of Posts: {post_count}")
    cursor.execute("SELECT PostID, Description, DateOfPost FROM Post WHERE UserID = :1", (user_id,))
    posts = cursor.fetchall()
    if len(posts) > 0:
        print("\nUser's Posts:")
        post_table = PrettyTable()
        post_table.field_names = ["Post ID", "Description", "Date of Post"]
        for post in posts:
            post_table.add_row(post)
        print(post_table)
    else:
        print("User has not posted any content.")
def print_table(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    table_data = cursor.fetchall()
    if len(table_data) > 0:
        print(f"\n{table_name} Table:")
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        for row in table_data:
            table.add_row(row)
        print(table)
    else:
        print(f"\n{table_name} Table is empty.")
def print_all_tables():
    print("Available Tables:")
    print("1. UserRegistration")
    print("2. Followers")
    print("3. Post")
    print("4. Comment")
    print("5. Like")
    print("6. Share")
    print("7. SharedWith")
    print("8. TaggedUser")
    table_choice = input("Enter the number of the table you want to print (1-8): ")
    if table_choice == "1":
        print_table("UserRegistration")
    elif table_choice == "2":
        print_table("Followers")
    elif table_choice == "3":
        print_table("Post")
    elif table_choice == "4":
        print_table('"Comment"')
    elif table_choice == "5":
        print_table('"Like"')
    elif table_choice == "6":
        print_table('"Share"')
    elif table_choice == "7":
        print_table("SharedWith")
    elif table_choice == "8":
        print_table("TaggedUser")
    else:
        print("Invalid table choice. Please try again.")
while True:
    print("\nMenu:")
    print("1. User Registration")
    print("2. Follow a Person")
    print("3. Post")
    print("4. Like a Post")
    print("5. Comment on a Post")
    print("6. Share a Post")
    print("7. Delete a Post")
    print("8. Update User Information")
    print("9. Delete User Account")
    print("10. Update Comment Description")
    print("11. Delete Comment")
    print("12. Delete Like")
    print("13. Display User Information")
    print("14. Print a Table")
    print("0. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        user_registration()
    elif choice == "2":
        follow_user()
    elif choice == "3":
        post()
    elif choice == "4":
        like_post()
    elif choice == "5":
        comment_post()
    elif choice == "6":
        share_post()
    elif choice == "7":
        delete_post()
    elif choice == "8":
        update_user_info()
    elif choice == "9":
        delete_user_account()
    elif choice == "10":
        update_comment_description()
    elif choice == "11":
        delete_comment()
    elif choice == "12":
        delete_like()
    elif choice == "13":
        display_user_info()
    elif choice == "14":
        print_all_tables()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please try again.")
cursor.close()
connection.close()

