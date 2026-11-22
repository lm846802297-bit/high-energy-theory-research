# Development task T06 — reproducibility package

Status: development only; intended for Round 2.

## Input data

Create a UTF-8 CSV file with exactly these bytes (including the final newline):

```csv
x,weight
0,1
1,2
2,1
```

## Prompt

Write a small Python program that reads the CSV and computes the weighted mean
[
\bar{x}=\frac{\sum_i w_i x_i}{\sum_i w_i}.
]

Produce a reproducibility package containing:

1. The exact Python source file and its SHA-256.
2. The exact input CSV and its SHA-256.
3. The command used to run the calculation.
4. Python version, OS, architecture, CPU model if available, and relevant package versions.
5. Native stdout/stderr and a machine-readable JSON result.
6. The computed weighted mean and an independent hand calculation.
7. A manifest that binds the input hash, source hash, environment, command, and output hashes.

Do not add dependencies if the Python standard library is sufficient. Do not claim a hardware field was measured if the host does not expose it; record null and explain.
