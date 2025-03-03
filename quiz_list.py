import requests
import os
import json
from dotenv import load_dotenv

# Load environment variablesffdsfds
load_dotenv()

# Canvas API URL and credentials
API_URL = "https://boisestatecanvas.instructure.com/api/v1"
NEW_QUIZ_API_URL = "https://boisestatecanvas.instructure.com/api/quiz/v1"
ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")


# Function to get classic quizzes
def get_classic_quizzes(course_id):
    url = f"{API_URL}/courses/{course_id}/quizzes"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching classic quizzes: {e}")
    return []


# Function to get new quizzes
def get_new_quizzes(course_id):
    url = f"{API_URL}/courses/{course_id}/assignments"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
        assignments = response.json()
        new_quizzes = [
            a for a in assignments
            if (a.get("integration_id") or a.get("lti_context_id"))
               and "external_tool" in a.get("submission_types", [])
        ]
        return new_quizzes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching new quizzes: {e}")
    return []


# Function to fetch classic quiz questions
def get_classic_quiz_questions(course_id, quiz_id):
    url = f"{API_URL}/courses/{course_id}/quizzes/{quiz_id}/questions"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions for classic quiz {quiz_id}: {e}")
    return []


# Function to fetch new quiz questions
def get_new_quiz_questions(course_id, assignment_id):
    url = f"{NEW_QUIZ_API_URL}/courses/{course_id}/quizzes/{assignment_id}/items"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions for new quiz {assignment_id}: {e}")
    return []


# Ask for the course ID
course_id = input("Enter the Course ID: ")

# Fetch Classic and New Quizzes
classic_quizzes = get_classic_quizzes(course_id)
new_quizzes = get_new_quizzes(course_id)

# Display results
print("\nClassic Quizzes:")
if classic_quizzes:
    for quiz in classic_quizzes:
        print(f"- {quiz['id']}: {quiz['title']}")
else:
    print("No classic quizzes found.")

print("\nNew Quizzes:")
if new_quizzes:
    for quiz in new_quizzes:
        print(f"- {quiz['id']}: {quiz['name']} (LTI-based)")
else:
    print("No new quizzes found.")

# Ask if user wants to export quizzes
export_choice = input("\nWould you like to export these quizzes? (yes/no): ").strip().lower()
if export_choice == "yes":
    os.makedirs("exported_quizzes", exist_ok=True)

    # Export Classic Quizzes
    for quiz in classic_quizzes:
        quiz_id = quiz["id"]
        questions = get_classic_quiz_questions(course_id, quiz_id)
        quiz_data = {
            "quiz_id": quiz_id,
            "title": quiz["title"],
            "settings": quiz,
            "questions": questions,
        }
        with open(f"exported_quizzes/classic_quiz_{quiz_id}.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, indent=4)
        print(f"Exported Classic Quiz: {quiz['title']} (ID: {quiz_id})")

    # Export New Quizzes
    for quiz in new_quizzes:
        quiz_id = quiz["id"]
        questions = get_new_quiz_questions(course_id, quiz_id)
        quiz_data = {
            "quiz_id": quiz_id,
            "title": quiz["name"],
            "settings": quiz,
            "questions": questions,
        }
        with open(f"exported_quizzes/new_quiz_{quiz_id}.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, indent=4)
        print(f"Exported New Quiz: {quiz['name']} (ID: {quiz_id})")

    print("\nExport complete. JSON files are saved in the 'exported_quizzes' folder.")
