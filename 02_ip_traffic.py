#Turn code completion off when starting this assignment
# Do not use co-pilot to complete this assignment.
import random
import datetime

# The following function creates a log of IP log entries
# Update the M Number in the first line of code in this function
def create_traffic():
    m_number = 1111  # replace this 4 digit number with the last 4 of your Mnumber
    random.seed(m_number)
    ip_addresses = [
    "192.168.1.10", "172.16.5.23", "203.0.113.45", "198.51.100.89", 
    "10.0.0.15", "192.168.1.25", "203.0.113.90", "198.51.100.20", 
    "172.16.5.89", "10.0.0.200"]
    status_codes = [200, 201, 302, 400, 401, 403, 404, 500]
    request_types = ["GET", "POST", "DELETE", "PATCH"]
    resources = ["/home", "/login", "/dashboard", "/products", "/cart/add",
                  "/orders", "/account", "/profile/update", "/search?q=laptop", "/logout"]

    ip_log_entries = []
    start_time = datetime.datetime(2025, 3, 28, 10, 0, 0)
    for _ in range(100):
        log_entry = {
            "ip_address": random.choice(ip_addresses),
            "timestamp": (start_time + datetime.timedelta(seconds=random.randint(1, 3600))).strftime("%Y-%m-%d %H:%M:%S"),
            "request_type": random.choice(request_types),
            "resource": random.choice(resources),
            "status_code": random.choice(status_codes),
            "response_time_ms": random.randint(50, 1500),  # Response time between 50ms and 1500ms
        }
        ip_log_entries.append(log_entry)
    return ip_log_entries

# Task 1
# Write a function that returns the three most frequent ip addresses. 
def frequent_ip(logs, many=3):
    frequents = []
    # write your code here
    return frequents

# Commit your code.  Write the commit message here....
#

# Task #2
# As a security analyst, you want to know what  resources a particular 
# visitor accessed.  Given the logs and ip_address, create the sequence 
# of resources that has a status 200. 
def naviation(logs, ip_address, status='200'):
    sequence = ""
    # Write your code here
    return sequence

# Commit your code.  Write the commit message here....
#



# Task #3
# update the main def block, so that it allows the user to 
# call frequent_ip and navigation functions.

def main():
    logs = create_traffic()
    #print(logs)
    while True:
        user_choice = input("Enter 1 for frequent_ip and 2 for navigation: ")
        # write code for prompting the user for their choice
        if not(user_choice) in '12':
            break
        else:
            # do user's action
            pass

# Commit your code.  Write the commit message here....
#

main()
