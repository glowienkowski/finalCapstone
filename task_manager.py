# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os  # Module for interacting with the operating system
from datetime import datetime, date  # Module for handling date and time

# Constants
DATETIME_STRING_FORMAT = "%Y-%m-%d"  # Date format used throughout the program

# Function to load user data from 'user.txt' file
def load_user_data():
    """Load username and password data from user.txt."""
    # Create a default user file if it doesn't exist
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")  # Default admin credentials

    # Read user data from file and create a dictionary
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Create a dictionary with usernames as keys and passwords as values
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

# Function to register a new user
def reg_user(username_password):
    """Add a new user to user.txt, ensuring no duplicate usernames."""
    while True:
        new_username = input("New Username: ")  # Prompt for new username
        # Check if the username already exists
        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
        else:
            new_password = input("New Password: ")  # Prompt for new password
            confirm_password = input("Confirm Password: ")  # Prompt to confirm password

            # Check if passwords match
            if new_password == confirm_password:
                print("New user added")
                username_password[new_username] = new_password  # Add new user to dictionary

                # Append new user data to user file
                with open("user.txt", "a") as out_file:
                    out_file.write(f"\n{new_username};{new_password}")
                break
            else:
                print("Passwords do not match")

# Function to load task data from 'tasks.txt' file
def load_task_data():
    """Load task data from tasks.txt."""
    # Create a default tasks file if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    # Read task data from file and create a list of dictionaries
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        # Populate dictionary with task details
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list

# Function to add a new task
def add_task(username, task_list, registered_users):
    """Add a new task."""
    while True:
        task_username = input("Username of the person assigned to this task: ")  # Prompt for assigned username
        if task_username not in registered_users:
            print("Error: This user is not registered. Please choose a registered user.")
        else:
            break

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Prompt for due date and validate format
    while True:
        task_due_date = input("Due date of task (YYYY-MM-DD): ")
        try:
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get current date
    curr_date = date.today()

    # Create a dictionary for the new task
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add new task to the task list
    task_list.append(new_task)

    # Write updated task list to file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all_tasks(task_list):
    """View all tasks."""
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_my_tasks(username, task_list):
    """View and interact with tasks assigned to the current user."""
    my_tasks = [t for t in task_list if t['username'] == username]
    if not my_tasks:
        print("You have no tasks assigned to you.")
        return

    # Display tasks and prompt for interaction
    while True:
        print("\nYour Tasks:")
        for i, task in enumerate(my_tasks, start=1):
            print(f"{i}. Task: {task['title']}")

        print("Enter the task number to interact with it, or '-1' to return to the main menu.")
        choice = input("Your choice: ")

        if choice == '-1':
            break

        try:
            task_index = int(choice) - 1
            selected_task = my_tasks[task_index]
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid task number.")
            continue

        # Display selected task details
        print("\nSelected Task:")
        print(f"Title: {selected_task['title']}")
        print(f"Assigned to: {selected_task['username']}")
        print(f"Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Task Description:\n{selected_task['description']}")
        print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")

        # Prompt for task modification if not completed
        if not selected_task['completed']:
            edit_choice = input("Enter 'C' to mark the task as complete, 'E' to edit, or '-1' to go back: ").upper()

            if edit_choice == 'C':
                selected_task['completed'] = True
                print("Task marked as complete.")
            elif edit_choice == 'E':
                print("Choose what to edit:")
                print("1. Username")
                print("2. Due Date")
                edit_option = input("Enter your choice: ")

                if edit_option == '1':
                    new_username = input("Enter new username: ")
                    selected_task['username'] = new_username
                    print("Username updated.")
                elif edit_option == '2':
                    while True:
                        try:
                            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                            selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            print("Due date updated.")
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified.")
                else:
                    print("Invalid choice. Task not edited.")

            else:
                print("Invalid choice.")
        else:
            print("This task is already completed.")

# Function to generate reports
def generate_reports(task_list):
    """Generate reports."""
    # Task Overview Report
    task_overview_filename = "task_overview.txt"
    with open(task_overview_filename, "w") as task_overview_file:
        # Calculate task statistics
        total_tasks = len(task_list)
        completed_tasks = sum(1 for task in task_list if task['completed'])
        incomplete_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.combine(date.today(), datetime.min.time()))
        incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Write task overview report
        task_overview_file.write("Task Overview\n\n")
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Incomplete Tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")

    # User Overview Report
    user_overview_filename = "user_overview.txt"
    with open(user_overview_filename, "w") as user_overview_file:
        # Calculate user statistics
        total_users = len(set(task['username'] for task in task_list))

        user_task_stats = {}
        for task in task_list:
            if task['username'] not in user_task_stats:
                user_task_stats[task['username']] = {'total': 0, 'completed': 0, 'overdue_incomplete': 0}

            user_task_stats[task['username']]['total'] += 1
            if task['completed']:
                user_task_stats[task['username']]['completed'] += 1
            elif not task['completed'] and task['due_date'] < datetime.combine(date.today(), datetime.min.time()):
                user_task_stats[task['username']]['overdue_incomplete'] += 1

        # Write user overview report
        user_overview_file.write("User Overview\n\n")
        user_overview_file.write(f"Total Users: {total_users}\n")
        user_overview_file.write(f"Total Tasks: {total_tasks}\n")
        user_overview_file.write("\n----- User Task Statistics -----\n")
        for username, stats in user_task_stats.items():
            incomplete_tasks = stats['total'] - stats['completed']
            incomplete_percentage = (incomplete_tasks / stats['total']) * 100 if stats['total'] > 0 else 0
            overdue_incomplete_percentage = (stats['overdue_incomplete'] / stats['total']) * 100 if stats['total'] > 0 else 0
            user_overview_file.write(f"User: {username}\n")
            user_overview_file.write(f"Total Tasks: {stats['total']}\n")
            user_overview_file.write(f"Completed Tasks: {stats['completed']}\n")
            user_overview_file.write(f"Incomplete Tasks: {incomplete_tasks}\n")
            user_overview_file.write(f"Percentage of Total Tasks: {(stats['total'] / total_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of Completed Tasks: {(stats['completed'] / stats['total']) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
            user_overview_file.write(f"Overdue Incomplete Tasks: {stats['overdue_incomplete']}\n")
            user_overview_file.write(f"Percentage of Overdue Incomplete Tasks: {overdue_incomplete_percentage:.2f}%\n\n")
    print("Reports generated successfully.")

# Function to display statistics
def display_statistics(username, task_list):
    """Display statistics about tasks."""
    # Check if necessary files exist
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        print("Task or user file not found. Please generate tasks and user data first.")
        return

    # Read user data and count total users
    with open("user.txt", "r") as user_file:
        user_data = user_file.readlines()
        total_users = len(user_data)

    # Count total tasks
    total_tasks = len(task_list)

    # Count completed, incomplete, and overdue tasks
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.combine(date.today(), datetime.min.time()))

    # Calculate percentages
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Display statistics
    print("User Overview")
    print(f"Total Users: {total_users}")
    print(f"Total Tasks: {total_tasks}")

    print("\nTask Overview")
    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Incomplete Tasks: {incomplete_tasks}")
    print(f"Overdue Tasks: {overdue_tasks}")
    print(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%")
    print(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%")

    print("\nUser and task statistics displayed from text files successfully.")

# Main function
def main():
    """Main function to control the flow of the program."""
    # Load user data and task data
    username_password = load_user_data()
    task_list = load_task_data()

    logged_in = False
    # Login loop
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        # Check login credentials
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    # Main menu loop
    while True:
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

        # Menu options
        if menu == 'r':
            reg_user(username_password)

        elif menu == 'a':
            add_task(curr_user, task_list, username_password)

        elif menu == 'va':
            view_all_tasks(task_list)

        elif menu == 'vm':
            view_my_tasks(curr_user, task_list)

        elif menu == 'gr':
            generate_reports(task_list)

        elif menu == 'ds':
            display_statistics(curr_user, task_list)

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

# Entry point of the program
if __name__ == "__main__":
    main()
