import os
import json
import re
from bs4 import BeautifulSoup


def clean_html(text):
    """Remove HTML tags and return plain text."""
    if not text:
        return ""
    return BeautifulSoup(text, "html.parser").get_text(separator=" ").strip()


def format_question(question):
    """Format a question based on the provided quiz export format."""
    q_type = question.get("question_type", "unknown")
    text = clean_html(question.get("question_text", "(No question text)"))
    formatted = f"{question['id']}. {text}\n"

    if q_type == "multiple_choice_question":
        for answer in question.get("answers", []):
            prefix = "*" if answer.get("weight", 0) > 0 else ""
            formatted += f"{prefix}{clean_html(answer['text'])}\n"

    elif q_type == "multiple_answers_question":
        for answer in question.get("answers", []):
            marker = "[*]" if answer.get("weight", 0) > 0 else "[ ]"
            formatted += f"{marker} {clean_html(answer['text'])}\n"

    elif q_type == "short_answer_question":
        for answer in question.get("answers", []):
            formatted += f"* {clean_html(answer['text'])}\n"

    elif q_type == "essay_question":
        formatted += "####\n"

    elif q_type == "file_upload_question":
        formatted += "^^^^\n"

    elif q_type == "true_false_question":
        correct_answer = "a) True" if question.get("correct_answer") else "b) False"
        incorrect_answer = "b) False" if question.get("correct_answer") else "a) True"
        formatted += f"*{correct_answer}\n{incorrect_answer}\n"

    return formatted + "\n"


def export_quizzes_to_text(json_folder, output_file):
    """Read quiz JSON files and format them into a single text file."""
    json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "exported_quizzes"))
    output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), output_file))

    print(f"Checking folder: {json_folder}")

    if not os.path.exists(json_folder):
        print(f"Error: The folder '{json_folder}' does not exist.")
        return

    files = os.listdir(json_folder)
    print(f"Found {len(files)} files: {files}")

    quiz_count = 0
    with open(output_file, "w", encoding="utf-8") as out:
        for filename in files:
            if filename.endswith(".json"):
                print(f"Processing {filename}...")
                with open(os.path.join(json_folder, filename), "r", encoding="utf-8") as f:
                    quiz = json.load(f)

                    out.write(f"Quiz Title: {clean_html(quiz['title'])}\n")
                    out.write(f"Total Points: {quiz['settings'].get('points_possible', 'N/A')}\n")
                    instructions = quiz['settings'].get('description', 'No instructions provided')
                    out.write(f"Instructions: {clean_html(instructions)}\n")
                    out.write("\n--- Questions ---\n\n")

                    question_count = 0
                    for question in quiz.get("questions", []):
                        out.write(format_question(question))
                        question_count += 1

                    out.write("\n=== End of Quiz ===\n\n")
                    print(f"Processed {question_count} questions from {quiz['title']}")
                    quiz_count += 1
    print(f"Export complete. {quiz_count} quizzes processed. Output saved to {output_file}")


# Example usage:fdsfdsa
export_quizzes_to_text("exported_quizzes", "quiz_export.txt")
