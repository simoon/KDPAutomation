"""
Batch Processing Manager for BookBolt Automation
Handles execution of multiple notebooks with progress tracking and summaries
"""

import time
from typing import Dict, Any, Callable
from utils.random_helper import RandomHelper

class BatchProcessor:
    """
    Manages batch processing of multiple notebooks with progress tracking,
    error handling, and detailed execution summaries.
    """
    
    def __init__(self, user_config_manager, random_helper: RandomHelper):
        self.config = user_config_manager
        self.random_helper = random_helper
        
        # Tracking variables
        self.successful_notebooks = 0
        self.failed_notebooks = 0
        self.execution_start_time = None
        self.execution_end_time = None
        
    def execute_batch_processing(self, sequence_executor: Callable[[str], bool], 
                                sequence_name: str = "template_creation_workflow") -> bool:
        """
        Execute batch processing for all configured notebooks.
        
        Args:
            sequence_executor: Function that executes a single sequence
            sequence_name: Name of sequence to execute
            
        Returns:
            bool: True if all sequences completed successfully
        """
        try:
            self.execution_start_time = time.time()
            
            print(f"\n🚀 Starting batch execution for {self.config.total_notebooks} notebooks")
            print(f"📈 Range: {self.config.start_number} to {self.config.start_number + self.config.total_notebooks - 1}")
            print(f"📚 Template: {self.config.selected_template['name']}")
            
            # Reset counters
            self.successful_notebooks = 0
            self.failed_notebooks = 0
            self.config.current_notebook_number = self.config.start_number
            
            for i in range(self.config.total_notebooks):
                print(f"\n" + "="*50)
                print(f"📖 NOTEBOOK {i+1}/{self.config.total_notebooks} - Number: {self.config.current_notebook_number}")
                print(f"📝 Dynamic Text: '{self.config.generate_dynamic_text()}'")
                print("="*50)
                
                # Execute sequence for this notebook
                success = sequence_executor(sequence_name)
                
                if success:
                    self.successful_notebooks += 1
                    print(f"✅ Notebook {self.config.current_notebook_number} completed successfully!")
                else:
                    self.failed_notebooks += 1
                    print(f"❌ Notebook {self.config.current_notebook_number} failed!")
                    
                    # Ask user if they want to continue
                    continue_choice = input(f"\n❓ Continue with remaining notebooks? (y/n): ").strip().lower()
                    if continue_choice not in ['y', 'yes']:
                        print("ℹ️ Batch execution stopped by user.")
                        print(f"🛑 STOPPED AT: Notebook {self.config.current_notebook_number}")
                        break
                
                # Increment for next iteration
                self.config.current_notebook_number += 1
                
                # Pause between notebooks (except for the last one)
                if i < self.config.total_notebooks - 1:
                    pause = self.random_helper.get_natural_pause("general")
                    print(f"⏸️ Pause between notebooks: {pause:.1f}s")
                    time.sleep(pause)
            
            self.execution_end_time = time.time()
            
            # Final summary
            self.print_batch_summary()
            return self.failed_notebooks == 0
            
        except Exception as e:
            print(f"❌ Batch execution failed: {e}")
            return False
    
    def print_batch_summary(self):
        """Print detailed batch execution summary with start/end numbers."""
        execution_time = None
        if self.execution_start_time and self.execution_end_time:
            execution_time = self.execution_end_time - self.execution_start_time
        
        print(f"\n" + "="*60)
        print(f"📊 BATCH EXECUTION SUMMARY")
        print(f"="*60)
        print(f"📚 Template: {self.config.selected_template['name']}")
        print(f"🔢 Configured Range: {self.config.start_number} to {self.config.start_number + self.config.total_notebooks - 1}")
        print(f"🔢 Actual Range Processed: {self.config.start_number} to {self.config.current_notebook_number - 1}")
        print(f"✅ Successful: {self.successful_notebooks}")
        print(f"❌ Failed: {self.failed_notebooks}")
        
        if self.config.total_notebooks > 0:
            success_rate = (self.successful_notebooks / self.config.total_notebooks) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if execution_time:
            print(f"⏱️ Total Execution Time: {execution_time/60:.1f} minutes")
            if self.successful_notebooks > 0:
                avg_time = execution_time / self.successful_notebooks
                print(f"⏱️ Average Time per Notebook: {avg_time:.1f} seconds")
        
        # Show where we stopped if interrupted
        expected_end = self.config.start_number + self.config.total_notebooks - 1
        actual_end = self.config.current_notebook_number - 1
        
        if actual_end < expected_end:
            print(f"🛑 EARLY TERMINATION:")
            print(f"   • Expected to end at: {expected_end}")
            print(f"   • Actually ended at: {actual_end}")
            print(f"   • Remaining: {expected_end - actual_end} notebooks")
        else:
            print(f"✅ COMPLETED: All notebooks processed successfully")
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics as dictionary"""
        execution_time = None
        if self.execution_start_time and self.execution_end_time:
            execution_time = self.execution_end_time - self.execution_start_time
            
        return {
            'successful_notebooks': self.successful_notebooks,
            'failed_notebooks': self.failed_notebooks,
            'total_configured': self.config.total_notebooks,
            'start_number': self.config.start_number,
            'end_number_configured': self.config.start_number + self.config.total_notebooks - 1,
            'end_number_actual': self.config.current_notebook_number - 1,
            'success_rate': (self.successful_notebooks / self.config.total_notebooks * 100) if self.config.total_notebooks > 0 else 0,
            'execution_time_seconds': execution_time,
            'avg_time_per_notebook': execution_time / self.successful_notebooks if execution_time and self.successful_notebooks > 0 else None
        }