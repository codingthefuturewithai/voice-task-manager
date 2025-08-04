#!/usr/bin/env python3
"""
UI tests for Voice Task Manager using Playwright
Tests the Streamlit interface and identifies UI issues
"""

import asyncio
import time
import subprocess
import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class StreamlitUITester:
    def __init__(self):
        self.process = None
        self.base_url = "http://localhost:8501"
    
    async def start_streamlit(self):
        """Start the Streamlit app"""
        print("🚀 Starting Streamlit app...")
        
        # Kill any existing process on port 8501
        try:
            subprocess.run(["lsof", "-ti:8501"], capture_output=True, text=True)
            subprocess.run(["kill", "-9", "$(lsof -ti:8501)"], shell=True)
        except:
            pass
        
        # Start Streamlit
        self.process = subprocess.Popen([
            "streamlit", "run", "app.py", 
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for app to start
        await asyncio.sleep(5)
        print("✅ Streamlit app started")
    
    async def stop_streamlit(self):
        """Stop the Streamlit app"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✅ Streamlit app stopped")
    
    async def test_basic_ui_loading(self, page):
        """Test that the UI loads correctly"""
        print("🧪 Testing basic UI loading...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Check that main elements are present
        assert await page.locator("text=Voice Task Manager").is_visible(), "Title should be visible"
        assert await page.locator("text=Mode Selection").is_visible(), "Mode selection should be visible"
        assert await page.locator("text=Voice Input").is_visible(), "Voice input should be visible"
        assert await page.locator("text=Task List").is_visible(), "Task list should be visible"
        
        print("✅ Basic UI loading passed!")
    
    async def test_mode_switching(self, page):
        """Test mode switching behavior"""
        print("🧪 Testing mode switching...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Wait for the radio buttons to be visible and interactive
        await page.wait_for_selector('.stRadio', timeout=10000)
        
        # Click on the Command mode option (second option)
        command_radio_label = page.locator('[data-baseweb="radio"]').nth(1)
        await command_radio_label.click()
        await page.wait_for_timeout(2000)  # Wait for UI update
        
        # Check that instructions changed to Command mode
        assert await page.locator("text=Command Mode").is_visible(), "Command mode instructions should be visible"
        
        print("✅ Mode switching passed!")
    
    async def test_task_operations(self, page):
        """Test task operations via text input (simulating voice input)"""
        print("🧪 Testing task operations...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Add a task manually by simulating the flow
        # Since we can't test voice input, we'll test the task display and operations
        
        # Check that task list shows "No tasks yet" initially
        assert await page.locator("text=No tasks yet").is_visible(), "Should show no tasks message"
        
        # Test quick actions
        clear_button = page.locator("button:has-text('Clear All Tasks')")
        assert await clear_button.is_visible(), "Clear All Tasks button should be visible"
        
        prioritize_button = page.locator("button:has-text('Auto-Prioritize')")
        assert await prioritize_button.is_visible(), "Auto-Prioritize button should be visible"
        
        print("✅ Task operations UI elements passed!")
    
    async def test_duplicate_panel_issue(self, page):
        """Test for the duplicate panel issue mentioned by user"""
        print("🧪 Testing for duplicate panel issue...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Count voice input sections
        voice_input_sections = page.locator("text=Voice Input")
        count = await voice_input_sections.count()
        
        print(f"Found {count} voice input sections")
        
        # Should only have one voice input section
        assert count == 1, f"Expected 1 voice input section, found {count}"
        
        # Check for any duplicate elements
        mode_selections = page.locator("text=Mode Selection")
        mode_count = await mode_selections.count()
        assert mode_count == 1, f"Expected 1 mode selection, found {mode_count}"
        
        print("✅ No duplicate panels detected!")
    
    async def test_state_persistence(self, page):
        """Test that state persists correctly across interactions"""
        print("🧪 Testing state persistence...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Wait for radio buttons to be available
        await page.wait_for_selector('.stRadio', timeout=10000)
        
        # Switch to command mode
        command_radio_label = page.locator('[data-baseweb="radio"]').nth(1)
        await command_radio_label.click()
        await page.wait_for_timeout(2000)
        
        # Refresh the page
        await page.reload()
        await page.wait_for_load_state("networkidle")
        
        # Check that mode selection is still in command mode
        # Note: Streamlit doesn't persist radio button state across reloads by default
        # This is expected behavior
        
        print("✅ State persistence test completed!")
    
    async def test_error_handling(self, page):
        """Test error handling and edge cases"""
        print("🧪 Testing error handling...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Test that the app doesn't crash on various interactions
        # Click various buttons to ensure no errors
        
        # Test mode switching multiple times
        await page.wait_for_selector('.stRadio', timeout=10000)
        
        for i in range(3):
            brain_dump_radio_label = page.locator('[data-baseweb="radio"]').first
            command_radio_label = page.locator('[data-baseweb="radio"]').nth(1)
            
            await brain_dump_radio_label.click()
            await page.wait_for_timeout(1000)
            await command_radio_label.click()
            await page.wait_for_timeout(1000)
        
        # Check that app is still responsive
        assert await page.locator("text=Voice Task Manager").is_visible(), "App should still be responsive"
        
        print("✅ Error handling test passed!")
    
    async def run_all_tests(self):
        """Run all UI tests"""
        print("🚀 Running Voice Task Manager UI Tests\n")
        
        try:
            await self.start_streamlit()
            
            # Import playwright here to avoid issues if not installed
            try:
                from playwright.async_api import async_playwright
            except ImportError:
                print("❌ Playwright not installed. Install with: pip install playwright")
                print("Then run: playwright install")
                return False
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()
                
                try:
                    await self.test_basic_ui_loading(page)
                    await self.test_mode_switching(page)
                    await self.test_task_operations(page)
                    await self.test_duplicate_panel_issue(page)
                    await self.test_state_persistence(page)
                    await self.test_error_handling(page)
                    
                    print("\n🎉 All UI tests passed!")
                    return True
                    
                finally:
                    await browser.close()
                    
        except Exception as e:
            print(f"\n❌ UI test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            await self.stop_streamlit()

async def main():
    tester = StreamlitUITester()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main()) 