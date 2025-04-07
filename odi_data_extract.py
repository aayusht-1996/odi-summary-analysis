import requests
import zipfile
import io
import json
import pandas as pd

def process_matches_from_url(zip_url, output_csv_path):
    # Step 1: Download and open ZIP from URL in memory
    response = requests.get(zip_url)
    zip_bytes = io.BytesIO(response.content)

    with zipfile.ZipFile(zip_bytes, 'r') as zip_ref:
        json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
        all_matches = []

        def get_legit_overs(overs):
            total_balls = 0
            for over in overs:
                for delivery in over.get("deliveries", []):
                    extras = delivery.get("extras", {})
                    if not ("wides" in extras or "noballs" in extras):
                        total_balls += 1
            full_overs = total_balls // 6
            remaining_balls = total_balls % 6
            return f"{full_overs}.{remaining_balls}"

        def summarize_innings(innings):
            summary = {}
            for i, inning in enumerate(innings[:2]):
                team = inning.get("team", f"team_{i+1}")
                overs = inning.get("overs", [])
                total_runs = 0
                total_wickets = 0
                for over in overs:
                    for delivery in over.get("deliveries", []):
                        total_runs += delivery.get("runs", {}).get("total", 0)
                        if "wickets" in delivery:
                            total_wickets += len(delivery["wickets"])
                label = 'batting_first' if i == 0 else 'batting_second'
                summary[f"{label}_team"] = team
                summary[f"{label}_runs"] = total_runs
                summary[f"{label}_wickets"] = total_wickets
                summary[f"{label}_overs"] = get_legit_overs(overs)

            if len(innings) > 1 and "target" in innings[1]:
                target_info = innings[1]["target"]
                summary["target_runs"] = target_info.get("runs")
                summary["target_overs"] = target_info.get("overs")
            else:
                summary["target_runs"] = None
                summary["target_overs"] = None

            return summary

        def extract_info(data):
            info = data.get("info", {})
            outcome = info.get("outcome", {})
            toss = info.get("toss", {})
            innings = data.get("innings", [])

            match_data = {
                "date": info.get("dates", [None])[0],
                "event_name": info.get("event", {}).get("name"),
                "venue": info.get("venue"),
                "gender": info.get("gender"),
                "match_type": info.get("match_type"),
                "winner": outcome.get("winner"),
                "won_by_runs": outcome.get("by", {}).get("runs"),
                "won_by_wickets": outcome.get("by", {}).get("wickets"),
                "player_of_match": info.get("player_of_match", [None])[0],
                "toss_winner": toss.get("winner"),
                "toss_decision": toss.get("decision")
            }

            match_data.update(summarize_innings(innings))
            return match_data

        for file_name in json_files:
            with zip_ref.open(file_name) as f:
                data = json.load(f)
                match_info = extract_info(data)
                match_info["file_name"] = file_name
                all_matches.append(match_info)

    # Step 2: Save to CSV
    df = pd.DataFrame(all_matches)
    df.to_csv(output_csv_path, index=False)
    print(f"Data saved to {output_csv_path}")

# Example usage:
zip_url = "https://cricsheet.org/downloads/odis_json.zip"
output_csv = "odi_summary1.csv"
process_matches_from_url(zip_url, output_csv)
