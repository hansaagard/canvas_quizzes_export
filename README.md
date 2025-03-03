# Canvas Quiz Exporter

This project consists of two Python scripts that interact with the Canvas LMS API to export quiz content and format it into a structured text file.

## **Setup**
### **1. Install Dependencies**
Ensure you have Python installed, then install the required dependencies:
```bash
pip install requests python-dotenv beautifulsoup4
```

### **2. Configure the .env File**
Create a `.env` file in the project root and add your **Canvas API token**:
```
CANVAS_ACCESS_TOKEN=your_canvas_api_token_here
```
Replace `your_canvas_api_token_here` with a valid API token from Canvas.

---

## **Scripts Overview**

### **1. `quiz_list.py`**
📥 **Purpose:** Connects to Canvas, retrieves quizzes from a specified course, and saves them as JSON files in `exported_quizzes/`.

#### **Usage:**
Run the script and enter a **Canvas Course ID** when prompted:
```bash
python quiz_list.py
```
📌 **Output:**
- Creates an `exported_quizzes/` folder (if it doesn’t exist).
- Saves quizzes as JSON files (`classic_quiz_XXXXX.json` or `new_quiz_XXXXX.json`).

---

### **2. `quiz_export.py`**
📤 **Purpose:** Reads quiz JSON files from `exported_quizzes/` and converts them into a formatted text file (`quiz_export.txt`).

#### **Usage:**
```bash
python quiz_export.py
```
📌 **Output:**
- Generates `quiz_export.txt`, containing:
  - Quiz **title, total points, instructions, and settings**
  - All **questions and answers**, formatted correctly

---

## **Example Workflow**
1. Run `quiz_list.py` and provide a **Canvas Course ID**.
2. The script pulls quizzes and saves them as `.json` in `exported_quizzes/`.
3. Run `quiz_export.py` to format the JSON data into `quiz_export.txt`.

🚀 **Your quizzes are now exported and formatted!**