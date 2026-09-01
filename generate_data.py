import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Configuration
TOTAL_RECORDS = 10000
ANOMALY_RATE = 0.05  # 5% of data will have errors

# Valid reference data
ARTICLES = [f"GDPR_Art{i}" for i in range(5, 40)] + [f"AI_Act_Art{i}" for i in range(1, 20)]
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
PARTIES = [f"Company_{fake.company().replace(' ', '_').replace(',', '')}" for _ in range(50)]
TASKS = ["Data Audit", "Risk Assessment", "Breach Notification", "Vendor Review", "Policy Update"]

def generate_record(is_anomalous=False):
    """Generates a single valid or anomalous legal obligation record."""
    record = {
        "id": fake.uuid4(),
        "title": f"{random.choice(TASKS)} - {fake.catch_phrase()}",
        "party": random.choice(PARTIES),
        "severity": random.choice(SEVERITIES),
        "deadline": (datetime.now() + timedelta(days=random.randint(10, 1000))).strftime("%Y-%m-%d"),
        "article": random.choice(ARTICLES)
    }

    if is_anomalous:
        anomaly_type = random.choice(["bad_date", "missing_party", "invalid_severity", "wrong_datatype"])
        
        if anomaly_type == "bad_date":
            # AI hallucinated a human-readable date instead of ISO
            record["deadline"] = "Next Friday" 
        elif anomaly_type == "missing_party":
            # AI failed to extract the responsible entity
            record["party"] = None
        elif anomaly_type == "invalid_severity":
            # AI hallucinated a severity outside the ENUM
            record["severity"] = "URGENT"
        elif anomaly_type == "wrong_datatype":
            # AI returned an integer instead of a string title
            record["title"] = 404

    return record

if __name__ == "__main__":
    print(f"Generating {TOTAL_RECORDS} records...")
    
    dataset = []
    for _ in range(TOTAL_RECORDS):
        # Determine if this record should be an anomaly
        is_anom = random.random() < ANOMALY_RATE
        dataset.append(generate_record(is_anomalous=is_anom))
        
    # Save to disk
    with open("large_extracted_data.json", "w") as f:
        json.dump(dataset, f, indent=2)
        
    anomalies_count = int(TOTAL_RECORDS * ANOMALY_RATE)
    print(f"Done! Saved to large_extracted_data.json.")
    print(f"Injected ~{anomalies_count} anomalies to test SHACL validation.")