# ML Systems Journey

### Quick Note
* I created this with ChatGPT, if this note is here it probably needs tweaks that I will be adding moving forward
* I also am using arch, so if its needed it will be geared towards that at first. If more support is needed I will come back

> Complete **Core Path** (\~150 h) and optional **Full‑Book Track**
>
> **Sources:** *Designing Data‑Intensive Applications* (17ᵗʰ ed, 12 chapters) • *Programming Massively Parallel Processors* (4ᵗʰ ed, 23 chapters) • **stas00/ml‑engineering**

---

## Legend

| Element                 | Description                                        |
| ----------------------- | -------------------------------------------------- |
| **Reading**             | Finish before coding (< 30 pp)                     |
| **Skill Objective**     | Key concept + minimal example                      |
| **Quick‑Start**         | Copy‑paste Bash commands to bootstrap the exercise |
| **Acceptance Criteria** | ✅ Tests you can run to confirm completion          |
| **Debrief**             | Save reflections in `notes/*`                      |
| **Effort**              | `R` read h · `B` build h · `Rƒ` reflect h          |

---

## CORE PATH (\~150 h)

### Module 0 — ON‑RAMP (\~6 h)

#### 00‑A Course Setup (R 1 · B 2 · Rƒ 0.5)

* **Reading:** Prefaces of DDIA & PMPP; review `ml-eng` README
* **Skill Objective:** Map each resource → pain point (e.g., “DDIA = safe data”)
* **Quick‑Start:**
* I use uv, feel free to swap in pip

  ```bash
  git init ml-systems-journey && cd $_
  echo "# ML Systems Journey" > README.md
  mkdir ddia ml-eng pmpp notes
  uv init
  docker run --rm -it --gpus all -v $PWD:/ws -w /ws nvcr.io/nvidia/pytorch:24.03-py3 bash
  ```
* **Acceptance Criteria:**

  * [ ] Local repo initialized with `README.md` containing project title
  * [ ] Remote origin added and `git push` succeeds
  * [ ] Inside container, Python REPL returns `True` for:

    ```python
    import torch
    torch.cuda.is_available()
    ```
* **Debrief:** Write 3 bullets in `notes/00-A.md` summarizing your motivation and setup experience

---

#### 00‑B Kafka Hello‑World (R 0.5 · B 1.5 · Rƒ 0.5)

* **Reading:** “Kafka in 5 min” blog post
* **Skill Objective:** Understand queue decoupling (producer/consumer resilience)
* **Quick‑Start:**
* Everything needed:
    ```bash
    yay -S docker-compose kcat-cli uv
    ```
    ```bash
    uv add kafka-python
    ```


  ```bash
  cat <<EOF > docker-compose.yml
    services:
      kafka:
        image: bitnami/kafka:latest
        ports:
          - "9092:9092"
        environment:
          - KAFKA_CFG_NODE_ID=0
          - KAFKA_CFG_PROCESS_ROLES=controller,broker
          - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
          - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
          - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
          - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
          - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
          - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092   
          - ALLOW_PLAINTEXT_LISTENER=yes                               

  EOF
  docker-compose up --detach
  docker-compose exec kafka \                                                                                      
    kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --create \
    --topic demo \
    --partitions 1 \
    --replication-factor 1
  uv add kafka-python
  uv run --with 'kafka-python>=2.0' python - <<'PY'
    import json, uuid, random, time, signal, sys
    from kafka import KafkaProducer, errors

    BOOTSTRAP = "localhost:9092"   
    TOPIC     = "demo"             
    INTERVAL  = 1.0                

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode(),
        request_timeout_ms=5000,   
    )

    def shutdown(*_):
        print("\n↩ flushing and closing …")
        producer.flush()
        producer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        payload = {"id": str(uuid.uuid4()), "v": random.random()}
        try:
            meta = producer.send(TOPIC, payload).get(timeout=5)
            print(f"✓ {payload['id']} → {meta.topic}:{meta.partition}@{meta.offset}")
        except errors.KafkaError as exc:
            print("send failed:", exc)
        time.sleep(INTERVAL)
    PY
  ```
    run in a separate terminal
  ```bash
  kcat -b localhost:9092 -t demo -C &
  sleep 3 && docker stop kafka && sleep 5 && docker start kafka
  ```
* **Acceptance Criteria:**

  * [ ] `docker compose ps` shows Kafka container running
  * [ ] Producer script writes at least 5 messages without error
  * [ ] After stopping & restarting Kafka, consumer resumes at last offset (no duplicates or gaps)
* **Debrief:** Note the single‑broker SPOF in `notes/00-B.md`

---

#### Module 0 Project M0 — DevBox Skeleton (B 2 · Rƒ 0.5)

* **Quick‑Start:**

  ```bash
  cp -r .devcontainer_template .devcontainer
  make test-dev
  ```
* **Acceptance Criteria:**

  * [ ] `.devcontainer` folder created
  * [ ] `make test-dev` prints **DevBox ready** in CI logs
* **Debrief:** Record image size and startup time in `notes/M0-devbox.md`

---

### Module 1 — DATA‑PLUMBING FUNDAMENTALS (DDIA 1–6) (\~40 h)

Each lesson follows the same pattern—here’s a reformatted example. Apply to all sub‑lessons.

#### 1‑1 Reliability Queue Chaos (R 1.5 · B 2 · Rƒ 0.5)

* **Reading:** DDIA Ch 1
* **Skill Objective:** Reliability vs. scalability trade‑offs in queuing
* **Quick‑Start:**

  ```bash
  asciinema rec demos/1-1.cast &
  ./chaos.sh  # stops & starts Kafka twice
  ```
* **Acceptance Criteria:**

  * [ ] Asciinema recording saved to `demos/1-1.cast`
  * [ ] Recording shows consumer recovering without message gaps
  * [ ] Consumer lag remains ≤ backlog size throughout chaos
* **Debrief:** Describe disk‐failure behavior in `notes/1-1.md`

#### 1‑2 SQL vs Document Benchmark (R 2 · B 2 · Rƒ 0.5)

* **Reading:** DDIA Ch 2
* **Skill Objective:** Data model selection based on workload
* **Quick‑Start:**

  ```bash
  wget -O data/movies.csv https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.csv
  sqlite3 movies.db ".mode csv" ".import data/movies.csv movies"
  docker run -d --name mongo -p 27017:27017 mongo
  mongoimport --db demo --collection movies --type csv --headerline --file data/movies.csv
  python scripts/query_sql.py
  python scripts/query_mongo.py
  ```
* **Acceptance Criteria:**

  * [ ] Both SQL and Mongo queries return identical top‑10 movie lists
  * [ ] Query latencies logged and compared in `notes/1-2.md`
* **Debrief:** Note scenarios where Mongo outperforms SQL

> **Tip:** Replicate this formatting for lessons 1‑3 through 1‑6.

---

### Module 2 — ML‑WORKFLOW GLUE (\~28 h)

Follow the same structure: reading, objective, quick‑start, acceptance checklist, debrief.

> **Examples for 2‑1 and 2‑2:**

#### 2‑1 Dataset Versioning (DVC) (R 1 · B 2 · Rƒ 0.5)

* **Reading:** ml‑eng “Data versioning”
* **Skill Objective:** Track changes to large datasets
* **Quick‑Start:**

  ```bash
  pip install 'dvc[s3]'
  dvc init && dvc add data/movies.csv
  dvc remote add -d local /tmp/dvcstore && dvc push
  truncate -s 0 data/movies.csv && dvc status && dvc checkout
  ```
* **Acceptance Criteria:**

  * [ ] `dvc status` reports changes after truncation
  * [ ] `dvc checkout` restores original `movies.csv`
* **Debrief:** Document chosen remote backend rationale

#### 2‑2 Experiment Tracking (W\&B) (R 1 · B 2 · Rƒ 0.5)

* **Reading:** ml‑eng “Experiment tracking”
* **Skill Objective:** Log metrics and code version
* **Quick‑Start:**

  ```bash
  pip install wandb scikit-learn
  python train_logreg.py  # logs metrics + git SHA
  ```
* **Acceptance Criteria:**

  * [ ] New run appears in WandB dashboard
  * [ ] Commit SHA matches local `git rev-parse HEAD`
* **Debrief:** Note any metric spam in `notes/2-2.md`

---

### Module 3 — GPU‑PERFORMANCE MINDSET (\~32 h)

#### 3‑1 Vector Add (R 2 · B 2 · Rƒ 0.5)

* **Reading:** PMPP Ch 2
* **Skill Objective:** Measure memory‑bound speedup on GPU vs. CPU
* **Quick‑Start:**

  ```bash
  nvcc -O3 -o vec_add vec_add.cu
  ./vec_add 100000000
  python bench_numpy.py
  ```
* **Acceptance Criteria:**

  * [ ] `nvcc` compiles without errors and produces `vec_add` binary
  * [ ] Running `./vec_add 100000000` completes in < 2 s on GPU
  * [ ] `bench_numpy.py` reports GPU throughput ≥ 100 GB/s and CPU (numpy) throughput ≤ 20 GB/s
* **Debrief:** Explain why vector addition is memory‑bound in `notes/3-1.md`

#### 3‑2 Tiled Mat‑Mul (R 2 · B 4 · Rƒ 1)

* **Reading:** PMPP Ch 3
* **Skill Objective:** Implement shared‑memory tiling for matrix multiplication
* **Quick‑Start:**

  ```bash
  nvcc -O3 -o matmul matmul.cu && ./matmul 1024
  nsys profile ./matmul 1024
  ```
* **Acceptance Criteria:**

  * [ ] `matmul` binary runs for size 1024 without errors
  * [ ] Profiling report (`nsys`) shows > 20× speedup over CPU implementation
  * [ ] Roofline plot (from profile) demonstrates compute‑bound performance
* **Debrief:** Justify tile size choice in `notes/3-2.md`

#### 3‑3 Occupancy Tuner (R 1.5 · B 3 · Rƒ 0.5)

* **Reading:** PMPP Ch 4
* **Skill Objective:** Tune block size to maximize GPU occupancy
* **Quick‑Start:**

  ```bash
  ./tune_blocks.sh > blocks.csv
  python plot_blocks.py
  ```
* **Acceptance Criteria:**

  * [ ] `blocks.csv` contains timing for block sizes \[32,64,128,256]
  * [ ] `plot_blocks.py` generates a chart showing an optimal block size
  * [ ] Document optimal block size and occupancy in `notes/3-3.md`
* **Debrief:** Discuss occupancy vs ILP trade‑offs

#### 3‑4 Warp Shuffle Reduction (R 1.5 · B 3 · Rƒ 0.5)

* **Reading:** PMPP Ch 5
* **Skill Objective:** Use warp‑shuffle for intra‑warp reduction
* **Quick‑Start:**

  ```bash
  nvcc -O3 -o reduce_shfl reduce_shfl.cu
  ./reduce_shfl 1000000
  ```
* **Acceptance Criteria:**

  * [ ] `reduce_shfl` runs without error on 1e6 elements
  * [ ] Measured throughput ≥ 1.8× that of shared‑memory reduction
  * [ ] Include benchmark results in `notes/3-4.md`
* **Debrief:** Explain why shuffle is faster than shared memory

#### 3‑5 Prefix‑Sum Scan (R 1.5 · B 3 · Rƒ 0.5)

* **Reading:** PMPP Ch 6
* **Skill Objective:** Implement multi‑block inclusive scan with cooperative groups
* **Quick‑Start:**

  ```bash
  nvcc -O3 -o scan scan.cu && ./scan 1000000
  ```
* **Acceptance Criteria:**

  * [ ] `scan` binary executes on 1e6 inputs without failures
  * [ ] Results match a CPU prefix‑sum reference implementation
  * [ ] Latency and throughput metrics logged in `notes/3-5.md`
* **Debrief:** Note multi‑block synchronization limits

#### 3‑6 Ring All‑Reduce (R 2 · B 3 · Rƒ 1)

* **Reading:** PMPP Ch 9
* **Skill Objective:** Measure all‑reduce bandwidth using NCCL tests
* **Quick‑Start:**

  ```bash
  git clone https://github.com/NVIDIA/nccl-tests && make MPI=0
  ./build/all_reduce_perf -b 8 -e 512M -f 2 -g 1
  ```
* **Acceptance Criteria:**

  * [ ] NCCL test builds and runs without errors
  * [ ] Reported bandwidth ≥ 200 GB/s for 512 MB transfers
  * [ ] Save performance output to `notes/3-6.md`
* **Debrief:** Compare ring vs tree topology impact

---

### Module 4 — CAPSTONE “Vector‑Aware Fine‑Tuner” (\~50 h)

#### 4‑A Data Plane Ready (R 2 · B 10 · Rƒ 1)

* **Reading:** DDIA Ch 7–8 skim
* **Skill Objective:** Stream Kafka → ClickHouse + snapshot export
* **Quick‑Start:**

  ```bash
  docker compose -f stacks/dataplane.yml up -d
  cargo run -p stream_to_ch
  python snapshot.py
  ```
* **Acceptance Criteria:**

  * [ ] Kafka topic ingestion lag < 5 s at 10 MB/s sustained
  * [ ] ClickHouse table populated with correct records
  * [ ] `snapshot.py` generates a Parquet file in `snapshots/`
* **Debrief:** Discuss retention strategy in `notes/4-A.md`

#### 4‑B Training Pipeline (R 2 · B 14 · Rƒ 2)

* **Reading:** ml‑eng distributed deep dive
* **Skill Objective:** Build and execute Prefect flow with custom kernels
* **Quick‑Start:**

  ```bash
  prefect deployment build flows/capstone.py:flow -n local
  prefect deployment run flow/local
  ```
* **Acceptance Criteria:**

  * [ ] Prefect UI shows flow state **Completed**
  * [ ] W\&B dashboard displays loss curve for custom kernels
  * [ ] `nvprof` trace confirms kernel execution
* **Debrief:** Analyze throughput vs baseline in `notes/4-B.md`

#### 4‑C Model Serving (R 1 · B 10 · Rƒ 1)

* **Reading:** vLLM & GGML docs
* **Skill Objective:** Deploy FastAPI REST + gRPC endpoints
* **Quick‑Start:**

  ```bash
  docker build -f serve.Dockerfile -t fine-tuner-serve .
  docker run -p 8080:8080 fine-tuner-serve
  ```
* **Acceptance Criteria:**

  * [ ] HTTP `/chat` endpoint returns valid JSON response within 200 ms
  * [ ] gRPC client example (`grpc_client.py`) runs without errors
  * [ ] Memory usage < 2 GB during inference
* **Debrief:** Record footprint and latency in `notes/4-C.md`

#### 4‑D Observability & CI (R 1 · B 8 · Rƒ 1)

* **Reading:** ml‑eng monitoring + GitHub Actions docs
* **Skill Objective:** Automate test suite and metrics dashboard
* **Quick‑Start:**

  ```bash
  echo "name: CI
  on: [push]
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
        - run: pip install pytest && pytest" > .github/workflows/ci.yml
  docker compose -f stacks/monitor_capstone.yml up -d
  ```
* **Acceptance Criteria:**

  * [ ] GitHub Action run shows **✅** for pytest
  * [ ] Grafana dashboard displays FLOPS & TPS metrics
* **Debrief:** Write alert rule rationale in `notes/4-D.md`

#### 4‑E Storytelling Launch (R 0.5 · B 8 · Rƒ writing)

* **Reading:** none
* **Skill Objective:** Communicate project value effectively
* **Quick‑Start:**

  ```bash
  echo "Capstone deep dive" > docs/blog.md
  # record 2-min screencast
  ```
* **Acceptance Criteria:**

  * [ ] `docs/blog.md` published to static site without errors
  * [ ] Screencast uploaded and linked in `README.md`
* **Debrief:** Capture launch stats in `notes/4-E.md`

---

## FULL‑BOOK TRACK (optional)

### Module A — DDIA 7‑12 Project “Bank‑grade Ledger” (\~32 h)

* **Quick‑Start:**

  ```bash
  docker compose -f stacks/ledger.yml up -d
  cargo run -p ledger_api
  python simulate_transfers.py
  ```
* **Acceptance Criteria:**

  * [ ] Ledger service processes 1 k transactions/sec without error
  * [ ] Funds remain balanced under random chaos tests
  * [ ] Batch vs. stream reconciliation diff ≤ \$0.01
* **Debrief:** 1 500‑word architecture report in `notes/A-ledger.md`

### Module B — PMPP 1 & 7‑23 Project “GPU Workbench” (\~48 h)

* **Quick‑Start:**

  ```bash
  mkdir gpu-workbench && cd $_
  ./bootstrap.sh
  ./run_all_bench.sh > results.md
  ```
* **Acceptance Criteria:**

  * [ ] ILP profiler outputs GFLOPS for vector add, matmul, scan
  * [ ] SparseSuite benchmarks complete successfully
  * [ ] README badge displays consolidated GFLOPS metrics
* **Debrief:** Summarize per-tool optimizations in `notes/B-workbench.md`

### Module C — ml‑eng Extras Project “Prod‑Ready MLOps” (\~20 h)

* **Quick‑Start:**

  ```bash
  gh workflow enable cd.yml
  ./infra/deploy_blue_green.sh
  feast apply
  ```
* **Acceptance Criteria:**

  * [ ] Blue‑green deployment completes in < 3 min
  * [ ] ZAP scan reports 0 critical vulnerabilities
  * [ ] Cost alert triggers at \$5/day threshold
* **Debrief:** Capture prod‑hardening lessons in `notes/C-mlops.md`
