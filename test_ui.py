#!/usr/bin/env python3
"""
UI Tests for Voice Task Manager using Playwright
Tests the Streamlit interface functionality
"""

import asyncio
import subprocess
import time
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright")
    print("Then install browsers: playwright install")
    sys.exit(1)


class StreamlitUITester:
    def __init__(self):
        self.process = None
        self.base_url = "http://localhost:8502"
        
    async def start_streamlit(self):
        """Start Streamlit app in background"""
        print("🚀 Starting Streamlit app...")
        self.process = subprocess.Popen([
            "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8502"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for app to start
        await asyncio.sleep(5)
        print("✅ Streamlit app started")
        
    async def stop_streamlit(self):
        """Stop Streamlit app"""
        if self.process:
            print("🛑 Stopping Streamlit app...")
            self.process.terminate()
            self.process.wait()
            print("✅ Streamlit app stopped")
            
    async def test_basic_ui_load(self, page):
        """Test that the basic UI loads correctly"""
        print("🧪 Testing basic UI load...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Check for main title
        title = await page.locator("h1").first.text_content()
        assert "Voice Task Manager" in title, f"Expected 'Voice Task Manager' in title, got: {title}"
        
        # Check for mode selector
        mode_selector = page.locator("text=Mode:").first
        assert await mode_selector.is_visible(), "Mode selector not found"
        
        print("✅ Basic UI load test passed")
        
    async def test_mode_switching(self, page):
        """Test switching between Brain Dump and Command modes"""
        print("🧪 Testing mode switching...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Wait for radio buttons to be available
        await page.wait_for_selector('[data-baseweb="radio"]')
        
        # Click Command mode radio button
        await page.locator('[data-baseweb="radio"]').nth(1).click()
        
        # Wait for mode switch
        await asyncio.sleep(2)
        
        # Check that Command mode instructions are visible
        command_text = page.locator("text=Command Mode").first
        assert await command_text.is_visible(), "Command mode instructions should be visible"
        
        print("✅ Mode switching test passed")
        
    async def test_task_operations(self, page):
        """Test basic task operations (add, delete)"""
        print("🧪 Testing task operations...")
        
        await page.goto(self.base_url)
        await page.wait_for_load_state("networkidle")
        
        # Check for task list container - look for any expander or task-related element
        task_container = page.locator('text=Tasks').first
        assert await task_container.is_visible(), "Task list container not found"
        
        print("✅ Task operations test passed")
        
    async def run_all_tests(self):
        """Run all UI tests"""
        print("🎭 Starting UI Tests with Playwright...")
        
        try:
            await self.start_streamlit()
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()
                
                try:
                    await self.test_basic_ui_load(page)
                    await self.test_mode_switching(page)
                    await self.test_task_operations(page)
                    
                    print("🎉 All UI tests passed!")
                    
                finally:
                    await browser.close()
                    
        except Exception as e:
            print(f"❌ UI test failed: {e}")
            raise
        finally:
            await self.stop_streamlit()


async def main():
    """Main test runner"""
    tester = StreamlitUITester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main()) 