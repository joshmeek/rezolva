import unittest
import os
import sys
import tempfile
import shutil
import importlib.util
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

class RezolvaE2ESmokeTest(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Path to examples directory
        self.examples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples'))
        
        # Path to the deduplication subdirectory
        self.dedup_dir = os.path.join(self.examples_dir, 'deduplication')
        
        # Ensure the directories exist
        self.assertTrue(os.path.isdir(self.examples_dir), f"Examples directory not found: {self.examples_dir}")
        self.assertTrue(os.path.isdir(self.dedup_dir), f"Deduplication directory not found: {self.dedup_dir}")

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_run_all_examples(self):
        # Run examples from the main directory
        self.run_examples_in_directory(self.examples_dir)
        
        # Run examples from the deduplication subdirectory
        self.run_examples_in_directory(self.dedup_dir)

    def run_examples_in_directory(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                with self.subTest(example=os.path.join(os.path.basename(directory), filename)):
                    self.run_example(os.path.join(directory, filename))

    def run_example(self, file_path):
        # Capture stdout and stderr
        stdout = StringIO()
        stderr = StringIO()
        
        # Change to the temporary directory
        original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Add the directory containing the example to sys.path temporarily
            sys.path.insert(0, os.path.dirname(file_path))
            
            # Load the module
            spec = importlib.util.spec_from_file_location(os.path.basename(file_path)[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            
            # Redirect stdout and stderr, then execute the module
            with redirect_stdout(stdout), redirect_stderr(stderr):
                spec.loader.exec_module(module)
            
            # Check if there were any errors
            self.assertEqual(stderr.getvalue(), '', f"Errors occurred while running {file_path}:\n{stderr.getvalue()}")
            
            # Print or log the stdout for debugging
            # print(f"Output from {file_path}:\n{stdout.getvalue()}")
            
        except Exception as e:
            self.fail(f"Exception occurred while running {file_path}: {str(e)}")
        
        finally:
            # Change back to the original directory
            os.chdir(original_dir)
            
            # Remove the directory from sys.path
            sys.path.pop(0)

if __name__ == '__main__':
    unittest.main()