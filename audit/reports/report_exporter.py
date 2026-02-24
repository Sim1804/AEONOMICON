import json


class ReportExporter:
    def export(self, report, path):
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
