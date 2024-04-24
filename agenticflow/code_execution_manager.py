import os
import subprocess
import tempfile
import logging
import cProfile
import pstats
import io
import ast
import astroid
import pylint.lint
import traceback
import pytest
from pylint import config

class CodeExecutionManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.workspace_folder = "workspace"
        os.makedirs(self.workspace_folder, exist_ok=True)

    def save_file(self, filepath, content):
        filepath = os.path.join(self.workspace_folder, filepath)
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            self.logger.info(f"File '{filepath}' saved successfully.")
            return True
        except Exception as e:
            self.logger.exception(f"Error saving file '{filepath}': {str(e)}")
            return False

    def read_file(self, filepath):
        filepath = os.path.join(self.workspace_folder, filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            self.logger.info(f"File '{filepath}' read successfully.")
            return content
        except FileNotFoundError:
            self.logger.error(f"File '{filepath}' not found.")
            return None
        except Exception as e:
            self.logger.exception(f"Error reading file '{filepath}': {str(e)}")
            return None
    def list_files_in_workspace(self):
        try:
            files = os.listdir(self.workspace_folder)
            self.logger.info("List of files in workspace retrieved successfully.")
            return files
        except Exception as e:
            self.logger.exception(f"Error listing files in workspace: {str(e)}")
            return None

    def test_code(self, code):
        if not code:
            return None, None

        with tempfile.TemporaryDirectory(dir=self.workspace_folder) as temp_dir:
            script_path = os.path.join(temp_dir, 'temp_script.py')
            with open(script_path, 'w') as f:
                f.write(code)

            try:
                # Use pytest to run tests and capture output
                result = pytest.main([script_path])
                
                if result == 0:
                    self.logger.info("Tests execution successful.")
                    return "All tests passed.", None
                else:
                    self.logger.error("Tests execution failed.")
                    return None, "Some tests failed."
            except subprocess.TimeoutExpired:
                self.logger.error("Tests execution timed out after 30 seconds.")
                return None, "Execution timed out after 30 seconds"
            except Exception as e:
                self.logger.exception(f"Tests execution error: {str(e)}")
                return None, f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"

    def execute_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            self.logger.info(f"Command executed: {command}")
            return result.stdout, result.stderr
        except Exception as e:
            self.logger.exception(f"Error executing command: {str(e)}")
            return None, str(e)

    def optimize_code(self, code):
        try:
            # Save the code to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
                tmp.write(code.encode('utf-8'))
                tmp_file_path = tmp.name

            # Configure Pylint with custom settings
            pylint_config_path = pylint.config.find_pylintrc()
            pylint_args = [tmp_file_path, "--rcfile", pylint_config_path]

            # Run Pylint analysis
            pylint_output = subprocess.check_output(["pylint"] + pylint_args, universal_newlines=True)

            # Parse Pylint output and provide actionable suggestions
            suggestions = []
            for line in pylint_output.splitlines():
                if line.startswith("C:") or line.startswith("R:") or line.startswith("W:"):
                    msg_id, _, msg = line.partition(":")
                    suggestion = f"Suggestion: {msg.strip()}"
                    if msg_id.startswith("C:"):
                        suggestion += " (Convention Violation)"
                    elif msg_id.startswith("R:"):
                        suggestion += " (Refactoring Opportunity)"
                    elif msg_id.startswith("W:"):
                        suggestion += " (Potential Bug)"
                    suggestions.append(suggestion)

            # Cleanup temporary file
            os.remove(tmp_file_path)

            if suggestions:
                optimization_suggestions = "\n".join(suggestions)
                self.logger.info(f"Optimization suggestions:\n{optimization_suggestions}")
                return optimization_suggestions
            else:
                self.logger.info("No optimization suggestions found.")
                return "No optimization suggestions found."

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Pylint analysis failed: {e.output}")
            return None

        except Exception as e:
            self.logger.exception(f"Error during optimization: {str(e)}")
            return None

    def format_code(self, code):
        try:
            # Save the code to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
                tmp.write(code.encode('utf-8'))
                tmp_file_path = tmp.name

            # Run Black code formatter
            subprocess.run(["black", tmp_file_path], check=True)

            # Read the formatted code from the temporary file
            with open(tmp_file_path, "r", encoding="utf-8") as f:
                formatted_code = f.read()

            # Cleanup temporary file
            os.remove(tmp_file_path)

            self.logger.info("Code formatting completed.")
            return formatted_code

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Code formatting failed: {e.output}")
            return None

        except Exception as e:
            self.logger.exception(f"Error during code formatting: {str(e)}")
            return None


def format_error_message(error):
    return f"Error: {str(error)}\nTraceback: {traceback.format_exc()}"

def run_tests(code):
    code_execution_manager = CodeExecutionManager()
    test_code_output, test_code_error = code_execution_manager.test_code(code)
    if test_code_output:
        print(f"\n[TEST CODE OUTPUT]\n{test_code_output}")
    if test_code_error:
        print(f"\n[TEST CODE ERROR]\n{test_code_error}")

def monitor_performance(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir="workspace") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        subprocess.run(['python', temp_file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing code: {e}")
    finally:
        profiler.disable()
        os.unlink(temp_file_path)

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats('cumulative')
    stats.print_stats()

    performance_data = stream.getvalue()
    print(f"\n[PERFORMANCE DATA]\n{performance_data}")

    return performance_data

def optimize_code(code):
    code_execution_manager = CodeExecutionManager()
    optimization_suggestions = code_execution_manager.optimize_code(code)
    if optimization_suggestions:
        print(f"\n[OPTIMIZATION SUGGESTIONS]\n{optimization_suggestions}")
    return optimization_suggestions

def format_code(code):
    code_execution_manager = CodeExecutionManager()
    formatted_code = code_execution_manager.format_code(code)
    if formatted_code:
        print(f"\n[FORMATTED CODE]\n{formatted_code}")
    return formatted_code

def pass_code_to_alex(code, alex_memory):
    alex_memory.append({"role": "system", "content": f"Code from Mike and Annie: {code}"})

def send_status_update(mike_memory, annie_memory, alex_memory, project_status):
    mike_memory.append({"role": "system", "content": f"Project Status Update: {project_status}"})
    annie_memory.append({"role": "system", "content": f"Project Status Update: {project_status}"})
    alex_memory.append({"role": "system", "content": f"Project Status Update: {project_status}"})

def generate_documentation(code):
    try:
        module = ast.parse(code)
        docstrings = []

        for node in ast.walk(module):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    docstrings.append(f"{node.name}:\n{docstring}")

        documentation = "\n".join(docstrings)
        print(f"\n[GENERATED DOCUMENTATION]\n{documentation}")

        return documentation
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return None

def commit_changes(code):
    subprocess.run(["git", "add", "workspace"])
    subprocess.run(["git", "commit", "-m", "Automated code commit"])
    subprocess.run(["git", "push"])

