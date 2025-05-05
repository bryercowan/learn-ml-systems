#!/usr/bin/env python3
"""
ML Systems Journey Module Initializer
------------------------------------
This script helps initialize the structure for a specific module.
"""

import os
import sys
import argparse
from pathlib import Path

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Initialize structure for a specific module")
    parser.add_argument("module", type=str, 
                        help="Module to initialize (e.g., 0, 1-1, 2-2, 3-1, 4-A, A, B, C)")
    return parser.parse_args()

def initialize_module(module):
    """Initialize the directory structure and files for a specific module"""
    project_root = Path(__file__).parent.parent
    
    # Determine which module we're initializing
    if "-" in module:
        module_number, sub_module = module.split("-")
    else:
        module_number = module
        sub_module = None
    
    print(f"Initializing structure for Module {module}...")
    
    # Create module-specific files and directories
    if module_number == "0":
        if sub_module == "A":
            # Module 0-A: Course Setup
            print("Creating Module 0-A: Course Setup structure...")
            (project_root / "notes").mkdir(exist_ok=True)
            with open(project_root / "notes" / "00-A.md", "w") as f:
                f.write("# Module 0-A: Course Setup\n\n3 bullets summarizing your motivation and setup experience:\n\n- \n- \n- \n")
                
        elif sub_module == "B":
            # Module 0-B: Kafka Hello-World
            print("Creating Module 0-B: Kafka Hello-World structure...")
            with open(project_root / "docker-compose.yml", "w") as f:
                f.write("""services:
  kafka:
    image: bitnami/kafka
    environment:
      - KAFKA_LISTENERS=PLAINTEXT://:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
    ports:
      - "9092:9092"
""")
            with open(project_root / "notes" / "00-B.md", "w") as f:
                f.write("# Module 0-B: Kafka Hello-World\n\nNotes on the single-broker SPOF:\n\n")
        else:
            # Module 0 Project M0 - DevBox Skeleton
            print("Creating Module 0 Project: DevBox Skeleton structure...")
            (project_root / ".devcontainer").mkdir(exist_ok=True)
            with open(project_root / "notes" / "M0-devbox.md", "w") as f:
                f.write("# Module 0 Project: DevBox Skeleton\n\nImage size and startup time:\n\n- Size: \n- Startup time: \n")
    
    elif module_number == "1":
        # Module 1: Data-Plumbing Fundamentals
        if sub_module == "1":
            print("Creating Module 1-1: Reliability Queue Chaos structure...")
            (project_root / "demos").mkdir(exist_ok=True)
            with open(project_root / "notes" / "1-1.md", "w") as f:
                f.write("# Module 1-1: Reliability Queue Chaos\n\nDisk-failure behavior:\n\n")
        elif sub_module == "2":
            print("Creating Module 1-2: SQL vs Document Benchmark structure...")
            (project_root / "data").mkdir(exist_ok=True)
            (project_root / "scripts").mkdir(exist_ok=True)
            with open(project_root / "scripts" / "query_sql.py", "w") as f:
                f.write("""#!/usr/bin/env python3
import sqlite3
import time

conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

start_time = time.time()
cursor.execute('''
SELECT * FROM movies 
ORDER BY year DESC 
LIMIT 10
''')
rows = cursor.fetchall()
elapsed = time.time() - start_time

print(f"Top 10 movies (SQL):")
for row in rows:
    print(row)
print(f"\\nQuery time: {elapsed:.4f} seconds")

conn.close()
""")
            with open(project_root / "scripts" / "query_mongo.py", "w") as f:
                f.write("""#!/usr/bin/env python3
import pymongo
import time

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["demo"]
collection = db["movies"]

start_time = time.time()
cursor = collection.find().sort("year", pymongo.DESCENDING).limit(10)
rows = list(cursor)
elapsed = time.time() - start_time

print(f"Top 10 movies (MongoDB):")
for row in rows:
    print(row)
print(f"\\nQuery time: {elapsed:.4f} seconds")

client.close()
""")
            with open(project_root / "notes" / "1-2.md", "w") as f:
                f.write("# Module 1-2: SQL vs Document Benchmark\n\nQuery latencies comparison:\n\n- SQL: \n- MongoDB: \n\nScenarios where MongoDB outperforms SQL:\n\n- \n- \n")
    
    elif module_number == "2":
        # Module 2: ML-Workflow Glue
        if sub_module == "1":
            print("Creating Module 2-1: Dataset Versioning (DVC) structure...")
            with open(project_root / "notes" / "2-1.md", "w") as f:
                f.write("# Module 2-1: Dataset Versioning (DVC)\n\nRemote backend rationale:\n\n")
        elif sub_module == "2":
            print("Creating Module 2-2: Experiment Tracking (W&B) structure...")
            with open(project_root / "train_logreg.py", "w") as f:
                f.write("""#!/usr/bin/env python3
import wandb
import subprocess
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Get git SHA
git_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

# Initialize W&B
wandb.init(project="ml-systems-journey", 
           config={
               "git_commit": git_sha,
               "model_type": "LogisticRegression",
               "dataset": "synthetic"
           })

# Generate synthetic data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Log metrics
wandb.log({
    "accuracy": accuracy,
    "n_samples": len(X),
    "n_features": X.shape[1]
})

print(f"Model trained with accuracy: {accuracy:.4f}")
print(f"Git SHA: {git_sha}")
print(f"Results logged to W&B")

# Finish the run
wandb.finish()
""")
            with open(project_root / "notes" / "2-2.md", "w") as f:
                f.write("# Module 2-2: Experiment Tracking (W&B)\n\nMetric spam notes:\n\n")
    
    elif module_number == "3":
        # Module 3: GPU-Performance Mindset
        if sub_module == "1":
            print("Creating Module 3-1: Vector Add structure...")
            with open(project_root / "vec_add.cu", "w") as f:
                f.write("""#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

// CUDA kernel for vector addition
__global__ void vectorAdd(const float *A, const float *B, float *C, int numElements) {
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    if (i < numElements) {
        C[i] = A[i] + B[i];
    }
}

int main(int argc, char **argv) {
    // Parse command line arguments
    if (argc != 2) {
        printf("Usage: %s <vector size>\\n", argv[0]);
        return 1;
    }
    int numElements = atoi(argv[1]);
    
    // Allocate memory for vectors
    size_t size = numElements * sizeof(float);
    
    float *h_A = (float *)malloc(size);
    float *h_B = (float *)malloc(size);
    float *h_C = (float *)malloc(size);
    
    // Initialize vectors
    for (int i = 0; i < numElements; i++) {
        h_A[i] = rand() / (float)RAND_MAX;
        h_B[i] = rand() / (float)RAND_MAX;
    }
    
    // Allocate device memory
    float *d_A, *d_B, *d_C;
    cudaMalloc((void **)&d_A, size);
    cudaMalloc((void **)&d_B, size);
    cudaMalloc((void **)&d_C, size);
    
    // Create events for timing
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    
    // Copy vectors from host to device
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);
    
    // Launch the CUDA kernel
    int threadsPerBlock = 256;
    int blocksPerGrid = (numElements + threadsPerBlock - 1) / threadsPerBlock;
    
    cudaEventRecord(start);
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, numElements);
    cudaEventRecord(stop);
    
    // Check for errors
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        fprintf(stderr, "Failed to launch kernel: %s\\n", cudaGetErrorString(err));
        return 1;
    }
    
    // Copy result from device to host
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);
    
    // Calculate elapsed time
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    
    // Calculate throughput (GB/s)
    float dataProcessedGB = (float)(numElements * 3 * sizeof(float)) / 1e9; // 3 arrays: A, B, C
    float throughputGBs = dataProcessedGB / (milliseconds / 1000.0);
    
    // Verify results
    bool success = true;
    for (int i = 0; i < numElements; i++) {
        if (fabs(h_A[i] + h_B[i] - h_C[i]) > 1e-5) {
            fprintf(stderr, "Result verification failed at element %d!\\n", i);
            success = false;
            break;
        }
    }
    
    printf("Vector addition of %d elements completed in %.3f ms\\n", numElements, milliseconds);
    printf("Throughput: %.2f GB/s\\n", throughputGBs);
    printf("Verification: %s\\n", success ? "PASSED" : "FAILED");
    
    // Free device memory
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    
    // Free host memory
    free(h_A);
    free(h_B);
    free(h_C);
    
    return 0;
}
""")
            with open(project_root / "bench_numpy.py", "w") as f:
                f.write("""#!/usr/bin/env python3
import numpy as np
import time
import argparse
import torch

def cpu_vector_add(size):
    # Generate random vectors
    a = np.random.rand(size).astype(np.float32)
    b = np.random.rand(size).astype(np.float32)
    
    # Warm-up
    _ = a + b
    
    # Time the operation
    start_time = time.time()
    c = a + b
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    # Calculate throughput (GB/s)
    bytes_processed = size * 3 * 4  # 3 arrays, 4 bytes per element
    throughput_gbs = (bytes_processed / 1e9) / (elapsed_ms / 1000)
    
    return elapsed_ms, throughput_gbs

def gpu_vector_add(size):
    if not torch.cuda.is_available():
        print("CUDA not available!")
        return -1, -1
    
    # Generate random vectors on GPU
    a = torch.rand(size, dtype=torch.float32, device='cuda')
    b = torch.rand(size, dtype=torch.float32, device='cuda')
    
    # Warm-up
    _ = a + b
    torch.cuda.synchronize()
    
    # Time the operation
    start_time = time.time()
    c = a + b
    torch.cuda.synchronize()
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    # Calculate throughput (GB/s)
    bytes_processed = size * 3 * 4  # 3 arrays, 4 bytes per element
    throughput_gbs = (bytes_processed / 1e9) / (elapsed_ms / 1000)
    
    return elapsed_ms, throughput_gbs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Benchmark vector addition on CPU and GPU')
    parser.add_argument('--size', type=int, default=100000000, help='Vector size')
    args = parser.parse_args()
    
    print(f"Vector addition benchmark with size: {args.size}")
    
    # CPU benchmark
    cpu_time, cpu_throughput = cpu_vector_add(args.size)
    print(f"CPU (NumPy): {cpu_time:.3f} ms, Throughput: {cpu_throughput:.2f} GB/s")
    
    # GPU benchmark
    if torch.cuda.is_available():
        gpu_time, gpu_throughput = gpu_vector_add(args.size)
        print(f"GPU (PyTorch): {gpu_time:.3f} ms, Throughput: {gpu_throughput:.2f} GB/s")
    else:
        print("GPU benchmark skipped: CUDA not available")
""")
            with open(project_root / "notes" / "3-1.md", "w") as f:
                f.write("# Module 3-1: Vector Add\n\nExplanation of why vector addition is memory-bound:\n\n")
    
    print(f"\nInitialized structure for Module {module}!")
    print(f"Check the created files and customize them for your needs.")

if __name__ == "__main__":
    args = parse_args()
    initialize_module(args.module)