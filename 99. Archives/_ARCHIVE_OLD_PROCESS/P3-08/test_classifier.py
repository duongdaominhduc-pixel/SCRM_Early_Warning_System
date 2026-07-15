import sys
sys.stdout.reconfigure(encoding='utf-8')

import unittest
from pathlib import Path

# Allow import from parent-level scripts by adding P3-08 to path
sys.path.insert(0, str(Path(__file__).parent))
from disruption_type import classify_disruption_type


class TestDisruptionTypeClassifier(unittest.TestCase):

    # ------------------------------------------------------------------
    # PORT_CONGESTION
    # ------------------------------------------------------------------
    def test_port_congestion_title(self):
        title = "Los Angeles Port Faces Severe Congestion as Ships Queue Outside Harbor"
        content = "Dozens of vessels are anchored offshore waiting for berth assignments."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'PORT_CONGESTION',
                         f"Expected PORT_CONGESTION, got {result}")

    def test_port_congestion_content_only(self):
        title = "Supply Chain Update"
        content = ("The terminal is experiencing significant congestion. Vessel delays "
                   "have pushed shipping backlogs to record levels at the dock.")
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'PORT_CONGESTION',
                         f"Expected PORT_CONGESTION, got {result}")

    # ------------------------------------------------------------------
    # GEOPOLITICAL
    # ------------------------------------------------------------------
    def test_geopolitical_sanctions(self):
        title = "US Imposes New Sanctions on Russian Energy Exports"
        content = "The embargo covers crude oil and refined petroleum products."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'GEOPOLITICAL',
                         f"Expected GEOPOLITICAL, got {result}")

    def test_geopolitical_tariff(self):
        title = "China Retaliates with Tariff Hike in Ongoing Trade War"
        content = "Import restrictions on semiconductors and rare earths are expected."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'GEOPOLITICAL',
                         f"Expected GEOPOLITICAL, got {result}")

    # ------------------------------------------------------------------
    # WEATHER_DISASTER
    # ------------------------------------------------------------------
    def test_weather_hurricane(self):
        title = "Hurricane Ian Disrupts Gulf Coast Supply Chains"
        content = "Flooding caused widespread damage to warehouses along the coastline."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'WEATHER_DISASTER',
                         f"Expected WEATHER_DISASTER, got {result}")

    def test_weather_earthquake(self):
        title = "Major Earthquake Hits Taiwan Semiconductor Hub"
        content = "The tsunami warning halted production at TSMC fabs."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'WEATHER_DISASTER',
                         f"Expected WEATHER_DISASTER, got {result}")

    # ------------------------------------------------------------------
    # LABOR_DISPUTE
    # ------------------------------------------------------------------
    def test_labor_strike(self):
        title = "Dock Workers Strike Shuts Down West Coast Ports"
        content = "The union called a walkout after contract talks collapsed."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'LABOR_DISPUTE',
                         f"Expected LABOR_DISPUTE, got {result}")

    def test_labor_content_only(self):
        title = "Logistics News Roundup"
        content = ("Workers held a walkout at three distribution centers. "
                   "The labor dispute stems from wage negotiations with the union.")
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'LABOR_DISPUTE',
                         f"Expected LABOR_DISPUTE, got {result}")

    # ------------------------------------------------------------------
    # SUPPLIER_FINANCIAL
    # ------------------------------------------------------------------
    def test_supplier_bankruptcy(self):
        title = "Tier-1 Auto Supplier Files for Bankruptcy Protection"
        content = "The company cited insolvency and financial distress after losing key contracts."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'SUPPLIER_FINANCIAL',
                         f"Expected SUPPLIER_FINANCIAL, got {result}")

    def test_supplier_chapter11(self):
        title = "Retailer Seeks Chapter 11 Restructuring Amid Debt Default"
        content = "Liquidation of non-core assets is underway to satisfy creditors."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'SUPPLIER_FINANCIAL',
                         f"Expected SUPPLIER_FINANCIAL, got {result}")

    # ------------------------------------------------------------------
    # GENERAL_DISRUPTION (fallback)
    # ------------------------------------------------------------------
    def test_general_no_keywords(self):
        title = "Supply Chain Innovation Forum 2024 Highlights"
        content = "Industry leaders gathered to discuss digital transformation strategies."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'GENERAL_DISRUPTION',
                         f"Expected GENERAL_DISRUPTION, got {result}")

    def test_general_empty_inputs(self):
        result = classify_disruption_type('', '')
        self.assertEqual(result, 'GENERAL_DISRUPTION',
                         f"Expected GENERAL_DISRUPTION, got {result}")

    # ------------------------------------------------------------------
    # Edge cases
    # ------------------------------------------------------------------
    def test_title_wins_over_content(self):
        """Title clearly says hurricane; content has mild labor keywords."""
        title = "Typhoon Mawar Devastates Philippine Supply Routes"
        content = "Unions are monitoring the situation and may call a shutdown."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'WEATHER_DISASTER',
                         f"Expected WEATHER_DISASTER (title priority), got {result}")

    def test_none_values_handled(self):
        """NaN-like None values should not crash."""
        result = classify_disruption_type(None, None)  # type: ignore
        self.assertEqual(result, 'GENERAL_DISRUPTION',
                         f"Expected GENERAL_DISRUPTION for None inputs, got {result}")

    def test_case_insensitive(self):
        title = "STRIKE AND LOCKOUT AT MAJOR UNION FACILITY"
        content = "WORKERS STAGED A WALKOUT DEMANDING HIGHER WAGES."
        result = classify_disruption_type(title, content)
        self.assertEqual(result, 'LABOR_DISPUTE',
                         f"Expected LABOR_DISPUTE (case-insensitive), got {result}")


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDisruptionTypeClassifier)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
