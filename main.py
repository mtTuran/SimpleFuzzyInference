import json
from InferenceEngine import InferenceEngine
import pandas as pd

if __name__ == '__main__':

    config_path = "FuzzySystemDefinition.json"
    with open(config_path) as f:
        json_dict = json.load(f)
    engine = InferenceEngine(json_dict)

    test_cases = [
        {
            "market_value": 950,
            "location": 9.5,
            "assets": 900,
            "salary": 95,
            "interest_rate": 1.5
        },

        {
            "market_value": 150,
            "location": 2.0,
            "assets": 50,
            "salary": 15,
            "interest_rate": 8.5
        },

        {
            "market_value": 500,
            "location": 5.0,
            "assets": 500,
            "salary": 50,
            "interest_rate": 5.0
        },

        {
            "market_value": 800,
            "location": 8.0,
            "assets": 100,
            "salary": 30,
            "interest_rate": 4.0
        },

        {
            "market_value": 250,
            "location": 3.5,
            "assets": 850,
            "salary": 80,
            "interest_rate": 2.5
        },

        {
            "market_value": 600,
            "location": 7.0,
            "assets": 50,
            "salary": 90,
            "interest_rate": 4.5
        },

        {
            "market_value": 700,
            "location": 6.0,
            "assets": 950,
            "salary": 20,
            "interest_rate": 3.0
        },

        {
            "market_value": 400,
            "location": 9.0,
            "assets": 400,
            "salary": None,  
            "interest_rate": 6.0
        },

        {
            "market_value": 900,    # since the rules are not exhaustive, when market value or location information is missing
            "location": None,       # the rules fire in a way that the house evaluation is equal to 0 even if the market value
            "assets": 600,          # or location is actually good.
            "salary": 60,
            "interest_rate": 5.5
        },

        {
            "market_value": None, 
            "location": 4.0,
            "assets": 200,
            "salary": 85,
            "interest_rate": None 
        },

        {
            "market_value": None,       
            "location": None,
            "assets": 200,
            "salary": 85,
            "interest_rate": None 
        }
    ]

    results = []
    for i, case in enumerate(test_cases):
        case_result = engine(case)
        merged_inp_out = case.copy()
        merged_inp_out.update(case_result)
        results.append(merged_inp_out)

        print(f"\n--- TEST CASE {i+1} ---")
        print(f"Inputs: {case}")
        print(f"Results: {case_result}")
        print("Fired Rule Chain:")
        
        trace = engine.get_execution_trace()
        for entry in trace:
            print(f"  [{entry['rule_type']}] Strength: {entry['strength']} | {entry['logic']}")
    
    df = pd.DataFrame(results)
    print(df)
