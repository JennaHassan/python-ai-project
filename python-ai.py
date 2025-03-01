import openai
import os

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# task storage
tasks = []

# To generate a response from ChatGPT
def chat_with_gpt(message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You check when the user wants their task completed and then arrange the list in order of due dates."},
            {"role": "user", "content": message}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# Task management functions
def create_task(task_name):
    due_date = input("By when do you need to complete this? ").lower()
    task = {"task": task_name, "due_date": due_date}
    tasks.append(task)
    return f"Task '{task_name}' (Due: {due_date}) has been added."

def list_tasks():
    if not tasks:
        return "No tasks available."
    
    # A string with all the tasks and their due dates
    task_list = "\n".join([f"{i+1}. {task['task']} (Due: {task['due_date']})" for i, task in enumerate(tasks)])

    # Prompt to ask ChatGPT to sort tasks based on due dates
    prompt = f"Please sort the following tasks by due date (today, tomorrow, next week, etc.) in chronological order:\n{task_list}\n\nProvide the tasks sorted by their due dates."

    # Send the prompt to ChatGPT to get the sorted task list
    rearranged_tasks = chat_with_gpt(prompt)
    return rearranged_tasks

def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        removed_task = tasks.pop(task_index)
        return f"Task '{removed_task['task']}' has been deleted."
    return "Task not found."

# Main program loop
def main():
    print("Welcome to your Task Manager Bot!")
    while True:
        user_input = input("\nWhat would you like to do? (Create/ List/ Delete/ Exit): ").lower()

        if user_input == "exit":
            print("Goodbye!")
            break

        elif user_input == "create":
            task_name = input("Enter the task name: ")
            response = create_task(task_name)
            print(response)

        elif user_input == "list":
            response = list_tasks()
            print("Here are your tasks:")
            print(response)   

        elif user_input == "delete":
            # Print the list so the user knows what to delete
            task_list = list_tasks()
            print("Here are your tasks:")
            print(task_list)

            try:
                task_number = int(input("Enter the task number to delete: ")) - 1
                response = delete_task(task_number)
                print(response)
            except ValueError:
                print("Invalid input. Please enter a number.")

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
