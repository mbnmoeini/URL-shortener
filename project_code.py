import pyodbc
import random
import string
from datetime import datetime, timedelta

server_name = 'DESKTOP-OQ1N3DT'
database_name = 'project-DB'
conn_str = f'Driver={{ODBC Driver 17 for SQL Server}};Server={server_name};Database={database_name};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

#generate a random 6-character string
def generate_shortened_link():
    domain = string.ascii_lowercase + string.digits
    return ''.join(random.choice(domain) for _ in range(6))

#register a new link
def register_link(original_link):
    # Check if the link already exists
    cursor.execute("select shortened_link from links where original_link = ?", original_link)
    row = cursor.fetchone()

    #return the previous shortened link    
    if row:
        return row.shortened_link
    #generate a new shortened link
    else:
        shortened_link = generate_shortened_link()
        cursor.execute("insert into links (original_link, shortened_link) values (?, ?)", original_link, shortened_link)
        conn.commit()

        return shortened_link

def check_expired_links():
    expiration_date = datetime.now() - timedelta(weeks=1)

    #Update the expired value to 1 for links that haven't been referenced for a week
    cursor.execute("update links set expired = 1 where created_date < ? AND references_count = 0", expiration_date)
    conn.commit()

def top_links():
    #execute the top_links procedure to fetch the 3 top referred links
    cursor.execute("exec top_links")
    rows = cursor.fetchall()

    print("Top Referred Links:")
    for row in rows:
        shortened_link = row[0]
        references_count = row[1]
        print(f"Shortened Link: {shortened_link}, References: {references_count}")

def link_maps():
    #execute the link_maps function to fetch link maps with its expiration and reference count
    cursor.execute("select * from link_maps()")
    rows = cursor.fetchall()

    print("Link Maps:")
    for row in rows:
        print(f"Shortened Link: {row.shortened_link}, Remaining Time: {row.remaining_time} days, References: {row.references_count}")

# Function to register a reference to a link
def register_reference(shortened_link):
    cursor.execute("select link_id FROM links where shortened_link=?", shortened_link)
    row = cursor.fetchone()
    if row is not None:

        # Insert the reference into the database
        cursor.execute("insert into references_link (shortened_link) values (?)", shortened_link)
        conn.commit()

        return True
    else:
        return False



answer = int(input("please enter 1 if you want to enter a new link\nenter 2 if you want to reference to one link: \n"))
if answer == 1:
    #example link
    original_link = input("Enter your link:")

    #register a new link
    shortened_link = register_link(original_link)
    print(f"Shortened Link: {shortened_link}")
else:
# Register a reference to a link
    shortened_link = input("Enter the shortened link: \n")
    if register_reference(shortened_link):
        print("Reference registered successfully")
    else:
        print("Link does not exist")

top_links()
link_maps()
