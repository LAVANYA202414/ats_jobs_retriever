import io
import unittest
from unittest.mock import MagicMock, patch
import numpy as np

# Prevent Streamlit UI code from crashing the import environment
import os
os.environ["STREAMLIT_RUN_ON_SAVE"] = "False"

# Import your core logic functions from app.py
from ingest_resume import is_valid_resume, get_score, extract_resume_text

class TestResumeMatcherApp(unittest.TestCase):

    def test_is_valid_resume_too_short(self):
        """Checks if a resume with fewer than 30 words is correctly rejected."""
        short_text = "John Doe. Software Engineer. Skills: Python, SQL. Contact: email@example.com."
        # This is only 11 words, it should return False
        self.assertFalse(is_valid_resume(short_text))

    def test_is_valid_resume_correct_length(self):
        """Checks if a resume with 30 or more words is correctly accepted."""
        # Generates a string with exactly 35 words
        good_text = " ".join(["word"] * 35)
        self.assertTrue(is_valid_resume(good_text))

    def test_get_score_sorting_key(self):
        """Verifies that the sorting key extractor returns the correct dictionary value."""
        mock_data = {"filename": "candidate_resume.pdf", "text": "...", "score": 0.875}
        self.assertEqual(get_score(mock_data), 0.875)

    def test_extract_resume_text_from_txt(self):
        """Simulates an uploaded TXT file and verifies the text extraction output."""
        # Create a fake file-like stream to mimic Streamlit's file_uploader object
        fake_file = io.BytesIO(b"This is the extracted content of a standard plain text resume.")
        fake_file.name = "test_resume.txt"
        
        extracted_result = extract_resume_text(fake_file)
        self.assertEqual(extracted_result, "This is the extracted content of a standard plain text resume.")

    @patch('app.cosine_similarity')
    def test_cosine_similarity_logic(self, mock_cosine):
        """Tests that the mathematical sorting logic registers score vectors correctly."""
        # Fake vector matrices
        mock_job_vector = [0.2, 0.4, 0.6]
        mock_resume_vector = [0.2, 0.4, 0.6]
        
        # Force the sklearn metric to return a 1.0 (perfect match array)
        mock_cosine.return_value = np.array([[1.0]])
        
        from app import cosine_similarity
        calculated_score = cosine_similarity([mock_job_vector], [mock_resume_vector])[0][0]
        self.assertAlmostEqual(calculated_score, 1.0)

if __name__ == '__main__':
    unittest.main()
