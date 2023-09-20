# URL-shortener
This project is developed using the Python programming language and employs SQL Server for data storage. The features of this project are outlined below:

1. **Registering a New Link**: The system accepts an input string (e.g., com.averylongurl.www). If this link has already been shortened, it returns the previous value. Otherwise, it generates and maps a new random 6-character string composed of lowercase letters and numbers.

2. **Referencing a Shortened Link**: The system receives a string containing the shortened form of a link. If the equivalent link is registered in the system, it returns it; otherwise, it generates an error.

3. **Dashboard Information**:
   - Displaying the number of newly registered links per day.
   - Showing the count of referrals to shortened links per day.
   - Displaying the top 3 links that have received the most referrals.
   - Listing all mappings in the system, along with the remaining time until expiration and the number of referrals they have received.

This project serves as a URL shortening service implemented in Python, utilizing SQL Server for data management.




