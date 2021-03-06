"""
Generate rarities JSON from APK CSV source.
"""

import csv
import json
import os

from .base import BaseGen
from .util import camelcase_split


class Rarities(BaseGen):
    def __init__(self, config):
        super().__init__(config)

    def run(self):
        """Generate rarities jsons"""
        rarities = []
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.rarities)
        fields = [
            "Name", "LevelCount", "RelativeLevel", "MirrorRelativeLevel", "CloneRelativeLevel", "DonateCapacity",
            "SortCapacity",
            "DonateReward", "DonateXP", "GoldConversionValue", "ChanceWeight", "BalanceMultiplier", "UpgradeExp",
            "UpgradeMaterialCount", "UpgradeCost", "PowerLevelMultiplier", "RefundGems"
        ]

        def value(v):
            if str(v).isdigit():
                return int(v)
            return v

        with open(csv_path, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rarity = None
            for i, row in enumerate(reader):
                if i > 0:
                    name = row.get('Name')
                    if name != '':
                        if rarity is not None:
                            rarities.append(rarity)
                        rarity = {'_'.join(camelcase_split(k)).lower(): value(v) for k, v in row.items() if k in fields}
                    else:
                        vals = {'_'.join(camelcase_split(k)).lower(): value(v) for k, v in row.items() if
                                k in fields and v != ''}
                        for k, v in vals.items():
                            if not isinstance(rarity[k], list):
                                rarity[k] = [rarity[k]]
                            rarity[k].append(v)

        json_path = os.path.join(self.config.json.base, self.config.json.rarities)
        with open(json_path, 'w') as f:
            json.dump(rarities, f, indent=4)

        print(json_path)


