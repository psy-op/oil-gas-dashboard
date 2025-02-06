import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_production_data(n_wells=5, days=365):
    """Generate synthetic oil and gas production data."""
    
    # Ensure output directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create date range (reversed for descending order)
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    
    data = []
    for well_id in range(1, n_wells + 1):
        # Base production with decline curve
        base_oil = np.random.uniform(100, 1000)
        base_gas = np.random.uniform(500, 5000)
        decline_rate = np.random.uniform(0.1, 0.3)  # Decline rate for production
        
        for i, date in enumerate(dates):
            time_factor = 1 / (1 + decline_rate * i / 365)  # Simulate production decline over time
            
            # Introduce daily variation and noise
            oil_production = base_oil * time_factor * (1 + np.random.normal(0, 0.1))
            gas_production = base_gas * time_factor * (1 + np.random.normal(0, 0.1))
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),  # Ensure date format is consistent
                'well_id': f'WELL_{well_id:03d}',
                'oil_production': max(0, oil_production),
                'gas_production': max(0, gas_production),
                'water_production': max(0, oil_production * np.random.uniform(0.2, 0.5)),
                'pressure': np.random.uniform(1000, 2000),
                'temperature': np.random.uniform(150, 200)
            })
    
    df = pd.DataFrame(data)
    df.to_csv("data/production_data.csv", index=False)  # Corrected file path
    return df

if __name__ == "__main__":
    df = generate_production_data()
    print(f"Generated dataset with {df.shape[0]} records.")
