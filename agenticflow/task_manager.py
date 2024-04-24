import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

class TaskManager:
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab)
        self.add_patterns()

    def add_patterns(self):
        task_pattern = [{"POS": "VERB"}, {"POS": "NOUN"}]
        due_date_pattern = [{"LOWER": "due"}, {"LOWER": "on"}, {"ENT_TYPE": "DATE"}]
        priority_pattern = [{"LOWER": "priority"}, {"LOWER": "is"}, {"ENT_TYPE": "ORDINAL"}]
        category_pattern = [{"LOWER": "category"}, {"LOWER": "is"}, {"POS": "NOUN"}]
        assignee_pattern = [{"LOWER": "assignee"}, {"LOWER": "is"}, {"POS": "PROPN"}]

        self.matcher.add("TASK", [task_pattern])
        self.matcher.add("DUE_DATE", [due_date_pattern])
        self.matcher.add("PRIORITY", [priority_pattern])
        self.matcher.add("CATEGORY", [category_pattern])
        self.matcher.add("ASSIGNEE", [assignee_pattern])

    def extract_tasks(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        tasks = []

        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            span = doc[start:end]

            if label == "TASK":
                task_text = span.text
                tasks.append({"task": task_text, "status": "pending"})
            elif label == "DUE_DATE":
                due_date = doc[end-1].text
                tasks[-1]["due_date"] = due_date
            elif label == "PRIORITY":
                priority = doc[end-1].text
                tasks[-1]["priority"] = priority
            elif label == "CATEGORY":
                category = doc[end-1].text
                tasks[-1]["category"] = category
            elif label == "ASSIGNEE":
                assignee = doc[end-1].text
                tasks[-1]["assignee"] = assignee

        return tasks

    def update_task_status(self, task, status):
        task["status"] = status
        return task

    def filter_tasks_by_category(self, tasks, category):
        filtered_tasks = [task for task in tasks if task.get("category") == category]
        return filtered_tasks

    def filter_tasks_by_assignee(self, tasks, assignee):
        filtered_tasks = [task for task in tasks if task.get("assignee") == assignee]
        return filtered_tasks

    def filter_tasks_by_status(self, tasks, status):
        filtered_tasks = [task for task in tasks if task.get("status") == status]
        return filtered_tasks

    def sort_tasks_by_priority(self, tasks):
        priority_order = {"high": 3, "medium": 2, "low": 1}
        sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority"), 0), reverse=True)
        return sorted_tasks

    def generate_task_summary(self, tasks):
        total_tasks = len(tasks)
        pending_tasks = len(self.filter_tasks_by_status(tasks, "pending"))
        in_progress_tasks = len(self.filter_tasks_by_status(tasks, "in progress"))
        completed_tasks = len(self.filter_tasks_by_status(tasks, "completed"))

        summary = f"Task Summary:\n"
        summary += f"Total Tasks: {total_tasks}\n"
        summary += f"Pending Tasks: {pending_tasks}\n"
        summary += f"In Progress Tasks: {in_progress_tasks}\n"
        summary += f"Completed Tasks: {completed_tasks}\n"

        return summary