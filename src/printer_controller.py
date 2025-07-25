"""
Printer Controller Module

Handles communication with printers for the child's automatic printer system.
"""

import logging
import cups
from typing import Optional, List
from pathlib import Path


class PrinterController:
    """Controls printer operations for kid-friendly content."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.conn = cups.Connection()
            self.logger.info("Connected to CUPS printing system")
        except Exception as e:
            self.logger.error(f"Failed to connect to printer system: {e}")
            self.conn = None
    
    def get_available_printers(self) -> List[str]:
        """Get list of available printers."""
        if not self.conn:
            return []
        
        try:
            printers = self.conn.getPrinters()
            printer_names = list(printers.keys())
            self.logger.info(f"Available printers: {printer_names}")
            return printer_names
        except Exception as e:
            self.logger.error(f"Error getting printers: {e}")
            return []
    
    def print_text(self, text: str, printer_name: Optional[str] = None) -> bool:
        """
        Print text content.
        
        Args:
            text: Text to print
            printer_name: Specific printer to use (None for default)
            
        Returns:
            True if print job was submitted successfully
        """
        if not self.conn:
            self.logger.error("No printer connection available")
            return False
        
        try:
            # Create temporary text file
            temp_file = Path("/tmp/kidprinter_text.txt")
            temp_file.write_text(text, encoding="utf-8")
            
            # Submit print job
            if printer_name:
                job_id = self.conn.printFile(printer_name, str(temp_file), "Kid Printer Text", {})
            else:
                # Use default printer
                printers = self.get_available_printers()
                if not printers:
                    self.logger.error("No printers available")
                    return False
                job_id = self.conn.printFile(printers[0], str(temp_file), "Kid Printer Text", {})
            
            self.logger.info(f"Print job submitted with ID: {job_id}")
            
            # Clean up temp file
            temp_file.unlink(missing_ok=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error printing text: {e}")
            return False
    
    def print_image(self, image_path: str, printer_name: Optional[str] = None) -> bool:
        """
        Print an image file.
        
        Args:
            image_path: Path to image file
            printer_name: Specific printer to use (None for default)
            
        Returns:
            True if print job was submitted successfully
        """
        if not self.conn:
            self.logger.error("No printer connection available")
            return False
        
        if not Path(image_path).exists():
            self.logger.error(f"Image file not found: {image_path}")
            return False
        
        try:
            if printer_name:
                job_id = self.conn.printFile(printer_name, image_path, "Kid Printer Image", {})
            else:
                printers = self.get_available_printers()
                if not printers:
                    self.logger.error("No printers available")
                    return False
                job_id = self.conn.printFile(printers[0], image_path, "Kid Printer Image", {})
            
            self.logger.info(f"Image print job submitted with ID: {job_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error printing image: {e}")
            return False
    
    def print_content(self, content: str) -> bool:
        """
        Print content based on voice command.
        
        Args:
            content: Recognized voice command
            
        Returns:
            True if content was printed successfully
        """
        # Simple logic - can be expanded based on command parsing
        if "kuva" in content or "piirros" in content:
            # For now, just print the text request
            # TODO: Implement image generation/selection
            return self.print_text(f"Kuva-pyyntö: {content}")
        else:
            return self.print_text(content)
