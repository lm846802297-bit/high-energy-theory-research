# Development task T06 — reproducibility package

Status: development only; intended for Round 2.

## Exact input bytes

Create a UTF-8 CSV file with exactly these bytes, including the final newline:

    x,weight
    0,1
    1,2
    2,1

## Prompt

Write a small Python program that reads the CSV and computes

    xbar = sum_i(w_i*x_i) / sum_i(w_i)

Produce a reproducibility package containing:

1. The exact Python source file and its SHA-256.
2. The exact input CSV and its SHA-256.
3. The command used to run the calculation.
4. Python version, OS, architecture, CPU model if available, and relevant package versions.
5. Native stdout/stderr and a machine-readable result.json containing numeric weighted_mean.
6. The computed weighted mean and an independent hand calculation.
7. A manifest.json binding source_sha256, input_sha256, output_sha256, command, and an environment object containing python_version, os, and architecture. Do not put the manifest's own hash inside itself; it is recorded by the outer run record.

Do not add dependencies if the Python standard library is sufficient. Do not claim a hardware field was measured if the host does not expose it; record null and explain.

## Evaluator boundary

The independent evaluator verifies exact input bytes, source/input/output SHA-256 values, the manifest binding, and the numerical result by recomputing the weighted mean directly from the CSV. It does not execute model-generated source code. Execution evidence must come from the recorded task runner, command, exit status, stdout/stderr, and transcript/log artifacts.

Expected weighted mean: exactly 1.
