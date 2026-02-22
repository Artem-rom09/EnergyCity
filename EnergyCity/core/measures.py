from dataclasses import dataclass

@dataclass
class Measure:
    name: str
    cost: float
    effect: float
    max_adoption: float

def default_measures():
    return [
        Measure("LED", 15, 0.08, 1.0),
        Measure("Insulation", 25, 0.15, 0.9),
        Measure("Solar", 30, 0.20, 0.7),
        Measure("SmartMeter", 10, 0.05, 1.0),
        Measure("SmartHome", 6, 0.03, 0.8),
    ]