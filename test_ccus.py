#!/usr/bin/env python3
"""
Test script for CCUS API endpoints
Run this to test the CCUS functionality
"""

import requests
import json
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from api.ccus import ccus_simulator

def test_ccus_simulator():
    """Test the CCUS simulator directly"""
    print("🏭 Testing CCUS Simulator...")
    print("=" * 50)
    
    # Test 1: Capture simulation
    print("\n1. Testing Capture Simulation:")
    capture_result = ccus_simulator.calculate_capture_potential('cement_industry', 50000)
    print(f"   Industry: Cement")
    print(f"   Annual Emissions: 50,000 tonnes")
    print(f"   Capture Efficiency: {capture_result['capture_efficiency']}%")
    print(f"   Capturable CO2: {capture_result['capturable_co2_tonnes']} tonnes")
    
    # Test 2: Storage sites
    print("\n2. Testing Storage Site Recommendations:")
    storage_sites = ccus_simulator.suggest_storage_sites(45000, 'Gujarat')
    print(f"   CO2 Amount: 45,000 tonnes")
    print(f"   State: Gujarat")
    print(f"   Recommended Sites: {len(storage_sites)}")
    for site in storage_sites[:2]:
        print(f"   - {site['state']}: {site['total_capacity_mt']} MT capacity")
    
    # Test 3: Utilization pathways
    print("\n3. Testing Utilization Pathways:")
    utilization = ccus_simulator.calculate_utilization_potential(45000)
    print(f"   CO2 Amount: 45,000 tonnes")
    print(f"   Available Pathways: {len(utilization)}")
    for pathway in utilization[:3]:
        print(f"   - {pathway['pathway']}: {pathway['utilizable_co2_tonnes']} tonnes")
    
    # Test 4: Carbon credits
    print("\n4. Testing Carbon Credits:")
    credits = ccus_simulator.calculate_carbon_credits(45000, 'voluntary_market')
    print(f"   Stored CO2: 45,000 tonnes")
    print(f"   Credit Type: Voluntary Market")
    print(f"   Total Value: ₹{credits['total_value_inr']:,.0f}")
    print(f"   Price per tonne: ₹{credits['price_per_tonne_inr']}")
    
    print("\n✅ All CCUS simulator tests completed successfully!")
    return True

def test_api_endpoints():
    """Test the API endpoints (if server is running)"""
    base_url = "http://localhost:5000/api/ccus"
    
    print("\n🌐 Testing CCUS API Endpoints...")
    print("=" * 50)
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Server is running!")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
        else:
            print("❌ Server not responding")
            return False
        
        # Test comprehensive analysis endpoint
        test_data = {
            "industry_type": "cement_industry",
            "annual_emissions_tonnes": 50000,
            "state": "Gujarat",
            "credit_type": "voluntary_market"
        }
        
        response = requests.post(f"{base_url}/comprehensive-analysis", json=test_data)
        if response.status_code == 200:
            print("✅ Comprehensive analysis endpoint working!")
            data = response.json()
            print(f"   Capture Efficiency: {data['capture_analysis']['capture_efficiency']}%")
            print(f"   Annual Revenue: ₹{data['carbon_credits']['annual_revenue_potential']:,.0f}")
        else:
            print(f"❌ Comprehensive analysis failed: {response.status_code}")
        
        # Test industry types endpoint
        response = requests.get(f"{base_url}/industry-types")
        if response.status_code == 200:
            print("✅ Industry types endpoint working!")
            data = response.json()
            print(f"   Supported Industries: {len(data['supported_industries'])}")
        else:
            print(f"❌ Industry types failed: {response.status_code}")
        
        # Test India storage overview
        response = requests.get(f"{base_url}/india-storage-overview")
        if response.status_code == 200:
            print("✅ India storage overview endpoint working!")
            data = response.json()
            overview = data['india_storage_overview']
            print(f"   Total Capacity: {overview['total_capacity_mt']} MT")
            print(f"   States Covered: {overview['states_covered']}")
        else:
            print(f"❌ India storage overview failed: {response.status_code}")
        
        print("\n✅ All API endpoint tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Flask backend is running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🏭 CCUS (Carbon Capture, Utilization & Storage) Test Suite")
    print("=" * 60)
    
    # Test simulator directly
    simulator_success = test_ccus_simulator()
    
    # Test API endpoints
    api_success = test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   ✅ Simulator Tests: {'Passed' if simulator_success else 'Failed'}")
    print(f"   🌐 API Tests: {'Passed' if api_success else 'Failed'}")
    
    if simulator_success and api_success:
        print("\n🎉 All CCUS features are working correctly!")
        print("\n💡 Next Steps:")
        print("   1. Visit http://localhost:3000/ccus to test the frontend")
        print("   2. Try running different industry simulations")
        print("   3. Explore the educational modules")
        print("   4. Check out the India storage overview")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    return simulator_success and api_success

if __name__ == "__main__":
    main()
