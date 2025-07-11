from IPython.display import display, HTML, clear_output
from datetime import datetime
import json
import os
import csv
from typing import List, Dict, Optional, Union
from pathlib import Path
import uuid

class LabProgress:
    """
    A comprehensive lab progress tracker for Jupyter notebooks.
    Tracks step completion, timing, scores, and provides persistence.
    """
    
    def __init__(self, steps: Union[List[str], Dict[str, dict]], lab_name: str = "Lab", 
                 persist: bool = False, persist_file: str = None, auto_save: bool = True,
                 step_metadata: Optional[Dict[str, dict]] = None):
        """
        Initialize the lab progress tracker.
        
        Args:
            steps: List of step names or dict with step details
            lab_name: Name of the lab for display
            persist: Whether to save progress to file
            persist_file: Custom file path for persistence
            auto_save: Whether to automatically save progress after each update
            step_metadata: Optional metadata for steps (tips, hints, instructions)
        """
        self.lab_name = lab_name
        self.persist = persist
        self.auto_save = auto_save
        self.persist_file = persist_file or f".{lab_name.lower().replace(' ', '_')}_progress.json"
        self._session_id = datetime.now().isoformat()
        self._student_id = str(uuid.uuid4())[:8]  # Generate short student ID
        self.step_metadata = step_metadata or {}
        self._analytics_data = []
        self._step_start_times = {}
        
        # Initialize steps
        if isinstance(steps, list):
            self.steps = {step: {
                'completed': False, 
                'timestamp': None,
                'attempts': 0,
                'score': None,
                'notes': '',
                'partial_progress': 0.0,
                'checkpoints': []
            } for step in steps}
        else:
            # Ensure all step dicts have required fields
            for step_name, step_data in steps.items():
                if 'partial_progress' not in step_data:
                    step_data['partial_progress'] = 0.0
                if 'checkpoints' not in step_data:
                    step_data['checkpoints'] = []
            self.steps = steps
            
        # Load saved progress if exists
        if persist and os.path.exists(self.persist_file):
            self._load_progress()
        
        # Ensure analytics attributes exist (in case of loading from older files)
        if not hasattr(self, '_analytics_data'):
            self._analytics_data = []
        if not hasattr(self, '_step_start_times'):
            self._step_start_times = {}
        if not hasattr(self, '_student_id'):
            self._student_id = str(uuid.uuid4())[:8]
            
        self.start_time = datetime.now()
        self._display_handle = None
        self._is_resumed = False
        self.display_progress()
    
    def mark_done(self, step: str, score: Optional[float] = None, notes: str = ''):
        """Mark a step as completed with optional score and notes."""
        if step in self.steps:
            completion_time = datetime.now()
            
            # Calculate time spent on this step
            time_spent = None
            if step in self._step_start_times:
                time_spent = (completion_time - self._step_start_times[step]).total_seconds()
            
            self.steps[step]['completed'] = True
            self.steps[step]['timestamp'] = completion_time.isoformat()
            self.steps[step]['score'] = score
            if notes:
                self.steps[step]['notes'] = notes
            
            # Record analytics data
            self._record_analytics_event(
                event_type='step_completed',
                step_name=step,
                score=score,
                time_spent=time_spent,
                notes=notes
            )
            
            if self.persist and self.auto_save:
                self._save_progress()
                
            self.display_progress()
        else:
            display(HTML(f"<div style='color: red;'>⚠️ Unknown step: {step}</div>"))
    
    def mark_partial(self, step: str, progress: float, notes: str = '', checkpoint_name: str = None):
        """Mark partial progress on a step (0.0 to 1.0)."""
        if step in self.steps:
            self.steps[step]['partial_progress'] = max(0, min(1, progress))
            if notes:
                self.steps[step]['notes'] = notes
            
            # Track step start time if this is the first interaction
            if step not in self._step_start_times and progress > 0:
                self._step_start_times[step] = datetime.now()
            
            # Add checkpoint if provided
            if checkpoint_name:
                checkpoint = {
                    'name': checkpoint_name,
                    'progress': progress,
                    'timestamp': datetime.now().isoformat()
                }
                self.steps[step]['checkpoints'].append(checkpoint)
            
            # Record analytics data
            self._record_analytics_event(
                event_type='partial_progress',
                step_name=step,
                progress=progress,
                checkpoint_name=checkpoint_name,
                notes=notes
            )
            
            if self.persist and self.auto_save:
                self._save_progress()
                
            self.display_progress()
    
    def increment_attempts(self, step: str):
        """Increment the attempt counter for a step."""
        if step in self.steps:
            self.steps[step]['attempts'] += 1
            
            # Record analytics for attempt
            self._record_analytics_event(
                event_type='attempt',
                step_name=step
            )
            
            if self.persist and self.auto_save:
                self._save_progress()
    
    def reset_step(self, step: str):
        """Reset a specific step."""
        if step in self.steps:
            self.steps[step] = {
                'completed': False,
                'timestamp': None,
                'attempts': 0,
                'score': None,
                'notes': '',
                'partial_progress': 0.0,
                'checkpoints': []
            }
            if self.persist and self.auto_save:
                self._save_progress()
            self.display_progress()
    
    def reset_all(self):
        """Reset all progress."""
        for step in self.steps:
            self.reset_step(step)
    
    def get_completion_rate(self) -> float:
        """Get overall completion percentage."""
        completed = sum(1 for s in self.steps.values() if s['completed'])
        return (completed / len(self.steps)) * 100 if self.steps else 0
    
    def get_average_score(self) -> Optional[float]:
        """Get average score across completed steps."""
        scores = [s['score'] for s in self.steps.values() 
                 if s['completed'] and s['score'] is not None]
        return sum(scores) / len(scores) if scores else None
    
    def display_progress(self, detailed: bool = False):
        """Display the current progress with visual indicators."""
        completion_rate = self.get_completion_rate()
        avg_score = self.get_average_score()
        
        # Build HTML
        html = f"""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin: 10px 0;'>
            <h3 style='color: #333; margin-bottom: 15px;'>{self.lab_name} Progress</h3>
            
            <!-- Progress Bar -->
            <div style='background-color: #e0e0e0; border-radius: 20px; height: 30px; margin-bottom: 20px;'>
                <div style='background-color: #4CAF50; height: 100%; border-radius: 20px; width: {completion_rate}%; 
                            transition: width 0.5s ease; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: white; font-weight: bold;'>{completion_rate:.1f}%</span>
                </div>
            </div>
        """
        
        if avg_score is not None:
            html += f"<p style='color: #666;'>Average Score: {avg_score:.1f}/100</p>"
        
        # Steps list
        html += "<ul style='list-style: none; padding: 0;'>"
        
        for step, info in self.steps.items():
            # Determine icon and color
            if info['completed']:
                icon = "✅"
                color = "#4CAF50"
                status = "Completed"
            elif info.get('partial_progress', 0) > 0:
                icon = "🔄"
                color = "#FF9800"
                status = f"{info['partial_progress']*100:.0f}% Complete"
            else:
                icon = "⏳"
                color = "#9E9E9E"
                status = "Pending"
            
            html += f"""
            <li style='margin: 10px 0; padding: 10px; background-color: white; 
                       border-left: 4px solid {color}; border-radius: 5px;'>
                <span style='font-size: 20px; margin-right: 10px;'>{icon}</span>
                <strong>{step}</strong> - <span style='color: {color};'>{status}</span>
            """
            
            if detailed:
                if info['timestamp']:
                    html += f"<br><small style='color: #666;'>Completed: {info['timestamp']}</small>"
                if info['attempts'] > 0:
                    html += f"<br><small style='color: #666;'>Attempts: {info['attempts']}</small>"
                if info['score'] is not None:
                    html += f"<br><small style='color: #666;'>Score: {info['score']}/100</small>"
                if info['notes']:
                    html += f"<br><small style='color: #666;'>Notes: {info['notes']}</small>"
            
            html += "</li>"
        
        html += "</ul>"
        
        # Summary
        elapsed = datetime.now() - self.start_time
        html += f"""
        <div style='margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd;'>
            <small style='color: #666;'>
                Time Elapsed: {str(elapsed).split('.')[0]} | 
                Steps Completed: {sum(1 for s in self.steps.values() if s['completed'])}/{len(self.steps)}
            </small>
        </div>
        </div>
        """
        
        # Use clear_output to update in place
        if self._display_handle:
            clear_output(wait=True)
        
        self._display_handle = display(HTML(html))
    
    def _save_progress(self):
        """Save progress to file."""
        data = {
            'lab_name': self.lab_name,
            'steps': self.steps,
            'start_time': self.start_time.isoformat(),
            'session_id': self._session_id,
            'student_id': self._student_id,
            'last_saved': datetime.now().isoformat(),
            'step_metadata': self.step_metadata,
            'analytics_data': self._analytics_data,
            'step_start_times': {k: v.isoformat() for k, v in self._step_start_times.items()}
        }
        with open(self.persist_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_progress(self):
        """Load progress from file."""
        try:
            with open(self.persist_file, 'r') as f:
                data = json.load(f)
                self.steps = data['steps']
                self.start_time = datetime.fromisoformat(data['start_time'])
                self._is_resumed = True
                if 'session_id' in data:
                    self._previous_session_id = data['session_id']
                if 'student_id' in data:
                    self._student_id = data['student_id']
                if 'step_metadata' in data:
                    self.step_metadata = data['step_metadata']
                if 'analytics_data' in data:
                    self._analytics_data = data['analytics_data']
                if 'step_start_times' in data:
                    self._step_start_times = {k: datetime.fromisoformat(v) for k, v in data['step_start_times'].items()}
        except Exception as e:
            print(f"Could not load saved progress: {e}")
    
    @classmethod
    def resume(cls, lab_name: str = None, persist_file: str = None) -> 'LabProgress':
        """
        Resume a lab from saved progress.
        
        Args:
            lab_name: Name of the lab (used to find default persist file)
            persist_file: Custom file path for persistence
            
        Returns:
            LabProgress instance with restored state
        """
        if not persist_file and not lab_name:
            # Try to find any progress file in current directory
            progress_files = list(Path('.').glob('.*.json'))
            if progress_files:
                persist_file = str(progress_files[0])
                print(f"Found progress file: {persist_file}")
            else:
                raise ValueError("No progress file found. Provide lab_name or persist_file.")
        
        if not persist_file:
            persist_file = f".{lab_name.lower().replace(' ', '_')}_progress.json"
        
        if not os.path.exists(persist_file):
            raise FileNotFoundError(f"No saved progress found at: {persist_file}")
        
        # Load the saved data to get lab name and steps
        with open(persist_file, 'r') as f:
            data = json.load(f)
        
        # Create instance with saved data
        instance = cls(
            steps=data['steps'],
            lab_name=data['lab_name'],
            persist=True,
            persist_file=persist_file
        )
        
        # Show resume message
        incomplete_steps = [s for s, info in instance.steps.items() 
                          if not info['completed']]
        
        resume_msg = f"""
        <div style='background-color: #e3f2fd; padding: 15px; border-radius: 8px; 
                    border-left: 4px solid #2196F3; margin: 10px 0;'>
            <strong>📂 Session Resumed!</strong><br>
            Lab: {instance.lab_name}<br>
            Progress: {instance.get_completion_rate():.1f}% complete<br>
            {len(incomplete_steps)} steps remaining
        </div>
        """
        display(HTML(resume_msg))
        
        return instance
    
    def get_incomplete_steps(self) -> List[str]:
        """Get list of incomplete steps."""
        return [step for step, info in self.steps.items() if not info['completed']]
    
    def get_current_step(self) -> Optional[str]:
        """Get the first incomplete step (current step to work on)."""
        incomplete = self.get_incomplete_steps()
        return incomplete[0] if incomplete else None
    
    def show_step_tips(self, step: str = None):
        """Display tips and guidance for a specific step or current step."""
        from .display import show_step_guidance, show_info
        
        if step is None:
            step = self.get_current_step()
            if not step:
                show_info("All steps completed! 🎉", title="Congratulations")
                return
        
        if step not in self.steps:
            show_info(f"Step '{step}' not found", title="Error")
            return
        
        # Get metadata for this step
        metadata = self.step_metadata.get(step, {})
        
        if not metadata:
            show_info(f"No tips available for step: {step}", title="Step Info")
            return
        
        # Display comprehensive guidance
        show_step_guidance(
            step_name=step,
            instructions=metadata.get('instructions', f"Complete the '{step}' step"),
            tips=metadata.get('tips'),
            hints=metadata.get('hints'),
            common_mistakes=metadata.get('common_mistakes')
        )
    
    def set_step_metadata(self, step: str, metadata: dict):
        """Set or update metadata for a specific step."""
        if step in self.steps:
            self.step_metadata[step] = metadata
            if self.persist and self.auto_save:
                self._save_progress()
    
    def export_report(self) -> str:
        """Export a text report of the progress."""
        report = f"Lab Progress Report: {self.lab_name}\n"
        report += "=" * 50 + "\n\n"
        report += f"Completion Rate: {self.get_completion_rate():.1f}%\n"
        
        avg_score = self.get_average_score()
        if avg_score:
            report += f"Average Score: {avg_score:.1f}/100\n"
        
        report += f"\nSteps:\n"
        for step, info in self.steps.items():
            status = "✅ Completed" if info['completed'] else "⏳ Pending"
            report += f"- {step}: {status}\n"
            if info['score'] is not None:
                report += f"  Score: {info['score']}/100\n"
            if info['attempts'] > 0:
                report += f"  Attempts: {info['attempts']}\n"
        
        return report
    
    def _record_analytics_event(self, event_type: str, step_name: str = None, **kwargs):
        """Record an analytics event."""
        # Ensure analytics attributes exist
        if not hasattr(self, '_analytics_data'):
            self._analytics_data = []
        if not hasattr(self, '_student_id'):
            self._student_id = str(uuid.uuid4())[:8]
        if not hasattr(self, '_session_id'):
            self._session_id = datetime.now().isoformat()
            
        event = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self._session_id,
            'student_id': self._student_id,
            'lab_name': self.lab_name,
            'event_type': event_type,
            'step_name': step_name,
            **kwargs
        }
        self._analytics_data.append(event)
    
    def export_analytics_csv(self, filename: str = None) -> str:
        """Export analytics data to CSV format."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.lab_name.lower().replace(' ', '_')}_analytics_{timestamp}.csv"
        
        # Ensure analytics data exists
        if not hasattr(self, '_analytics_data') or not self._analytics_data:
            return filename
        
        # Get all unique keys from all events
        all_keys = set()
        for event in self._analytics_data:
            all_keys.update(event.keys())
        
        fieldnames = sorted(all_keys)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self._analytics_data)
        
        return filename
    
    def export_analytics_json(self, filename: str = None) -> str:
        """Export analytics data to JSON format."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.lab_name.lower().replace(' ', '_')}_analytics_{timestamp}.json"
        
        analytics_export = {
            'lab_name': self.lab_name,
            'session_id': self._session_id,
            'student_id': self._student_id,
            'export_timestamp': datetime.now().isoformat(),
            'summary': self.get_analytics_summary(),
            'events': self._analytics_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analytics_export, f, indent=2)
        
        return filename
    
    def get_analytics_summary(self) -> Dict:
        """Get a summary of analytics data."""
        # Ensure analytics data exists
        if not hasattr(self, '_analytics_data') or not self._analytics_data:
            return {}
        
        summary = {
            'total_events': len(self._analytics_data),
            'session_duration': None,
            'steps_completed': sum(1 for s in self.steps.values() if s['completed']),
            'total_steps': len(self.steps),
            'completion_rate': self.get_completion_rate(),
            'average_score': self.get_average_score(),
            'total_attempts': sum(s['attempts'] for s in self.steps.values()),
            'event_types': {},
            'step_analytics': {}
        }
        
        # Calculate session duration
        if self._analytics_data:
            start_time = datetime.fromisoformat(self._analytics_data[0]['timestamp'])
            end_time = datetime.fromisoformat(self._analytics_data[-1]['timestamp'])
            summary['session_duration'] = (end_time - start_time).total_seconds()
        
        # Count event types
        for event in self._analytics_data:
            event_type = event['event_type']
            summary['event_types'][event_type] = summary['event_types'].get(event_type, 0) + 1
        
        # Step-level analytics
        for step_name, step_data in self.steps.items():
            step_events = [e for e in self._analytics_data if e.get('step_name') == step_name]
            
            summary['step_analytics'][step_name] = {
                'completed': step_data['completed'],
                'attempts': step_data['attempts'],
                'score': step_data['score'],
                'total_events': len(step_events),
                'time_spent': None
            }
            
            # Calculate time spent on step
            if step_name in self._step_start_times and step_data['completed']:
                start_time = self._step_start_times[step_name]
                end_time = datetime.fromisoformat(step_data['timestamp'])
                summary['step_analytics'][step_name]['time_spent'] = (end_time - start_time).total_seconds()
        
        return summary
    
    def display_analytics_dashboard(self):
        """Display an analytics dashboard with key metrics."""
        from .display import show_info, show_table
        
        summary = self.get_analytics_summary()
        
        if not summary:
            show_info("No analytics data available yet.")
            return
        
        # Create metrics table
        metrics = [
            ["Total Events", summary['total_events']],
            ["Session Duration", f"{summary['session_duration']:.0f} seconds" if summary['session_duration'] else "N/A"],
            ["Steps Completed", f"{summary['steps_completed']}/{summary['total_steps']}"],
            ["Completion Rate", f"{summary['completion_rate']:.1f}%"],
            ["Average Score", f"{summary['average_score']:.1f}" if summary['average_score'] else "N/A"],
            ["Total Attempts", summary['total_attempts']]
        ]
        
        show_table(["Metric", "Value"], metrics, title="📊 Lab Analytics Dashboard")
        
        # Event types breakdown
        if summary['event_types']:
            event_data = [[event_type, count] for event_type, count in summary['event_types'].items()]
            show_table(["Event Type", "Count"], event_data, title="Event Types Breakdown")
        
        # Step performance
        step_data = []
        for step_name, step_info in summary['step_analytics'].items():
            time_str = f"{step_info['time_spent']:.0f}s" if step_info['time_spent'] else "N/A"
            score_str = str(step_info['score']) if step_info['score'] is not None else "N/A"
            status = "✅" if step_info['completed'] else "⏳"
            
            step_data.append([
                step_name, 
                status, 
                step_info['attempts'], 
                score_str, 
                time_str
            ])
        
        show_table(
            ["Step", "Status", "Attempts", "Score", "Time"], 
            step_data, 
            title="Step Performance"
        )
    
    # Shell Step functionality
    def run_shell_step(self, step_name: str, command: str, 
                       expected_output: Optional[str] = None,
                       timeout: int = 30,
                       working_dir: Optional[str] = None,
                       auto_mark_complete: bool = True,
                       show_output: bool = True) -> bool:
        """
        Execute a shell command as part of a lab step with styled output.
        
        Args:
            step_name: Name of the step to track
            command: Shell command to execute
            expected_output: Optional string that should be in the output for success
            timeout: Command timeout in seconds
            working_dir: Optional working directory for the command
            auto_mark_complete: Whether to auto-mark step complete on success
            show_output: Whether to display the command output
            
        Returns:
            Boolean indicating if command was successful
        """
        import subprocess
        import os
        import time
        
        # Record step start
        if step_name not in self._step_start_times:
            self._step_start_times[step_name] = datetime.now()
        
        # Display command header
        if show_output:
            self._display_shell_header(step_name, command, working_dir)
        
        try:
            # Set up the environment
            env = os.environ.copy()
            cwd = working_dir if working_dir else os.getcwd()
            
            # Execute the command
            start_time = time.time()
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=env
            )
            
            execution_time = time.time() - start_time
            
            # Check success criteria
            success = result.returncode == 0
            if expected_output and success:
                success = expected_output in result.stdout
            
            # Display results
            if show_output:
                self._display_shell_result(
                    command=command,
                    returncode=result.returncode,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    execution_time=execution_time,
                    success=success,
                    expected_output=expected_output
                )
            
            # Record analytics
            self._record_analytics_event(
                event_type='shell_command',
                step_name=step_name,
                command=command,
                returncode=result.returncode,
                execution_time=execution_time,
                success=success,
                working_dir=cwd
            )
            
            # Auto-mark step complete if successful
            if success and auto_mark_complete and step_name in self.steps:
                self.mark_done(step_name, score=100, notes=f"Shell command executed successfully")
                if show_output:
                    self.display_progress()
            elif not success and step_name in self.steps:
                # Increment attempts
                self.steps[step_name]['attempts'] += 1
                if self.persist and self.auto_save:
                    self._save_progress()
            
            return success
            
        except subprocess.TimeoutExpired:
            if show_output:
                self._display_shell_timeout(command, timeout)
            
            self._record_analytics_event(
                event_type='shell_timeout',
                step_name=step_name,
                command=command,
                timeout=timeout
            )
            
            return False
            
        except Exception as e:
            if show_output:
                self._display_shell_error(command, str(e))
            
            self._record_analytics_event(
                event_type='shell_error',
                step_name=step_name,
                command=command,
                error=str(e)
            )
            
            return False
    
    def _display_shell_header(self, step_name: str, command: str, working_dir: Optional[str]):
        """Display shell command header."""
        cwd_display = working_dir if working_dir else os.getcwd()
        
        html = f"""
        <div style='background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #dee2e6; font-family: monospace;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 20px; margin-right: 10px;'>🖥️</span>
                <strong style='color: #495057; font-size: 16px;'>Executing Shell Command: {step_name}</strong>
            </div>
            <div style='background-color: #343a40; color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <div style='color: #6f42c1; font-size: 12px; margin-bottom: 5px;'>📁 {cwd_display}</div>
                <div style='color: #28a745; font-weight: bold;'>$ {command}</div>
            </div>
        """
        
        display(HTML(html))
    
    def _display_shell_result(self, command: str, returncode: int, stdout: str, stderr: str,
                             execution_time: float, success: bool, expected_output: Optional[str]):
        """Display shell command results with styling."""
        
        # Determine status styling
        if success:
            status_color = "#28a745"
            status_icon = "✅"
            status_text = "SUCCESS"
            border_color = "#28a745"
        else:
            status_color = "#dc3545"
            status_icon = "❌"
            status_text = "FAILED"
            border_color = "#dc3545"
        
        html = f"""
        <div style='background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid {border_color}; font-family: monospace;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                <div>
                    <span style='font-size: 18px; margin-right: 8px;'>{status_icon}</span>
                    <strong style='color: {status_color}; font-size: 16px;'>{status_text}</strong>
                </div>
                <div style='color: #6c757d; font-size: 14px;'>
                    Exit Code: {returncode} | Time: {execution_time:.2f}s
                </div>
            </div>
        """
        
        # Show stdout if present
        if stdout.strip():
            # Truncate very long output
            display_stdout = stdout[:2000] + "..." if len(stdout) > 2000 else stdout
            html += f"""
            <div style='margin-bottom: 10px;'>
                <div style='color: #495057; font-weight: bold; margin-bottom: 5px;'>📤 Output:</div>
                <div style='background-color: #ffffff; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; max-height: 200px; overflow-y: auto; white-space: pre-wrap; font-size: 12px;'>{display_stdout}</div>
            </div>
            """
        
        # Show stderr if present
        if stderr.strip():
            display_stderr = stderr[:1000] + "..." if len(stderr) > 1000 else stderr
            html += f"""
            <div style='margin-bottom: 10px;'>
                <div style='color: #dc3545; font-weight: bold; margin-bottom: 5px;'>⚠️ Error Output:</div>
                <div style='background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; max-height: 150px; overflow-y: auto; white-space: pre-wrap; font-size: 12px; color: #721c24;'>{display_stderr}</div>
            </div>
            """
        
        # Show expected output check if applicable
        if expected_output:
            found = expected_output in stdout
            check_icon = "✅" if found else "❌"
            check_color = "#28a745" if found else "#dc3545"
            html += f"""
            <div style='margin-bottom: 10px;'>
                <div style='color: #495057; font-weight: bold; margin-bottom: 5px;'>🔍 Expected Output Check:</div>
                <div style='background-color: #e9ecef; padding: 8px; border-radius: 5px; font-size: 12px;'>
                    Looking for: <code>{expected_output}</code>
                    <span style='color: {check_color}; margin-left: 10px;'>{check_icon} {"Found" if found else "Not found"}</span>
                </div>
            </div>
            """
        
        html += "</div>"
        display(HTML(html))
    
    def _display_shell_timeout(self, command: str, timeout: int):
        """Display timeout message."""
        html = f"""
        <div style='background-color: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ffc107; font-family: monospace;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 18px; margin-right: 8px;'>⏰</span>
                <strong style='color: #856404; font-size: 16px;'>TIMEOUT</strong>
            </div>
            <div style='color: #856404;'>
                Command timed out after {timeout} seconds:<br>
                <code>{command}</code>
            </div>
        </div>
        """
        display(HTML(html))
    
    def _display_shell_error(self, command: str, error: str):
        """Display error message."""
        html = f"""
        <div style='background-color: #f8d7da; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #dc3545; font-family: monospace;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 18px; margin-right: 8px;'>💥</span>
                <strong style='color: #721c24; font-size: 16px;'>EXECUTION ERROR</strong>
            </div>
            <div style='color: #721c24;'>
                Error executing command: <code>{command}</code><br>
                <strong>Error:</strong> {error}
            </div>
        </div>
        """
        display(HTML(html))
    
    def run_shell_sequence(self, step_name: str, commands: List[str],
                          working_dir: Optional[str] = None,
                          stop_on_error: bool = True,
                          timeout_per_command: int = 30) -> bool:
        """
        Execute a sequence of shell commands for a lab step.
        
        Args:
            step_name: Name of the step to track
            commands: List of shell commands to execute in sequence
            working_dir: Optional working directory for all commands
            stop_on_error: Whether to stop sequence on first error
            timeout_per_command: Timeout for each individual command
            
        Returns:
            Boolean indicating if all commands were successful
        """
        
        # Display sequence header
        html = f"""
        <div style='background-color: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #1976d2;'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 20px; margin-right: 10px;'>🔄</span>
                <strong style='color: #1976d2; font-size: 16px;'>Shell Command Sequence: {step_name}</strong>
            </div>
            <div style='color: #1976d2; font-size: 14px;'>
                Executing {len(commands)} commands | Stop on error: {"Yes" if stop_on_error else "No"}
            </div>
        </div>
        """
        display(HTML(html))
        
        all_successful = True
        successful_count = 0
        
        for i, command in enumerate(commands, 1):
            # Display command number
            display(HTML(f"""
            <div style='color: #6c757d; font-weight: bold; margin: 10px 0;'>
                Command {i}/{len(commands)}:
            </div>
            """))
            
            # Execute the command (but don't auto-complete the step yet)
            success = self.run_shell_step(
                step_name=f"{step_name}_cmd_{i}",  # Temporary step name
                command=command,
                working_dir=working_dir,
                timeout=timeout_per_command,
                auto_mark_complete=False,  # Don't auto-complete individual commands
                show_output=True
            )
            
            if success:
                successful_count += 1
            else:
                all_successful = False
                if stop_on_error:
                    break
        
        # Display sequence summary
        if all_successful:
            summary_color = "#28a745"
            summary_icon = "✅"
            summary_text = "SEQUENCE COMPLETED"
        else:
            summary_color = "#dc3545"
            summary_icon = "❌"
            summary_text = "SEQUENCE FAILED"
        
        html = f"""
        <div style='background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid {summary_color};'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='font-size: 18px; margin-right: 8px;'>{summary_icon}</span>
                    <strong style='color: {summary_color}; font-size: 16px;'>{summary_text}</strong>
                </div>
                <div style='color: #6c757d;'>
                    Success: {successful_count}/{len(commands)}
                </div>
            </div>
        </div>
        """
        display(HTML(html))
        
        # Mark the main step complete if all successful
        if all_successful and step_name in self.steps:
            self.mark_done(step_name, score=100, notes=f"All {len(commands)} shell commands executed successfully")
            self.display_progress()
        elif step_name in self.steps:
            # Update attempts and partial progress
            self.steps[step_name]['attempts'] += 1
            self.steps[step_name]['partial_progress'] = (successful_count / len(commands)) * 100
            if self.persist and self.auto_save:
                self._save_progress()
        
        return all_successful