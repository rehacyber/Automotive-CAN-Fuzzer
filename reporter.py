import json
import csv

from pathlib import Path
from datetime import datetime


class Reporter:

    def __init__(self):

        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)

        self.mutation_results = []

    def add_mutation_result(
        self,
        can_id,
        original_data,
        mutated_data,
        mutation_mode
    ):

        result = {
            "can_id": hex(can_id),
            "original_data": original_data,
            "mutated_data": mutated_data,
            "mutation_mode": mutation_mode
        }

        self.mutation_results.append(result)

    def create_report(self, data):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        data["mutation_results"] = self.mutation_results

        json_file = self.report_dir / f"fuzz_report_{timestamp}.json"
        csv_file = self.report_dir / f"fuzz_report_{timestamp}.csv"
        html_file = self.report_dir / f"fuzz_report_{timestamp}.html"

        # -------------------------
        # JSON Report
        # -------------------------

        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        # -------------------------
        # CSV Report
        # -------------------------

        with open(csv_file, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Parameter",
                    "Value"
                ]
            )

            for key, value in data.items():
                writer.writerow([key, value])

        # -------------------------
        # HTML Report
        # -------------------------

        html = f"""
<!DOCTYPE html>
<html>

<head>
<meta charset="utf-8">
<title>Automotive CAN Fuzzer Report</title>

<style>

body {{
    font-family: Arial;
    background:#f5f5f5;
    margin:40px;
}}

table {{
    border-collapse: collapse;
    width: 80%;
}}

th, td {{
    border:1px solid #ccc;
    padding:10px;
}}

th {{
    background:#2c3e50;
    color:white;
}}

h1 {{
    color:#2c3e50;
}}

</style>

</head>

<body>

<h1>Automotive CAN Fuzzer Report</h1>

<table>

<tr>
<th>Parameter</th>
<th>Value</th>
</tr>
"""

        for key, value in data.items():

            html += f"""
<tr>
<td>{key}</td>
<td>{value}</td>
</tr>
"""

        html += """

</table>

</body>
</html>
"""

        with open(html_file, "w", encoding="utf-8") as file:
            file.write(html)

        print("[+] Reports created")
        print(f"[+] JSON : {json_file}")
        print(f"[+] CSV  : {csv_file}")
        print(f"[+] HTML : {html_file}")