#!/usr/bin/env python3
"""
Test script for the Sales Agent System
Run this to verify your setup is working correctly.
"""

import asyncio
import os
import sys
import importlib.util
from pathlib import Path

# Import the openai-agents module
spec = importlib.util.spec_from_file_location("openai_agents", Path(__file__).parent / "openai-agents.py")
if spec is None or spec.loader is None:
    print("❌ Could not find openai-agents.py. Make sure it's in the same directory.")
    sys.exit(1)

openai_agents = importlib.util.module_from_spec(spec)
spec.loader.exec_module(openai_agents)

SalesAgentSystem = openai_agents.SalesAgentSystem
EmailConfig = openai_agents.EmailConfig


async def test_configuration():
    """Test that configuration loads properly"""
    print("🔧 Testing configuration...")
    
    try:
        config = EmailConfig.from_env()
        print(f"✅ Configuration loaded successfully")
        print(f"   From email: {config.from_email}")
        print(f"   To email: {config.default_to_email}")
        print(f"   SendGrid API key: {'configured' if config.sendgrid_api_key else 'NOT CONFIGURED'}")
        
        if not config.sendgrid_api_key:
            print("⚠️  WARNING: SendGrid API key not configured. Email sending will fail.")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


async def test_agent_initialization():
    """Test that agents can be initialized"""
    print("\n🤖 Testing agent initialization...")
    
    try:
        config = EmailConfig.from_env()
        sales_system = SalesAgentSystem(config)
        print("✅ All agents initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Agent initialization error: {e}")
        return False


async def test_email_generation_dry_run():
    """Test email generation without actually sending"""
    print("\n📧 Testing email generation (dry run)...")
    
    try:
        # Create a test config with dummy SendGrid key for dry run
        config = EmailConfig(
            from_email="test@example.com",
            default_to_email="test@example.com", 
            sendgrid_api_key="dummy_key_for_testing"
        )
        
        sales_system = SalesAgentSystem(config)
        
        # This will test the agent workflow but fail at email sending
        # which is expected for a dry run
        message = "Generate a test cold sales email for validation purposes"
        print(f"   Testing with message: {message}")
        
        # We expect this to fail at the email sending step, which is OK for testing
        result = await sales_system.generate_and_send_email(message)
        
        if result["status"] == "error" and "Email service not configured" in result.get("message", ""):
            print("✅ Email generation workflow completed (failed at sending as expected)")
            return True
        elif result["status"] == "success":
            print("✅ Email generation and sending completed successfully")
            return True
        else:
            print(f"❌ Unexpected result: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Email generation error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Sales Agent System - Production Readiness Test\n")
    
    tests = [
        ("Configuration", test_configuration),
        ("Agent Initialization", test_agent_initialization), 
        ("Email Generation", test_email_generation_dry_run),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results:
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if passed_test:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready for production.")
    else:
        print("⚠️  Some tests failed. Please check the configuration and setup.")
        print("\nCommon issues:")
        print("- Missing .env file (copy from .env.template)")
        print("- Invalid SendGrid API key")
        print("- Invalid email addresses")
        print("- Missing required dependencies")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
