# Instagram-Database-Management


# Project Title

Instagram database Management

Team name : DBMS DINOS

-Team members :

1)Vandit Patel

2)Ankit Singh

3)Vishwa Lathigara

4)Misbah Shaikh


## Description

This project involves designing a relational database for a social media platform  Instagram. This database will store and manage various data entities and their relationships to support core features of the platform, including user profiles, posts, comments, likes, shares, and user interactions.

## Features :


-Data Storage and Retrieval

-User Authentication and Authorization

-Social Graph Management

-Multimedia Content Management

-Activity Logging

-Scalability

-Data Integrity and Consistency

-Notification System

-Analytics and Insights

-Security and Privacy

-Backup and Recovery

## Objective :

The primary objective of the "Instagram Database Management System" is to design and implement an efficient, scalable, and secure database system that supports the storage, retrieval, and management of user data, multimedia content, and social interactions within the Instagram platform. The system aims to enhance the overall performance, reliability, and user experience on the Instagram platform.


## Technology Stack :

1)PL-SQL

2)SQL

3)PYTHON

## Entities and attributes
1.User entity

-User ID(Primary key)

-First Name

-Last Name

-Date of birth(DOB)

-Age

-Password

-Phoneno

-Email

2.Post entity

-Post ID(Primary key)

-Tagged User

-Description

-Email

3.Comment entity

-Comment ID (Primary Key)

-Post ID

-Date

-Time

-Image

4.Like entity

-Like ID(Primary Key)

-Post ID(Foreign Key)

-Date

-Time

5.Share entity

-Share ID(Primary key)

-Post ID(Foreign key)

-Time

-Date

-Shared user
## Different Tables created :

---UserRegistration Table:

Purpose: This table is used to store user registration information, including details such as the user's name, date of birth, age, email, phone number, and securely hashed password.
Use: It's essential for user account management and authentication. It allows users to create accounts and log in securely.

---Followers Table:

Purpose: The Followers table establishes a many-to-many relationship between users. It stores information about who follows whom.
Use: This table allows users to follow and be followed by other users. It's crucial for managing the social aspect of the platform, enabling users to build a network of followers.

---Post Table:

Purpose: The Post table is used to store information about user-generated posts, including text content, media (images or videos), and statistics about post engagement (likes, comments, shares).
Use: This table is at the core of the platform, allowing users to create, share, and engage with posts. It provides a platform for sharing content with others.

---Comment Table:

Purpose: The Comment table stores individual comments made on posts, associating them with the posts and the users who made the comments.
Use: This table enables users to interact with posts by leaving comments. It's essential for fostering discussions and conversations.

---Like Table:

Purpose: The Like table records individual likes on posts, linking them to the posts and the users who liked them.
Use: It allows users to express their appreciation for posts. Likes are a fundamental form of engagement on social media.

---Share Table:

Purpose: The Share table keeps track of posts that are shared by users. It associates shared posts with the users who shared them and the recipients.
Use: Sharing posts is a common feature on social media platforms. This table enables users to share interesting content with their followers and friends.

---SharedWith Table:

Purpose: The SharedWith table manages shared posts with multiple recipients. It creates a many-to-many relationship between shared posts and the users they are shared with.
Use: In cases where a post is shared with multiple users or groups, this table helps maintain those relationships.

---TaggedUser Table:

Purpose: The TaggedUser table tracks which users are tagged in posts, establishing a many-to-many relationship between posts and tagged users.
Use: Tagging users in posts is a common feature for notifying and involving specific users in a post's content. This table maintains those connections.
## Conclusion :

The Instagram Database Management System project aims to create a robust and scalable infrastructure to handle the complexities of a social media platform, providing users with a seamless and secure experience while ensuring the efficient management of data and interactions on the platform.

This Project has successfully achieved its objectives by designing and implementing a robust and efficient database management system to support the dynamic and complex nature of a social media platform named Instagram.





