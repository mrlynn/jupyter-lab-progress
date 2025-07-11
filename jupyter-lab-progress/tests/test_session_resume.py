import os
import json
import tempfile
import shutil
from pathlib import Path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jupyter_lab_progress import LabProgress


def test_auto_save_progress():
    """Test that progress is automatically saved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        persist_file = os.path.join(tmpdir, "test_progress.json")
        
        # Create progress tracker with auto-save
        progress = LabProgress(
            steps=["Step 1", "Step 2", "Step 3"],
            lab_name="Test Lab",
            persist=True,
            persist_file=persist_file,
            auto_save=True
        )
        
        # Mark a step as done
        progress.mark_done("Step 1", score=85)
        
        # Check that file was created and contains data
        assert os.path.exists(persist_file)
        
        with open(persist_file, 'r') as f:
            data = json.load(f)
            assert data['lab_name'] == "Test Lab"
            assert data['steps']['Step 1']['completed'] is True
            assert data['steps']['Step 1']['score'] == 85


def test_partial_progress_with_checkpoints():
    """Test partial progress tracking with checkpoints."""
    with tempfile.TemporaryDirectory() as tmpdir:
        persist_file = os.path.join(tmpdir, "test_progress.json")
        
        progress = LabProgress(
            steps=["Data Loading", "Processing", "Analysis"],
            lab_name="Data Lab",
            persist=True,
            persist_file=persist_file
        )
        
        # Add partial progress with checkpoint
        progress.mark_partial("Data Loading", 0.5, "Loaded 50% of data", "halfway")
        
        # Check that checkpoint was saved
        assert progress.steps["Data Loading"]['partial_progress'] == 0.5
        assert len(progress.steps["Data Loading"]['checkpoints']) == 1
        assert progress.steps["Data Loading"]['checkpoints'][0]['name'] == "halfway"
        assert progress.steps["Data Loading"]['checkpoints'][0]['progress'] == 0.5


def test_resume_session():
    """Test resuming a lab from saved progress."""
    with tempfile.TemporaryDirectory() as tmpdir:
        persist_file = os.path.join(tmpdir, "test_progress.json")
        
        # Create initial progress
        progress1 = LabProgress(
            steps=["Setup", "Implementation", "Testing", "Documentation"],
            lab_name="Resume Test Lab",
            persist=True,
            persist_file=persist_file
        )
        
        # Make some progress
        progress1.mark_done("Setup")
        progress1.mark_partial("Implementation", 0.7, checkpoint_name="main_feature_done")
        progress1.mark_done("Testing", score=90)
        
        # Resume the session
        progress2 = LabProgress.resume(persist_file=persist_file)
        
        # Verify state was restored
        assert progress2.lab_name == "Resume Test Lab"
        assert progress2.steps["Setup"]['completed'] is True
        assert progress2.steps["Implementation"]['partial_progress'] == 0.7
        assert len(progress2.steps["Implementation"]['checkpoints']) == 1
        assert progress2.steps["Testing"]['completed'] is True
        assert progress2.steps["Testing"]['score'] == 90
        assert progress2.steps["Documentation"]['completed'] is False
        assert progress2._is_resumed is True


def test_resume_with_lab_name():
    """Test resuming using lab name."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            # Create progress
            progress1 = LabProgress(
                steps=["A", "B", "C"],
                lab_name="Named Lab",
                persist=True
            )
            progress1.mark_done("A")
            
            # Resume using lab name
            progress2 = LabProgress.resume(lab_name="Named Lab")
            assert progress2.steps["A"]['completed'] is True
            
        finally:
            os.chdir(original_dir)


def test_resume_auto_find():
    """Test auto-finding progress file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            # Create a progress file
            progress1 = LabProgress(
                steps=["X", "Y"],
                lab_name="Auto Find Lab",
                persist=True
            )
            progress1.mark_done("X")
            
            # Resume without specifying file or name
            progress2 = LabProgress.resume()
            assert progress2.lab_name == "Auto Find Lab"
            assert progress2.steps["X"]['completed'] is True
            
        finally:
            os.chdir(original_dir)


def test_get_incomplete_and_current_step():
    """Test getting incomplete steps and current step."""
    progress = LabProgress(
        steps=["First", "Second", "Third", "Fourth"],
        lab_name="Step Test"
    )
    
    # Mark some as complete
    progress.mark_done("First")
    progress.mark_done("Third")
    
    # Test incomplete steps
    incomplete = progress.get_incomplete_steps()
    assert len(incomplete) == 2
    assert "Second" in incomplete
    assert "Fourth" in incomplete
    
    # Test current step (should be first incomplete)
    current = progress.get_current_step()
    assert current == "Second"
    
    # Complete all steps
    progress.mark_done("Second")
    progress.mark_done("Fourth")
    
    assert progress.get_current_step() is None
    assert len(progress.get_incomplete_steps()) == 0


def test_session_metadata():
    """Test that session metadata is saved and loaded."""
    with tempfile.TemporaryDirectory() as tmpdir:
        persist_file = os.path.join(tmpdir, "test_progress.json")
        
        # Create progress
        progress1 = LabProgress(
            steps=["Task 1"],
            lab_name="Metadata Test",
            persist=True,
            persist_file=persist_file
        )
        
        # Save session ID for comparison
        session_id = progress1._session_id
        
        # Load the saved file
        with open(persist_file, 'r') as f:
            data = json.load(f)
            assert 'session_id' in data
            assert 'last_saved' in data
            assert data['session_id'] == session_id


if __name__ == "__main__":
    test_auto_save_progress()
    test_partial_progress_with_checkpoints()
    test_resume_session()
    test_resume_with_lab_name()
    test_resume_auto_find()
    test_get_incomplete_and_current_step()
    test_session_metadata()
    print("All session resume tests passed!")