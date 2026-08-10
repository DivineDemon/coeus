#!/usr/bin/env python3
"""
Verification script for the Haga UK Sponsor Job Automation verification script
"""

import sys
import os

def test_imports():
    """Test that the automation script can be imported"""
    try:
        sys.path.insert(0, "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career")
        from automate_sponsor_outreach import (
            TECH_KEYWORDS, JOB_TERMS, KNOWN_DOMAINS, PRIORITY_COMPANIES
        )
        print("��✅ Automation script imports successfully")
        return True
    except Exception as e:
        print(f"��❌ Import error: {e}")
        return False

def test_priority_companies():
    """Test priority companies structure"""
    try:
        sys.path.insert(0, "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career")
        from automate_sponsor_outreach import PRIORITY_COMPANIES, KNOWN_DOMAINS
        
        # Check we have the expected number
        assert len(PRIORITY_COMPANIES) == 17, f"Expected 17 priority companies, got {len(PRIORITY_COMPANIES)}"
        assert len(KNOWN_DOMAINS) == 17, f"Expected 17 known domains, got {len(KNOWN_DOMAINS)}"
        
        # Check structure
        for company in PRIORITY_COMPANIES:
            assert "name" in company, "Missing 'name' field"
            assert "location" in company, "Missing 'location' field"
            assert "domain" in company, "Missing 'domain' field"
            assert "keywords" in company, "Missing 'keywords' field"
            
        print("��✅ Priority companies structure is correct")
        return True
    except Exception as e:
        print(f"��❌ Priority companies test error: {e}")
        return False

def test_known_domains():
    """Test that known domains mapping is correct"""
    try:
        sys.path.insert(0, "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career")
        from automate_sponsor_outreach import KNOWN_DOMAINS
        
        # Check some key domains
        expected_domains = {
            "Shadow Robot Company Ltd.": "shadowrobot.com",
            "Apollo Research AI Ltd": "apolloresearch.ai",
            "Mistral AI UK Limited": "mistral.ai",
            "Stability AI Ltd": "stability.ai"
        }
        
        for company, domain in expected_domains.items():
            assert company in KNOWN_DOMAINS, f"Missing company: {company}"
            assert KNOWN_DOMAINS[company] == domain, f"Wrong domain for {company}: expected {domain}, got {KNOWN_DOMAINS[company]}"
            
        print("��✅ Known domains mapping is correct")
        return True
    except Exception as e:
        print(f"��❌ Known domains test error: {e}")
        return False

def test_tech_keywords():
    """Test that tech keywords are present"""
    try:
        sys.path.insert(0, "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career")
        from automate_sponsor_outreach import TECH_KEYWORDS
        
        # Check we have keywords
        assert len(TECH_KEYWORDS) > 20, f"Expected >20 tech keywords, got {len(TECH_KEYWORDS)}"
        
        # Check some key terms are present
        key_terms = ["robotics", "simulation", "ai", "machine learning", "computer vision"]
        for term in key_terms:
            assert term in TECH_KEYWORDS, f"Missing key term: {term}"
            
        print("��✅ Tech keywords are present and correct")
        return True
    except Exception as e:
        print(f"��❌ Tech keywords test error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("=" * 50)
    print("���🔍 VERIFYING HAGA AUTOMATION VERIFICATION SCRIPT")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_priority_companies,
        test_known_domains,
        test_tech_keywords
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Empty line between tests
    
    print("=" * 50)
    print(f"���📊 RESULTS: {passed}/{total} tests passed")
    if passed == total:
        print("���🎉 ALL VERIFICATION TESTS PASSED")
        print("��✅ The verify_automation.py script is working correctly")
    else:
        print("��❌ SOME TESTS FAILED")
    print("=" * 50)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)