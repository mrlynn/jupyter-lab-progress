from typing import Any, Callable, Optional, List, Dict, Union
import re
import inspect
from IPython.display import display, HTML
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime

class LabValidator:
    """
    Comprehensive validation class for Jupyter lab exercises.
    Provides a variety of validation methods with visual feedback.
    """
    
    def __init__(self, progress_tracker=None):
        """
        Initialize the validator.
        
        Args:
            progress_tracker: Optional LabProgress instance to auto-update on successful validations
        """
        self.progress_tracker = progress_tracker
        self.last_validation_result = None
        self.scoring_rules = {}
        self.validation_history = []
    
    def _display_result(self, success: bool, message: str, details: str = ""):
        """Display validation result with color-coded output."""
        if success:
            icon = "✅"
            color = "#4CAF50"
            bg_color = "#e8f5e9"
        else:
            icon = "❌"
            color = "#f44336"
            bg_color = "#ffebee"
        
        html = f"""
        <div style='background-color: {bg_color}; border-left: 4px solid {color}; 
                    padding: 10px; margin: 10px 0; border-radius: 5px;'>
            <span style='font-size: 20px; margin-right: 10px;'>{icon}</span>
            <strong style='color: {color};'>{message}</strong>
            {f"<br><small style='color: #666;'>{details}</small>" if details else ""}
        </div>
        """
        display(HTML(html))
        self.last_validation_result = success
        return success
    
    def validate_variable_exists(self, var_name: str, globals_dict: dict, 
                                expected_type: Optional[type] = None) -> bool:
        """
        Validate that a variable exists in the namespace.
        
        Args:
            var_name: Name of the variable to check
            globals_dict: Usually globals() from the notebook
            expected_type: Optional type to check against
        """
        if var_name not in globals_dict:
            return self._display_result(False, f"Variable '{var_name}' not found", 
                                      "Make sure you've run the cell that creates this variable.")
        
        if expected_type:
            actual_type = type(globals_dict[var_name])
            if not isinstance(globals_dict[var_name], expected_type):
                return self._display_result(False, f"Type mismatch for '{var_name}'", 
                                          f"Expected {expected_type.__name__}, got {actual_type.__name__}")
        
        return self._display_result(True, f"Variable '{var_name}' validated successfully")
    
    def validate_function_exists(self, func_name: str, globals_dict: dict,
                               expected_params: Optional[List[str]] = None) -> bool:
        """
        Validate that a function exists and has expected parameters.
        
        Args:
            func_name: Name of the function
            globals_dict: Usually globals() from the notebook
            expected_params: Optional list of expected parameter names
        """
        if func_name not in globals_dict:
            return self._display_result(False, f"Function '{func_name}' not found",
                                      "Make sure you've defined this function.")
        
        obj = globals_dict[func_name]
        if not callable(obj):
            return self._display_result(False, f"'{func_name}' is not callable",
                                      f"Found {type(obj).__name__} instead of a function.")
        
        if expected_params:
            sig = inspect.signature(obj)
            actual_params = list(sig.parameters.keys())
            missing = set(expected_params) - set(actual_params)
            if missing:
                return self._display_result(False, f"Missing parameters in '{func_name}'",
                                          f"Expected: {expected_params}, Missing: {list(missing)}")
        
        return self._display_result(True, f"Function '{func_name}' validated successfully")
    
    def validate_output(self, actual: Any, expected: Any, 
                       comparison_func: Optional[Callable] = None,
                       tolerance: float = 1e-6) -> bool:
        """
        Validate that output matches expected value.
        
        Args:
            actual: The actual output
            expected: The expected output
            comparison_func: Optional custom comparison function
            tolerance: Tolerance for float comparisons
        """
        if comparison_func:
            match = comparison_func(actual, expected)
        elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            match = abs(actual - expected) < tolerance
        elif isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
            match = np.allclose(actual, expected, atol=tolerance)
        else:
            match = actual == expected
        
        if match:
            return self._display_result(True, "Output matches expected value")
        else:
            return self._display_result(False, "Output does not match expected value",
                                      f"Expected: {expected}, Got: {actual}")
    
    def validate_dataframe(self, df: Any, expected_shape: Optional[tuple] = None,
                          expected_columns: Optional[List[str]] = None,
                          expected_dtypes: Optional[Dict[str, type]] = None,
                          show_preview: bool = True,
                          show_histograms: bool = False,
                          histogram_columns: Optional[List[str]] = None) -> bool:
        """
        Validate pandas DataFrame properties with enhanced visual feedback.
        
        Args:
            df: The dataframe to validate
            expected_shape: Expected (rows, cols) tuple
            expected_columns: Expected column names
            expected_dtypes: Expected column data types
            show_preview: Whether to show df.head() preview
            show_histograms: Whether to show histograms for numeric columns
            histogram_columns: Specific columns to show histograms for
        """
        if not isinstance(df, pd.DataFrame):
            return self._display_result(False, "Not a DataFrame",
                                      f"Got {type(df).__name__} instead")
        
        issues = []
        
        if expected_shape and df.shape != expected_shape:
            issues.append(f"Shape mismatch: expected {expected_shape}, got {df.shape}")
        
        if expected_columns:
            missing_cols = set(expected_columns) - set(df.columns)
            if missing_cols:
                issues.append(f"Missing columns: {missing_cols}")
        
        if expected_dtypes:
            for col, expected_type in expected_dtypes.items():
                if col in df.columns and not df[col].dtype == expected_type:
                    issues.append(f"Column '{col}' has wrong dtype: expected {expected_type}, got {df[col].dtype}")
        
        # Show validation result first
        if issues:
            success = self._display_result(False, "DataFrame validation failed", "; ".join(issues))
        else:
            success = self._display_result(True, "DataFrame validated successfully")
        
        # Show enhanced visuals if requested
        if show_preview or show_histograms:
            self._display_dataframe_visuals(df, show_preview, show_histograms, histogram_columns)
        
        return success
    
    def check_embedding_shape(self, embedding: Any, expected_dim: int) -> bool:
        """Check if embedding has correct dimensions."""
        try:
            if hasattr(embedding, '__len__'):
                actual_dim = len(embedding)
            elif hasattr(embedding, 'shape'):
                actual_dim = embedding.shape[-1]
            else:
                return self._display_result(False, "Invalid embedding format",
                                          "Embedding should be a list or array")
            
            if actual_dim != expected_dim:
                return self._display_result(False, f"Embedding dimension mismatch",
                                          f"Expected {expected_dim}, got {actual_dim}")
            
            return self._display_result(True, f"Embedding shape is correct: {actual_dim}")
        except Exception as e:
            return self._display_result(False, "Error checking embedding shape", str(e))
    
    def assert_in_dataframe(self, df: Any, column: str, value: Any) -> bool:
        """Check if a value exists in a dataframe column."""
        if not isinstance(df, pd.DataFrame):
            return self._display_result(False, "Not a DataFrame",
                                      f"Got {type(df).__name__} instead")
        
        if column not in df.columns:
            return self._display_result(False, f"Column '{column}' not found",
                                      f"Available columns: {list(df.columns)}")
        
        if value not in df[column].values:
            return self._display_result(False, f"Value not found in column '{column}'",
                                      f"Looking for: {value}")
        
        return self._display_result(True, f"Found {value} in {column}")
    
    def validate_file_exists(self, filepath: str) -> bool:
        """Validate that a file exists."""
        import os
        if not os.path.exists(filepath):
            return self._display_result(False, f"File not found: {filepath}",
                                      "Make sure the file path is correct")
        
        return self._display_result(True, f"File exists: {filepath}")
    
    def validate_string_pattern(self, text: str, pattern: str, 
                              description: str = "pattern") -> bool:
        """Validate that a string matches a regex pattern."""
        if re.match(pattern, text):
            return self._display_result(True, f"Text matches {description}")
        else:
            return self._display_result(False, f"Text does not match {description}",
                                      f"Pattern: {pattern}")
    
    def validate_range(self, value: Union[int, float], min_val: Optional[float] = None, 
                      max_val: Optional[float] = None) -> bool:
        """Validate that a value is within a specified range."""
        if min_val is not None and value < min_val:
            return self._display_result(False, f"Value {value} is below minimum",
                                      f"Minimum allowed: {min_val}")
        
        if max_val is not None and value > max_val:
            return self._display_result(False, f"Value {value} is above maximum",
                                      f"Maximum allowed: {max_val}")
        
        return self._display_result(True, f"Value {value} is within valid range")
    
    def validate_list_items(self, lst: List[Any], 
                          validator_func: Callable[[Any], bool],
                          description: str = "validation") -> bool:
        """Validate all items in a list using a custom function."""
        if not isinstance(lst, list):
            return self._display_result(False, "Not a list",
                                      f"Got {type(lst).__name__} instead")
        
        invalid_items = []
        for i, item in enumerate(lst):
            try:
                if not validator_func(item):
                    invalid_items.append((i, item))
            except Exception as e:
                invalid_items.append((i, f"Error: {e}"))
        
        if invalid_items:
            details = f"Failed items: {invalid_items[:3]}{'...' if len(invalid_items) > 3 else ''}"
            return self._display_result(False, f"List {description} failed", details)
        
        return self._display_result(True, f"All {len(lst)} items passed {description}")
    
    def validate_custom(self, condition: bool, success_msg: str, 
                       failure_msg: str, details: str = "") -> bool:
        """Generic validation with custom condition and messages."""
        if condition:
            return self._display_result(True, success_msg)
        else:
            return self._display_result(False, failure_msg, details)
    
    def validate_and_mark_complete(self, step_name: str, condition: bool,
                                 success_msg: str = "Step completed!",
                                 failure_msg: str = "Step not yet complete") -> bool:
        """
        Validate a condition and automatically mark progress if validator has progress_tracker.
        
        Args:
            step_name: Name of the step in progress tracker
            condition: Boolean condition to validate
            success_msg: Message to show on success
            failure_msg: Message to show on failure
        """
        result = self.validate_custom(condition, success_msg, failure_msg)
        
        if result and self.progress_tracker:
            self.progress_tracker.mark_done(step_name)
        
        return result
    
    def create_step_validator(self, step_name: str) -> Callable:
        """
        Create a validator function tied to a specific step.
        
        Returns a function that when called with a condition, validates and marks progress.
        """
        def validator(condition: bool, success_msg: str = f"{step_name} completed!",
                     failure_msg: str = f"{step_name} not yet complete"):
            return self.validate_and_mark_complete(step_name, condition, success_msg, failure_msg)
        
        return validator
    
    def add_scoring_rule(self, name: str, weight: float, 
                        checker: Union[Callable, Dict[str, Any]], 
                        description: str = "", 
                        partial_credit: bool = True):
        """
        Add a scoring rule for auto-grading.
        
        Args:
            name: Unique name for the rule
            weight: Weight of this rule (0.0 to 1.0, all weights should sum to 1.0)
            checker: Either a callable that returns (bool, score) or dict with validation params
            description: Human-readable description of what's being checked
            partial_credit: Whether to allow partial scores (0-100) or just pass/fail
        """
        self.scoring_rules[name] = {
            'weight': weight,
            'checker': checker,
            'description': description,
            'partial_credit': partial_credit,
            'last_score': None,
            'last_result': None
        }
    
    def validate_with_score(self, rule_name: str, *args, **kwargs) -> tuple:
        """
        Run a validation and return both success status and score.
        
        Returns:
            Tuple of (success: bool, score: float 0-100)
        """
        if rule_name not in self.scoring_rules:
            return False, 0
        
        rule = self.scoring_rules[rule_name]
        checker = rule['checker']
        
        try:
            if callable(checker):
                result = checker(*args, **kwargs)
                if isinstance(result, tuple):
                    success, score = result
                else:
                    success = result
                    score = 100 if success else 0
            else:
                # Dictionary-based validation
                success = self._run_dict_validation(checker, *args, **kwargs)
                score = 100 if success else 0
            
            # Apply partial credit rules
            if not rule['partial_credit']:
                score = 100 if success else 0
            
            # Store result
            rule['last_score'] = score
            rule['last_result'] = success
            
            # Add to history
            self.validation_history.append({
                'rule': rule_name,
                'score': score,
                'success': success,
                'timestamp': pd.Timestamp.now()
            })
            
            return success, score
            
        except Exception as e:
            rule['last_score'] = 0
            rule['last_result'] = False
            return False, 0
    
    def _run_dict_validation(self, config: dict, *args, **kwargs) -> bool:
        """Run validation based on dictionary configuration."""
        val_type = config.get('type', 'custom')
        
        if val_type == 'variable_exists':
            return self.validate_variable_exists(
                config['var_name'], 
                kwargs.get('globals_dict', globals()),
                config.get('expected_type')
            )
        elif val_type == 'output_match':
            return self.validate_output(
                kwargs.get('actual'),
                config.get('expected'),
                tolerance=config.get('tolerance', 1e-6)
            )
        elif val_type == 'dataframe':
            return self.validate_dataframe(
                kwargs.get('df'),
                min_rows=config.get('min_rows'),
                required_columns=config.get('required_columns')
            )
        else:
            return False
    
    def run_auto_grading(self, globals_dict: dict = None, verbose: bool = True) -> Dict[str, Any]:
        """
        Run all scoring rules and generate a grade report.
        
        Args:
            globals_dict: Global namespace (usually globals() from notebook)
            verbose: Whether to display detailed results
            
        Returns:
            Dictionary with overall score and detailed results
        """
        if globals_dict is None:
            globals_dict = globals()
        
        results = {}
        total_score = 0
        total_weight = 0
        
        # Display header
        if verbose:
            display(HTML("""
            <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: #333; margin-bottom: 15px;'>🎯 Auto-Grading Results</h3>
            """))
        
        for rule_name, rule in self.scoring_rules.items():
            # Run the validation
            success, score = self.validate_with_score(rule_name, globals_dict=globals_dict)
            
            # Calculate weighted score
            weighted_score = score * rule['weight']
            total_score += weighted_score
            total_weight += rule['weight']
            
            results[rule_name] = {
                'score': score,
                'weighted_score': weighted_score,
                'weight': rule['weight'],
                'success': success,
                'description': rule['description']
            }
            
            # Display individual result
            if verbose:
                self._display_grading_result(rule_name, rule, score, weighted_score)
        
        # Calculate final grade
        if total_weight > 0:
            final_score = (total_score / total_weight)
        else:
            final_score = 0
        
        # Display summary
        if verbose:
            self._display_grading_summary(final_score, total_weight)
            display(HTML("</div>"))
        
        # Update progress tracker if available
        if self.progress_tracker and hasattr(self.progress_tracker, 'set_overall_score'):
            self.progress_tracker.set_overall_score(final_score)
        
        return {
            'final_score': final_score,
            'total_weight': total_weight,
            'detailed_results': results,
            'timestamp': pd.Timestamp.now().isoformat()
        }
    
    def _display_grading_result(self, name: str, rule: dict, score: float, weighted_score: float):
        """Display individual grading result."""
        color = "#4CAF50" if score >= 70 else "#FF9800" if score >= 40 else "#f44336"
        icon = "✅" if score >= 70 else "⚠️" if score >= 40 else "❌"
        
        html = f"""
        <div style='background-color: white; padding: 10px; margin: 5px 0; 
                    border-left: 4px solid {color}; border-radius: 5px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='font-size: 16px; margin-right: 8px;'>{icon}</span>
                    <strong>{name}</strong>
                    {f" - {rule['description']}" if rule['description'] else ""}
                </div>
                <div style='text-align: right;'>
                    <span style='color: {color}; font-weight: bold;'>{score:.0f}%</span>
                    <small style='color: #666;'> (weight: {rule['weight']:.1%})</small>
                </div>
            </div>
        </div>
        """
        display(HTML(html))
    
    def _display_grading_summary(self, final_score: float, total_weight: float):
        """Display grading summary."""
        grade = self._score_to_grade(final_score)
        color = "#4CAF50" if final_score >= 70 else "#FF9800" if final_score >= 40 else "#f44336"
        
        html = f"""
        <div style='margin-top: 20px; padding: 15px; background-color: #e3f2fd; 
                    border-radius: 8px; text-align: center;'>
            <h4 style='margin: 0; color: #1976d2;'>Final Score</h4>
            <div style='font-size: 48px; font-weight: bold; color: {color}; margin: 10px 0;'>
                {final_score:.0f}%
            </div>
            <div style='font-size: 24px; color: #666;'>Grade: {grade}</div>
            <small style='color: #999;'>Total weight: {total_weight:.1%}</small>
        </div>
        """
        display(HTML(html))
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 93: return "A"
        elif score >= 90: return "A-"
        elif score >= 87: return "B+"
        elif score >= 83: return "B"
        elif score >= 80: return "B-"
        elif score >= 77: return "C+"
        elif score >= 73: return "C"
        elif score >= 70: return "C-"
        elif score >= 67: return "D+"
        elif score >= 63: return "D"
        elif score >= 60: return "D-"
        else: return "F"
    
    def export_grading_report(self, filename: str = None) -> str:
        """Export grading results to a file or return as string."""
        report = "Lab Auto-Grading Report\n"
        report += "=" * 50 + "\n\n"
        
        # Get latest results
        results = self.run_auto_grading(verbose=False)
        
        report += f"Final Score: {results['final_score']:.1f}%\n"
        report += f"Grade: {self._score_to_grade(results['final_score'])}\n"
        report += f"Timestamp: {results['timestamp']}\n\n"
        
        report += "Detailed Results:\n"
        report += "-" * 30 + "\n"
        
        for rule_name, detail in results['detailed_results'].items():
            report += f"\n{rule_name}:\n"
            report += f"  Score: {detail['score']:.0f}%\n"
            report += f"  Weight: {detail['weight']:.1%}\n"
            report += f"  Weighted Score: {detail['weighted_score']:.1f}\n"
            if detail['description']:
                report += f"  Description: {detail['description']}\n"
        
        if filename:
            with open(filename, 'w') as f:
                f.write(report)
        
        return report
    
    def get_validation_history_df(self) -> pd.DataFrame:
        """Get validation history as a pandas DataFrame."""
        if not self.validation_history:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.validation_history)
        df = df.set_index('timestamp')
        return df
    
    def check_auto_grading_available(self) -> bool:
        """Check if auto-grading functionality is available."""
        required_methods = [
            'add_scoring_rule', 'validate_with_score', 'run_auto_grading', 
            'export_grading_report', 'get_validation_history_df'
        ]
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(self, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Missing auto-grading methods: {missing_methods}")
            print("💡 Please restart the Jupyter kernel to reload the module.")
            return False
        else:
            print("✅ All auto-grading methods are available!")
            return True
    
    # MongoDB Status Checker functionality
    def validate_mongodb_connection(self, connection_string: str = None, 
                                  client_object: Any = None,
                                  timeout: int = 5) -> bool:
        """
        Validate MongoDB connection using either connection string or existing client.
        
        Args:
            connection_string: MongoDB connection string
            client_object: Existing pymongo MongoClient object
            timeout: Connection timeout in seconds
        """
        try:
            # Try to import pymongo
            try:
                from pymongo import MongoClient
                from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
            except ImportError:
                return self._display_result(False, "PyMongo not installed",
                                          "Install with: pip install pymongo")
            
            # Create or use existing client
            if client_object:
                client = client_object
                source = "provided client object"
            elif connection_string:
                client = MongoClient(connection_string, serverSelectionTimeoutMS=timeout*1000)
                source = "connection string"
            else:
                return self._display_result(False, "No MongoDB connection provided",
                                          "Provide either connection_string or client_object")
            
            # Test the connection
            start_time = time.time()
            try:
                # The admin command 'ping' is a good way to test connectivity
                result = client.admin.command('ping')
                connection_time = round((time.time() - start_time) * 1000, 2)
                
                if result.get('ok') == 1:
                    return self._display_result(True, 
                                              f"MongoDB connection successful via {source}",
                                              f"Ping response time: {connection_time}ms")
                else:
                    return self._display_result(False, "MongoDB ping failed", 
                                              f"Response: {result}")
                    
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                return self._display_result(False, "MongoDB connection failed", str(e))
            except Exception as e:
                return self._display_result(False, "MongoDB connection error", str(e))
                
        except Exception as e:
            return self._display_result(False, "Error testing MongoDB connection", str(e))
    
    def validate_mongodb_database(self, client: Any, database_name: str) -> bool:
        """
        Validate that a MongoDB database exists and is accessible.
        
        Args:
            client: pymongo MongoClient object
            database_name: Name of the database to validate
        """
        try:
            # Check if database exists
            db_list = client.list_database_names()
            
            if database_name not in db_list:
                return self._display_result(False, f"Database '{database_name}' not found",
                                          f"Available databases: {db_list}")
            
            # Try to access the database
            db = client[database_name]
            collections = db.list_collection_names()
            
            return self._display_result(True, f"Database '{database_name}' validated",
                                      f"Collections found: {len(collections)} ({collections[:5]}{'...' if len(collections) > 5 else ''})")
            
        except Exception as e:
            return self._display_result(False, f"Error validating database '{database_name}'", str(e))
    
    def validate_mongodb_collection(self, db: Any, collection_name: str, 
                                   min_documents: int = 0,
                                   expected_fields: Optional[List[str]] = None) -> bool:
        """
        Validate MongoDB collection existence, document count, and schema.
        
        Args:
            db: pymongo Database object
            collection_name: Name of the collection
            min_documents: Minimum expected document count
            expected_fields: List of field names that should exist in documents
        """
        try:
            # Check if collection exists
            collections = db.list_collection_names()
            if collection_name not in collections:
                return self._display_result(False, f"Collection '{collection_name}' not found",
                                          f"Available collections: {collections}")
            
            collection = db[collection_name]
            
            # Check document count
            doc_count = collection.count_documents({})
            if doc_count < min_documents:
                return self._display_result(False, f"Collection '{collection_name}' has insufficient documents",
                                          f"Found {doc_count}, expected at least {min_documents}")
            
            details = [f"Document count: {doc_count}"]
            
            # Check for expected fields if provided
            if expected_fields and doc_count > 0:
                sample_doc = collection.find_one()
                missing_fields = []
                present_fields = []
                
                for field in expected_fields:
                    if field in sample_doc:
                        present_fields.append(field)
                    else:
                        missing_fields.append(field)
                
                if missing_fields:
                    return self._display_result(False, f"Missing expected fields in '{collection_name}'",
                                              f"Missing: {missing_fields}, Present: {present_fields}")
                
                details.append(f"All expected fields present: {expected_fields}")
            
            return self._display_result(True, f"Collection '{collection_name}' validated", 
                                      "; ".join(details))
            
        except Exception as e:
            return self._display_result(False, f"Error validating collection '{collection_name}'", str(e))
    
    def validate_mongodb_index(self, collection: Any, index_fields: Union[str, List[str]],
                              index_type: str = "single") -> bool:
        """
        Validate that a MongoDB index exists on specified fields.
        
        Args:
            collection: pymongo Collection object
            index_fields: Field name(s) for the index
            index_type: Type of index ("single", "compound", "text", "vector")
        """
        try:
            indexes = list(collection.list_indexes())
            
            # Convert single field to list for consistent processing
            if isinstance(index_fields, str):
                index_fields = [index_fields]
            
            # Look for matching index
            for index in indexes:
                index_key = index.get('key', {})
                
                if index_type == "vector":
                    # Vector search indexes have special structure
                    if any(field in str(index) for field in index_fields):
                        return self._display_result(True, f"Vector index found for fields: {index_fields}")
                        
                elif index_type == "text":
                    # Text indexes
                    if any(index_key.get(field) == "text" for field in index_fields):
                        return self._display_result(True, f"Text index found for fields: {index_fields}")
                        
                else:
                    # Regular and compound indexes
                    index_field_names = list(index_key.keys())
                    if set(index_fields).issubset(set(index_field_names)):
                        return self._display_result(True, f"Index found for fields: {index_fields}",
                                                  f"Index name: {index.get('name', 'unknown')}")
            
            # No matching index found
            available_indexes = [f"{idx.get('name', 'unknown')}: {list(idx.get('key', {}).keys())}" 
                               for idx in indexes]
            return self._display_result(False, f"No {index_type} index found for fields: {index_fields}",
                                      f"Available indexes: {available_indexes}")
            
        except Exception as e:
            return self._display_result(False, f"Error checking index for {index_fields}", str(e))
    
    def validate_mongodb_query(self, collection: Any, query: Dict[str, Any],
                              expected_count: Optional[int] = None,
                              max_execution_time: float = 5.0) -> bool:
        """
        Validate a MongoDB query execution and optionally check result count.
        
        Args:
            collection: pymongo Collection object
            query: MongoDB query document
            expected_count: Expected number of results (optional)
            max_execution_time: Maximum allowed execution time in seconds
        """
        try:
            start_time = time.time()
            
            # Execute the query
            cursor = collection.find(query)
            results = list(cursor)
            
            execution_time = time.time() - start_time
            result_count = len(results)
            
            details = [f"Execution time: {execution_time:.3f}s", f"Results: {result_count}"]
            
            # Check execution time
            if execution_time > max_execution_time:
                return self._display_result(False, "Query execution too slow",
                                          f"Took {execution_time:.3f}s, maximum allowed: {max_execution_time}s")
            
            # Check result count if specified
            if expected_count is not None and result_count != expected_count:
                return self._display_result(False, "Query result count mismatch",
                                          f"Expected {expected_count}, got {result_count}")
            
            return self._display_result(True, "MongoDB query executed successfully", "; ".join(details))
            
        except Exception as e:
            return self._display_result(False, "MongoDB query execution failed", str(e))
    
    def check_mongodb_atlas_cluster_status(self, connection_string: str) -> bool:
        """
        Check MongoDB Atlas cluster status and basic health metrics.
        
        Args:
            connection_string: MongoDB Atlas connection string
        """
        try:
            from pymongo import MongoClient
            from pymongo.errors import ConnectionFailure
            
            client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
            
            try:
                # Get server status
                server_status = client.admin.command('serverStatus')
                
                # Extract key metrics
                uptime = server_status.get('uptime', 0)
                connections = server_status.get('connections', {})
                memory = server_status.get('mem', {})
                
                uptime_hours = uptime / 3600
                
                details = [
                    f"Uptime: {uptime_hours:.1f} hours",
                    f"Connections: {connections.get('current', 'unknown')}/{connections.get('available', 'unknown')}",
                    f"Memory usage: {memory.get('resident', 'unknown')}MB"
                ]
                
                # Basic health checks
                if uptime < 300:  # Less than 5 minutes
                    return self._display_result(False, "Atlas cluster recently restarted",
                                              f"Uptime: {uptime_hours:.1f} hours (may indicate issues)")
                
                return self._display_result(True, "MongoDB Atlas cluster is healthy", "; ".join(details))
                
            except Exception as e:
                return self._display_result(False, "Could not retrieve Atlas cluster status", str(e))
                
        except Exception as e:
            return self._display_result(False, "Error connecting to MongoDB Atlas", str(e))
    
    def create_mongodb_diagnostic_report(self, client: Any, database_name: str = None) -> Dict[str, Any]:
        """
        Generate a comprehensive MongoDB diagnostic report.
        
        Args:
            client: pymongo MongoClient object
            database_name: Optional specific database to focus on
            
        Returns:
            Dictionary with diagnostic information
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'connection_status': 'unknown',
            'databases': [],
            'server_info': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Test connection
            client.admin.command('ping')
            report['connection_status'] = 'connected'
            
            # Get server information
            try:
                server_info = client.server_info()
                report['server_info'] = {
                    'version': server_info.get('version', 'unknown'),
                    'platform': server_info.get('os', {}).get('name', 'unknown'),
                    'architecture': server_info.get('os', {}).get('architecture', 'unknown')
                }
            except:
                report['issues'].append("Could not retrieve server information")
            
            # List databases
            try:
                db_names = client.list_database_names()
                for db_name in db_names:
                    if database_name and db_name != database_name:
                        continue
                        
                    db = client[db_name]
                    collections = db.list_collection_names()
                    
                    db_info = {
                        'name': db_name,
                        'collections': len(collections),
                        'collection_names': collections[:10]  # First 10 collections
                    }
                    
                    # Get collection stats for main collections
                    if collections:
                        try:
                            stats = db.command('dbStats')
                            db_info.update({
                                'data_size': stats.get('dataSize', 0),
                                'storage_size': stats.get('storageSize', 0),
                                'index_size': stats.get('indexSize', 0)
                            })
                        except:
                            pass
                    
                    report['databases'].append(db_info)
                    
            except Exception as e:
                report['issues'].append(f"Could not list databases: {str(e)}")
            
            # Generate recommendations
            if not report['databases']:
                report['recommendations'].append("No databases found - create a database and collection to get started")
            
            for db_info in report['databases']:
                if db_info['collections'] == 0:
                    report['recommendations'].append(f"Database '{db_info['name']}' has no collections")
                elif db_info['collections'] > 100:
                    report['recommendations'].append(f"Database '{db_info['name']}' has many collections ({db_info['collections']}) - consider organization")
            
        except Exception as e:
            report['connection_status'] = 'failed'
            report['issues'].append(f"Connection failed: {str(e)}")
        
        # Display the report
        self._display_mongodb_report(report)
        
        return report
    
    def _display_mongodb_report(self, report: Dict[str, Any]):
        """Display MongoDB diagnostic report in a nice format."""
        status_color = "#4CAF50" if report['connection_status'] == 'connected' else "#f44336"
        status_icon = "✅" if report['connection_status'] == 'connected' else "❌"
        
        html = f"""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0; font-family: Arial, sans-serif;'>
            <h3 style='color: #333; margin-bottom: 15px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px;'>
                🔍 MongoDB Diagnostic Report
            </h3>
            
            <div style='margin: 15px 0;'>
                <h4 style='color: #495057; margin-bottom: 10px;'>Connection Status</h4>
                <div style='background-color: white; padding: 10px; border-left: 4px solid {status_color}; border-radius: 5px;'>
                    <span style='font-size: 18px; margin-right: 10px;'>{status_icon}</span>
                    <strong style='color: {status_color};'>{report['connection_status'].upper()}</strong>
                    <small style='color: #666; margin-left: 10px;'>{report['timestamp']}</small>
                </div>
            </div>
        """
        
        # Server info
        if report['server_info']:
            html += f"""
            <div style='margin: 15px 0;'>
                <h4 style='color: #495057; margin-bottom: 10px;'>Server Information</h4>
                <div style='background-color: white; padding: 10px; border-radius: 5px; border: 1px solid #e9ecef;'>
                    <strong>Version:</strong> {report['server_info'].get('version', 'unknown')}<br>
                    <strong>Platform:</strong> {report['server_info'].get('platform', 'unknown')}<br>
                    <strong>Architecture:</strong> {report['server_info'].get('architecture', 'unknown')}
                </div>
            </div>
            """
        
        # Databases
        if report['databases']:
            html += """
            <div style='margin: 15px 0;'>
                <h4 style='color: #495057; margin-bottom: 10px;'>Databases</h4>
            """
            
            for db in report['databases']:
                html += f"""
                <div style='background-color: white; padding: 10px; margin: 5px 0; border-radius: 5px; border: 1px solid #e9ecef;'>
                    <strong>{db['name']}</strong> - {db['collections']} collections
                    {f"<br><small style='color: #666;'>Collections: {', '.join(db['collection_names'][:5])}{'...' if len(db['collection_names']) > 5 else ''}</small>" if db['collection_names'] else ""}
                    {f"<br><small style='color: #666;'>Data: {db.get('data_size', 0):,} bytes, Storage: {db.get('storage_size', 0):,} bytes</small>" if 'data_size' in db else ""}
                </div>
                """
            
            html += "</div>"
        
        # Issues
        if report['issues']:
            html += """
            <div style='margin: 15px 0;'>
                <h4 style='color: #dc3545; margin-bottom: 10px;'>⚠️ Issues Found</h4>
            """
            for issue in report['issues']:
                html += f"""
                <div style='background-color: #fff3cd; padding: 8px; margin: 3px 0; border-radius: 3px; border-left: 3px solid #ffc107;'>
                    {issue}
                </div>
                """
            html += "</div>"
        
        # Recommendations
        if report['recommendations']:
            html += """
            <div style='margin: 15px 0;'>
                <h4 style='color: #0066cc; margin-bottom: 10px;'>💡 Recommendations</h4>
            """
            for rec in report['recommendations']:
                html += f"""
                <div style='background-color: #d1ecf1; padding: 8px; margin: 3px 0; border-radius: 3px; border-left: 3px solid #0066cc;'>
                    {rec}
                </div>
                """
            html += "</div>"
        
        html += "</div>"
        
        display(HTML(html))
    
    def _display_dataframe_visuals(self, df: pd.DataFrame, show_preview: bool = True,
                                  show_histograms: bool = False,
                                  histogram_columns: Optional[List[str]] = None):
        """Display enhanced visuals for DataFrame validation."""
        try:
            # Import plotting libraries with fallback
            plotting_available = True
            try:
                import matplotlib.pyplot as plt
                import seaborn as sns
                plt.style.use('default')
            except ImportError:
                plotting_available = False
            
            if show_preview:
                self._display_dataframe_preview(df)
            
            if show_histograms and plotting_available:
                self._display_dataframe_histograms(df, histogram_columns)
            elif show_histograms and not plotting_available:
                display(HTML("""
                <div style='background-color: #fff3cd; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107;'>
                    <strong>⚠️ Plotting libraries not available</strong><br>
                    Install matplotlib and seaborn to see histograms: <code>pip install matplotlib seaborn</code>
                </div>
                """))
        except Exception as e:
            display(HTML(f"""
            <div style='background-color: #f8d7da; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #dc3545;'>
                <strong>❌ Error displaying DataFrame visuals:</strong> {str(e)}
            </div>
            """))
    
    def _display_dataframe_preview(self, df: pd.DataFrame):
        """Display DataFrame preview with styling."""
        html = """
        <div style='background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #dee2e6;'>
            <h4 style='color: #495057; margin-bottom: 10px; font-size: 16px;'>📊 DataFrame Preview</h4>
            <div style='margin-bottom: 10px;'>
                <strong>Shape:</strong> {shape} | <strong>Memory Usage:</strong> {memory}
            </div>
        """.format(
            shape=f"{df.shape[0]:,} rows × {df.shape[1]} columns",
            memory=f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        )
        
        # Add column info
        html += "<div style='margin-bottom: 15px;'><strong>Columns:</strong><br>"
        for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes)):
            null_count = df[col].isnull().sum()
            html += f"<span style='font-family: monospace; background-color: #e9ecef; padding: 2px 4px; margin: 2px; border-radius: 3px; font-size: 12px;'>{col} ({dtype})"
            if null_count > 0:
                html += f" - {null_count} nulls"
            html += "</span> "
            if i > 0 and (i + 1) % 3 == 0:
                html += "<br>"
        html += "</div>"
        
        html += "</div>"
        display(HTML(html))
        
        # Display the actual dataframe head
        try:
            from IPython.display import display
            display(df.head())
        except:
            # Fallback to simple string representation
            display(HTML(f"<pre>{df.head().to_string()}</pre>"))
    
    def _display_dataframe_histograms(self, df: pd.DataFrame, 
                                     histogram_columns: Optional[List[str]] = None):
        """Display histograms for numeric columns."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Get numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if histogram_columns:
                # Filter to specified columns that are also numeric
                numeric_cols = [col for col in histogram_columns if col in numeric_cols]
            
            if not numeric_cols:
                display(HTML("""
                <div style='background-color: #d1ecf1; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #0066cc;'>
                    <strong>ℹ️ No numeric columns found for histograms</strong>
                </div>
                """))
                return
            
            # Limit to first 6 columns to avoid overwhelming output
            numeric_cols = numeric_cols[:6]
            
            # Create subplots
            n_cols = min(3, len(numeric_cols))
            n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 3*n_rows))
            if n_rows == 1 and n_cols == 1:
                axes = [axes]
            elif n_rows == 1:
                axes = axes
            else:
                axes = axes.flatten()
            
            for i, col in enumerate(numeric_cols):
                ax = axes[i] if len(numeric_cols) > 1 else axes
                
                # Remove any infinite values for plotting
                data = df[col].replace([np.inf, -np.inf], np.nan).dropna()
                
                if len(data) > 0:
                    ax.hist(data, bins=min(30, len(data)//2), alpha=0.7, color='skyblue', edgecolor='black')
                    ax.set_title(f'{col}\n(mean: {data.mean():.2f}, std: {data.std():.2f})', fontsize=10)
                    ax.set_xlabel(col)
                    ax.set_ylabel('Frequency')
                    ax.grid(True, alpha=0.3)
                else:
                    ax.text(0.5, 0.5, f'No valid data\nfor {col}', 
                           ha='center', va='center', transform=ax.transAxes)
                    ax.set_title(col)
            
            # Hide unused subplots
            for i in range(len(numeric_cols), len(axes)):
                axes[i].set_visible(False)
            
            plt.suptitle('DataFrame Histograms', fontsize=14, y=1.02)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            display(HTML(f"""
            <div style='background-color: #f8d7da; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #dc3545;'>
                <strong>❌ Error creating histograms:</strong> {str(e)}
            </div>
            """))
    
    def analyze_dataframe(self, df: pd.DataFrame, column_focus: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Comprehensive DataFrame analysis with visual output.
        
        Args:
            df: DataFrame to analyze
            column_focus: Optional list of columns to focus analysis on
            
        Returns:
            Dictionary with analysis results
        """
        if not isinstance(df, pd.DataFrame):
            self._display_result(False, "Not a DataFrame", f"Got {type(df).__name__} instead")
            return {}
        
        # Basic info
        analysis = {
            'shape': df.shape,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'column_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': df.duplicated().sum(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
        }
        
        # Focus on specific columns if requested
        focus_cols = column_focus if column_focus else df.columns.tolist()
        
        # Numeric analysis
        numeric_stats = {}
        for col in analysis['numeric_columns']:
            if col in focus_cols:
                series = df[col]
                numeric_stats[col] = {
                    'mean': series.mean() if not series.empty else None,
                    'median': series.median() if not series.empty else None,
                    'std': series.std() if not series.empty else None,
                    'min': series.min() if not series.empty else None,
                    'max': series.max() if not series.empty else None,
                    'q25': series.quantile(0.25) if not series.empty else None,
                    'q75': series.quantile(0.75) if not series.empty else None,
                    'outliers': len(series[(series < (series.quantile(0.25) - 1.5 * (series.quantile(0.75) - series.quantile(0.25)))) | 
                                          (series > (series.quantile(0.75) + 1.5 * (series.quantile(0.75) - series.quantile(0.25))))])
                }
        
        analysis['numeric_stats'] = numeric_stats
        
        # Categorical analysis
        categorical_stats = {}
        for col in analysis['categorical_columns']:
            if col in focus_cols:
                series = df[col]
                categorical_stats[col] = {
                    'unique_values': series.nunique(),
                    'most_common': series.value_counts().head().to_dict() if not series.empty else {},
                    'missing_count': series.isnull().sum()
                }
        
        analysis['categorical_stats'] = categorical_stats
        
        # Display the analysis
        self._display_dataframe_analysis(analysis, df)
        
        return analysis
    
    def _display_dataframe_analysis(self, analysis: Dict[str, Any], df: pd.DataFrame):
        """Display comprehensive DataFrame analysis."""
        html = f"""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0; font-family: Arial, sans-serif;'>
            <h3 style='color: #333; margin-bottom: 15px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px;'>
                📊 DataFrame Analysis Report
            </h3>
            
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px;'>
                <div style='background-color: white; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;'>
                    <h4 style='color: #495057; margin-bottom: 10px; font-size: 16px;'>📏 Shape & Size</h4>
                    <div><strong>Rows:</strong> {analysis['shape'][0]:,}</div>
                    <div><strong>Columns:</strong> {analysis['shape'][1]:,}</div>
                    <div><strong>Memory:</strong> {analysis['memory_usage_mb']:.2f} MB</div>
                    <div><strong>Duplicates:</strong> {analysis['duplicate_rows']:,}</div>
                </div>
                
                <div style='background-color: white; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;'>
                    <h4 style='color: #495057; margin-bottom: 10px; font-size: 16px;'>🏷️ Column Types</h4>
                    <div><strong>Numeric:</strong> {len(analysis['numeric_columns'])}</div>
                    <div><strong>Categorical:</strong> {len(analysis['categorical_columns'])}</div>
                    <div><strong>DateTime:</strong> {len(analysis['datetime_columns'])}</div>
                    <div><strong>Total Missing:</strong> {sum(analysis['missing_values'].values()):,}</div>
                </div>
            </div>
        """
        
        # Missing values section
        missing_cols = {k: v for k, v in analysis['missing_values'].items() if v > 0}
        if missing_cols:
            html += """
            <div style='background-color: #fff3cd; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #ffc107;'>
                <h4 style='color: #856404; margin-bottom: 10px; font-size: 16px;'>⚠️ Missing Values</h4>
            """
            for col, count in sorted(missing_cols.items(), key=lambda x: x[1], reverse=True)[:10]:
                pct = (count / analysis['shape'][0]) * 100
                html += f"<div><strong>{col}:</strong> {count:,} ({pct:.1f}%)</div>"
            if len(missing_cols) > 10:
                html += f"<div><em>... and {len(missing_cols) - 10} more columns with missing values</em></div>"
            html += "</div>"
        
        # Numeric stats
        if analysis['numeric_stats']:
            html += """
            <div style='background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; border: 1px solid #dee2e6;'>
                <h4 style='color: #495057; margin-bottom: 15px; font-size: 16px;'>📈 Numeric Columns Summary</h4>
                <div style='overflow-x: auto;'>
                    <table style='width: 100%; border-collapse: collapse; font-size: 12px;'>
                        <thead>
                            <tr style='background-color: #f8f9fa;'>
                                <th style='padding: 8px; text-align: left; border: 1px solid #dee2e6;'>Column</th>
                                <th style='padding: 8px; text-align: right; border: 1px solid #dee2e6;'>Mean</th>
                                <th style='padding: 8px; text-align: right; border: 1px solid #dee2e6;'>Median</th>
                                <th style='padding: 8px; text-align: right; border: 1px solid #dee2e6;'>Std</th>
                                <th style='padding: 8px; text-align: right; border: 1px solid #dee2e6;'>Min</th>
                                <th style='padding: 8px; text-align: right; border: 1px solid #dee2e6;'>Max</th>
                                <th style='padding: 8px; text-align: right; border: 1px solid #dee2e6;'>Outliers</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for col, stats in analysis['numeric_stats'].items():
                html += f"""
                <tr>
                    <td style='padding: 8px; border: 1px solid #dee2e6; font-weight: bold;'>{col}</td>
                    <td style='padding: 8px; border: 1px solid #dee2e6; text-align: right;'>{stats['mean']:.2f if stats['mean'] is not None else 'N/A'}</td>
                    <td style='padding: 8px; border: 1px solid #dee2e6; text-align: right;'>{stats['median']:.2f if stats['median'] is not None else 'N/A'}</td>
                    <td style='padding: 8px; border: 1px solid #dee2e6; text-align: right;'>{stats['std']:.2f if stats['std'] is not None else 'N/A'}</td>
                    <td style='padding: 8px; border: 1px solid #dee2e6; text-align: right;'>{stats['min']:.2f if stats['min'] is not None else 'N/A'}</td>
                    <td style='padding: 8px; border: 1px solid #dee2e6; text-align: right;'>{stats['max']:.2f if stats['max'] is not None else 'N/A'}</td>
                    <td style='padding: 8px; border: 1px solid #dee2e6; text-align: right;'>{stats['outliers']}</td>
                </tr>
                """
            
            html += """
                        </tbody>
                    </table>
                </div>
            </div>
            """
        
        # Categorical stats
        if analysis['categorical_stats']:
            html += """
            <div style='background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; border: 1px solid #dee2e6;'>
                <h4 style='color: #495057; margin-bottom: 15px; font-size: 16px;'>🏷️ Categorical Columns Summary</h4>
            """
            
            for col, stats in list(analysis['categorical_stats'].items())[:5]:  # Show first 5
                html += f"""
                <div style='margin-bottom: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'>
                    <div style='font-weight: bold; margin-bottom: 5px;'>{col}</div>
                    <div style='font-size: 12px; color: #666;'>
                        Unique values: {stats['unique_values']} | Missing: {stats['missing_count']}
                    </div>
                """
                
                if stats['most_common']:
                    html += "<div style='margin-top: 5px; font-size: 11px;'>"
                    for value, count in list(stats['most_common'].items())[:3]:
                        pct = (count / analysis['shape'][0]) * 100
                        html += f"<span style='background-color: #e9ecef; padding: 2px 6px; margin: 2px; border-radius: 3px;'>{value}: {count} ({pct:.1f}%)</span> "
                    html += "</div>"
                
                html += "</div>"
            
            if len(analysis['categorical_stats']) > 5:
                html += f"<div><em>... and {len(analysis['categorical_stats']) - 5} more categorical columns</em></div>"
            
            html += "</div>"
        
        html += "</div>"
        
        display(HTML(html))
        
        # Also show preview and histograms
        self._display_dataframe_preview(df)
        if analysis['numeric_columns']:
            self._display_dataframe_histograms(df, analysis['numeric_columns'][:6])