# Bayesian trap
Suppose there is an infectious disease that affects 1 in 1000 people and a test kit whose false positive and false negative rates are both 5%. What is the probability that a person with a positive diagnosis actually has the disease?

## Theoretical answer
Let `D` and `I` respective denote "positive diagnosis" and "actual infection".According to Bayes' theorem:

$$
P(I \lvert D) \cdot P(D) = P(D \lvert I) \cdot P(I)
$$

We trivially know that $P(I) = 0.001$ and we know $P(D|I) = 1 - \text{false negative rate} = 0.95$.

The probability of having a positive diagnosis is summed across people with and without infection:

$$
\begin{aligned}
P(D) &= P(D \cap I) + P(D \cap \overline{I}) \\
&= P(D \lvert I) \cdot P(I) + P(D \lvert \overline{I}) \cdot P(\overline{I}) \\
&= 0.95 \cdot 0.001 + 0.05 \cdot 0.999 \\
&= 0.0509
\end{aligned}
$$

Solving the equation shows that $P(I \lvert D) \approx 0.0187$, or just a bit less than 2%.

## Empirical simulation
The theoretical answer can be a bit too jaring to immediately accept, so I wrote a quick python script to confirm. You can invoke the script with:

```
python main <sample_size> <base_rate> <false_positivity> <false_negativity>
```

Here is some result:
```bash
python main.py 1000000 0.001 0.05 0.05
{'sample size': 1000000,
 'empirical base rate': 0.000999,
 'empirical false positive': 0.05007702694992297,
 'empirical false negative': 0.049049049049049054,
 'positve diagnosis confidence': 0.018635855385762207,
 'negative diagnosis confidence': 0.9999483679531476}
```
