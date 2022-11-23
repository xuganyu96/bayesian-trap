import argparse
import pprint
from random import random
from typing import Tuple
import pandas as pd

class BayesianTrap:

    def __init__(self, n, base_rate, false_pos, false_neg):
        assert 0 <= base_rate <= 1, "base rate must be between 0 and 1"
        assert 0 <= false_pos <= 1, "false positive must be between 0 and 1"
        assert 0 <= false_neg <= 1, "false negative must be between 0 and 1"
        self.base_rate = base_rate
        self.false_pos = false_pos
        self.false_neg = false_neg
        self.n = n
        self.data = self.generate(n, base_rate, false_pos, false_neg)

    def resample(self):
        self.data = self.generate(self.n, self.base_rate, self.false_pos, self.false_neg)

    @staticmethod
    def generate(n, base_rate, false_pos, false_neg):
        """Generate data"""
        data = pd.DataFrame({
            "id": list(range(n)),
            "has_disease": [random() < base_rate for _ in range(n)],
        })

        data["diagnosis"] = data["has_disease"].apply(
            lambda d: random() < (1 - false_neg) if d else random() < false_pos
        )

        return data

    def observe(self) -> Tuple[float, float, float]:
        emp_base_rate = self.data.has_disease.mean()
        emp_false_pos = self.data.loc[~self.data.has_disease].diagnosis.mean()
        emp_false_neg = 1 - self.data.loc[self.data.has_disease].diagnosis.mean()

        return emp_base_rate, emp_false_pos, emp_false_neg

    def diagnose_pos(self) -> float:
        """Return the probability of having the disease when the test kit
        returns positive results
        """
        return self.data.loc[self.data.diagnosis].has_disease.mean()

    def diagnose_neg(self):
        """Return the probability of having the disease when the test kit
        returns negative results
        """
        return self.data.loc[~self.data.diagnosis].has_disease.mean()

    def summarize(self):
        base, pos, neg = self.observe()
        summary = {
            "sample size": self.n,
            "empirical base rate": base,
            "empirical false positive": pos, 
            "empirical false negative": neg,
            "positve diagnosis confidence": self.diagnose_pos(),
            "negative diagnosis confidence": 1 - self.diagnose_neg(),
        }
        pprint.pprint(summary, sort_dicts=False)

parser = argparse.ArgumentParser(
    prog = "bayesian-trap",
    description = """A simulation of the famous Bayesian trap involving rare
    disease and imperfect test kit""",
)

parser.add_argument("sample_size", type=int)
parser.add_argument("base_rate", type=float)
parser.add_argument("false_pos", type=float)
parser.add_argument("false_neg", type=float)

if __name__ == "__main__":
    args = parser.parse_args()
    trap = BayesianTrap(args.sample_size, args.base_rate, args.false_pos, args.false_neg)
    trap.summarize()
