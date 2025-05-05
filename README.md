# ML Systems Journey
Sources: *Designing Data‑Intensive Applications* 17ᵗʰ (12 chapters) • *Programming Massively Parallel Processors* 4ᵗʰ (23 chapters) • **stas00/ml‑engineering**

---
### Quick Note
I created this with ChatGPT, so its gonna need tweaking. I will tweak it as I go through it but if this note is here, expect issues.
---

## Legend

**Reading** – finish before coding (< 30 pp)
**Skill Objective** – idea you can explain + tiny example
**Mini‑Project Quick‑Start** – indented Bash you can copy‑run
**Acceptance Criteria** – bullet tests to pass
**Debrief** – short reflection you save in `notes/*`
**Effort** – `R` read h · `B` build h · `Rƒ` reflect h

---

## CORE PATH ≈ 150 h

### Module 0 — ON‑RAMP ≈ 6 h

##### 00‑A Course Setup  (R 1 · B 2 · Rƒ 0.5)

*Reading* Prefaces DDIA& PMPP; ml‑eng README
*Skill Objective* map each resource → pain (ex “DDIA = safe data”)
*Quick‑Start*

```bash
git init ml-systems-journey && cd $_
echo "# ML Systems Journey" > README.md
mkdir ddia ml-eng pmpp notes
docker run --rm -it --gpus all -v $PWD:/ws -w /ws nvcr.io/nvidia/pytorch:24.03-py3 bash
```

*Acceptance Criteria* repo pushed · expectations note · `torch.cuda.is_available()` True
*Debrief* 3 bullets: personal motivation

##### 00‑B Kafka Hello‑World  (R 0.5 · B 1.5 · Rƒ 0.5)

*Reading* short blog “Kafka in 5 min”
*Skill Objective* queue decoupling (consumer crash ≠ data loss)
*Quick‑Start*

```bash
printf "services:
  kafka:
    image: bitnami/kafka
    environment:
      - KAFKA_LISTENERS=PLAINTEXT://:9092
      - ALLOW_PLAINTEXT_LISTENER=yes
    ports: [\"9092:9092\"]
" > docker-compose.yml
docker compose up -d
pip install kafka-python kcat
python - <<'PY'
from kafka import KafkaProducer;import json,uuid,random,time
p=KafkaProducer(bootstrap_servers="localhost:9092",
                value_serializer=lambda v: json.dumps(v).encode())
while True:
    p.send("demo",{"id":str(uuid.uuid4()),"v":random.random()});p.flush();time.sleep(1)
PY
kcat -b localhost:9092 -t demo -C &
sleep 3 && docker stop kafka && sleep 5 && docker start kafka
```

*Acceptance Criteria* consumer resumes gap‑free · lag seconds recorded
*Debrief* note single‑broker SPOF

##### Module 0 Project M0 DevBox Skeleton  (B 2 · Rƒ 0.5)

*Quick‑Start*

```bash
cp -r .devcontainer_template .devcontainer
make test-dev
```

*Acceptance Criteria* container builds · `make test-dev` prints **DevBox ready**
*Debrief* container image size & startup time

---

### Module 1 — DATA‑PLUMBING FUNDAMENTALS (DDIA 1‑6) ≈ 40 h

##### 1‑1 Reliability Queue Chaos  (R 1.5 · B 2 · Rƒ 0.5)

*Reading* DDIA Ch 1
*Skill Objective* reliability vs. scalability (example queue)
*Quick‑Start*

```bash
asciinema rec demos/1-1.cast &
./chaos.sh   # script: stop & start kafka twice
```

*Acceptance Criteria* asciinema shows gap‑free recovery · consumer lag ≤ backlog
*Debrief* what happens if disk fails

##### 1‑2 SQL vs Document Benchmark  (R 2 · B 2 · Rƒ 0.5)

*Reading* DDIA Ch 2
*Skill Objective* choose data model
*Quick‑Start*

```bash
wget -O data/movies.csv https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.csv
sqlite3 movies.db ".mode csv" ".import data/movies.csv movies"
docker run -d --name mongo -p 27017:27017 mongo
mongoimport --db demo --collection movies --type csv --headerline --file data/movies.csv
python scripts/query_sql.py && python scripts/query_mongo.py
```

*Acceptance Criteria* identical lists · latencies noted
*Debrief* when Mongo outperforms SQL

##### 1‑3 Mini LSM‑Tree  (R 2 · B 4 · Rƒ 0.5)

*Reading* DDIA Ch 3
*Skill Objective* explain write amplification
*Quick‑Start*

```bash
cargo new ddia/1-3/lsmtree && cd $_
# implement memtable + WAL + SSTable flush
cargo run --release --bin bench_write 1_000_000
python plot_write_amp.py
```

*Acceptance Criteria* 1 M inserts < 4 s · amp ≈ 1.2×
*Debrief* compaction trade‑off

##### 1‑4 Schema Evolution Avro  (R 1.5 · B 2 · Rƒ 0.5)

*Reading* DDIA Ch 4
*Skill Objective* forward/backward compatibility
*Quick‑Start*

```bash
docker compose -f confluent.yml up -d
curl -X POST http://localhost:8081/subjects/tweet/versions \
     -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
     -d '{"schema":"{\"type\":\"record\",\"name\":\"tweet\",\"fields\":[{\"name\":\"id\",\"type\":\"string\"},{\"name\":\"text\",\"type\":\"string\"}]}"}'
# register v2 with extra field and run producer/consumer
```

*Acceptance Criteria* consumer reads mixed versions · curl cmds saved
*Debrief* why rename is unsafe

##### 1‑5 Replication Lag Demo  (R 1.5 · B 3 · Rƒ 0.5)

*Reading* DDIA Ch 5
*Skill Objective* monitor under‑replicated partitions
*Quick‑Start*

```bash
./add_broker.sh             # adds broker‑2
./throttle.sh 200kbit       # tc qdisc limit
./lag_watch.sh              # JMX exporter → Prometheus
```

*Acceptance Criteria* lag spikes then recovers · screenshot committed
*Debrief* leader election risk

##### 1‑6 Consistent Hash Ring  (R 1.5 · B 3 · Rƒ 0.5)

*Reading* DDIA Ch 6
*Skill Objective* compute % key movement
*Quick‑Start*

```bash
cargo run -p ring_sim -- 3 4 1_000_000
```

*Acceptance Criteria* \~25 % keys move · reflection on virtual nodes
*Debrief* cache warm‑up impact

##### Module 1 Project M1 Observability Stack  (B 6 · Rƒ 1)

*Quick‑Start*

```bash
docker compose -f stacks/plumbing.yml up -d
open http://localhost:3000
```

*Acceptance Criteria* Grafana shows producer TPS, replication lag, LSM flush rate · README gif of chaos test
*Debrief* 200‑word trade‑off summary

---

### Module 2 — ML‑WORKFLOW GLUE ≈ 28 h

##### 2‑1 Dataset Versioning (DVC)  (R 1 · B 2 · Rƒ 0.5)

*Reading* ml‑eng “Data versioning”
*Skill Objective* snapshot datasets
*Quick‑Start*

```bash
pip install 'dvc[s3]'
dvc init && dvc add data/movies.csv
dvc remote add -d local /tmp/dvcstore && dvc push
truncate -s 0 data/movies.csv && dvc status && dvc checkout
```

*Acceptance Criteria* status detects change · checkout restores file
*Debrief* chosen remote backend

##### 2‑2 Experiment Tracking (W\&B)  (R 1 · B 2 · Rƒ 0.5)

*Reading* ml‑eng “Experiment tracking”
*Skill Objective* log code→model
*Quick‑Start*

```bash
pip install wandb scikit-learn
python train_logreg.py        # logs.metrics + git SHA
```

*Acceptance Criteria* run online · link stored
*Debrief* beware excessive metric spam

##### 2‑3 Distributed Training ZeRO‑2  (R 2 · B 4 · Rƒ 1)

*Reading* ml‑eng “Distributed training”
*Skill Objective* memory savings & speed
*Quick‑Start*

```bash
pip install deepspeed transformers datasets
deepspeed train.py --deepspeed ds_z2.json --model facebook/opt-1.3b
```

*Acceptance Criteria* GPU mem <10 GB · tokens/s in notes
*Debrief* fp16 overflow note

##### 2‑4 Orchestration Prefect  (R 1.5 · B 3 · Rƒ 0.5)

*Reading* ml‑eng “Orchestration”
*Skill Objective* build DAG
*Quick‑Start*

```bash
pip install prefect
prefect deployment build flows/fine_tune.py:flow -n local
prefect deployment run flow/local
```

*Acceptance Criteria* flow green · artifacts saved
*Debrief* idempotency strategy

##### 2‑5 IaC Terraform  (R 2 · B 3 · Rƒ 1)

*Reading* ml‑eng “IaC”
*Skill Objective* infra reproducibility
*Quick‑Start*

```bash
cd iac && terraform init && terraform apply
```

*Acceptance Criteria* Kafka endpoint output · cost estimate in notes
*Debrief* teardown commanded

##### 2‑6 Monitoring Stack  (R 1 · B 3 · Rƒ 0.5)

*Reading* ml‑eng “Monitoring”
*Skill Objective* system health dashboard
*Quick‑Start*

```bash
docker compose -f stacks/monitor.yml up -d
```

*Acceptance Criteria* Grafana shows GPU util & consumer lag · alert set
*Debrief* alert threshold chosen

##### Module 2 Project M2 ML Ops Dashboard  (B 4 · Rƒ 1)

*Quick‑Start*

```bash
cd frontend && npm i && npm run dev
```

*Acceptance Criteria* React page lists Prefect runs & embeds Grafana
*Debrief* screenshot + user story

---

### Module 3 — GPU‑PERFORMANCE MINDSET ≈ 32 h

##### 3‑1 Vector Add  (R 2 · B 2 · Rƒ 0.5)

*Reading* PMPP Ch 2
*Skill Objective* memory‑bound GPU gain
*Quick‑Start*

```bash
nvcc -O3 -o vec_add vec_add.cu
./vec_add 100000000
python bench_numpy.py
```

*Acceptance Criteria* GPU ≥100 GB/s · numpy slower
*Debrief* mem‑bound reasoning

##### 3‑2 Tiled Mat‑Mul  (R 2 · B 4 · Rƒ 1)

*Reading* PMPP Ch 3
*Skill Objective* shared‑mem tiling
*Quick‑Start*

```bash
nvcc -O3 -o matmul matmul.cu && ./matmul 1024
nsys profile ./matmul 1024
```

*Acceptance Criteria* ≥20× numpy · roofline compute‑bound
*Debrief* tile size choice

##### 3‑3 Occupancy Tuner  (R 1.5 · B 3 · Rƒ 0.5)

*Reading* PMPP Ch 4
*Skill Objective* block‑size tuning
*Quick‑Start*

```bash
./tune_blocks.sh > blocks.csv
python plot_blocks.py
```

*Acceptance Criteria* graph shows optimum
*Debrief* occupancy vs ILP

##### 3‑4 Warp Shuffle Reduction  (R 1.5 · B 3 · Rƒ 0.5)

*Reading* PMPP Ch 5
*Skill Objective* shuffles outperform shared mem
*Quick‑Start*

```bash
nvcc -O3 -o reduce_shfl reduce_shfl.cu
./reduce_shfl 1000000
```

*Acceptance Criteria* ≥1.8× baseline
*Debrief* why shuffles win

##### 3‑5 Prefix‑Sum Scan  (R 1.5 · B 3 · Rƒ 0.5)

*Reading* PMPP Ch 6
*Skill Objective* cooperative groups scan
*Quick‑Start*

```bash
nvcc -O3 -o scan scan.cu && ./scan 1000000
```

*Acceptance Criteria* tests pass · speed recorded
*Debrief* multi‑block limit

##### 3‑6 Ring All‑Reduce  (R 2 · B 3 · Rƒ 1)

*Reading* PMPP Ch 9
*Skill Objective* ring communication
*Quick‑Start*

```bash
git clone https://github.com/NVIDIA/nccl-tests && make MPI=0
./build/all_reduce_perf -b 8 -e 512M -f 2 -g 1
```

*Acceptance Criteria* bandwidth numbers saved
*Debrief* ring vs tree

##### Module 3 Project M3 Custom PyTorch Kernels  (B 4 · Rƒ 1)

*Quick‑Start*

```bash
python setup.py install
python benchmark.py
```

*Acceptance Criteria* custom GeLU + Attention ≥ 1.3× Triton
*Debrief* 200‑word performance post‑mortem

---

### Module 4 — CAPSTONE “Vector‑Aware Fine‑Tuner” ≈ 50 h

##### 4‑A Data Plane Ready  (R 2 · B 10 · Rƒ 1)

*Reading* skim DDIA 7–8
*Skill Objective* Kafka → ClickHouse + snapshot
*Quick‑Start*

```bash
docker compose -f stacks/dataplane.yml up -d
cargo run -p stream_to_ch
python snapshot.py
```

*Acceptance Criteria* ingest lag < 5 s @10 MB/s · parquet snapshot nightly
*Debrief* retention length

##### 4‑B Training Pipeline  (R 2 · B 14 · Rƒ 2)

*Reading* ml‑eng distributed section deep dive
*Skill Objective* Prefect flow w/ custom kernels
*Quick‑Start*

```bash
prefect deployment build flows/capstone.py:flow -n local
prefect deployment run flow/local
```

*Acceptance Criteria* W\&B loss curve · `nvprof` shows custom kernels
*Debrief* throughput vs baseline

##### 4‑C Model Serving  (R 1 · B 10 · Rƒ 1)

*Reading* vLLM or GGML docs
*Skill Objective* FastAPI REST + gRPC
*Quick‑Start*

```bash
docker build -f serve.Dockerfile -t fine-tuner-serve .
docker run -p 8080:8080 fine-tuner-serve
```

*Acceptance Criteria* /chat latency < 200 ms · grpc client ok
*Debrief* memory footprint

##### 4‑D Observability & CI  (R 1 · B 8 · Rƒ 1)

*Reading* ml‑eng monitoring + GH Actions doc
*Skill Objective* automate tests & dash
*Quick‑Start*

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

*Acceptance Criteria* CI badge green · Grafana shows FLOPS & TPS
*Debrief* alert rule

##### 4‑E Storytelling Launch  (R 0.5 · B 8 · Rƒ writing)

*Reading* none
*Skill Objective* communicate value
*Quick‑Start*

```bash
echo "Capstone deep dive" > docs/blog.md
# record 2‑min screencast
```

*Acceptance Criteria* blog published · README links video & ./dev\_up.sh
*Debrief* publish stats

##### Module 4 Project M4 Full Launch  (B 6 · Rƒ 1)

*Quick‑Start*

```bash
./dev_up.sh
```

*Acceptance Criteria* one‑click brings up pipeline, training, serving, dashboards
*Debrief* 500‑word retrospective

---

## FULL‑BOOK TRACK (optional)

### Module A DDIA 7‑12 Project “Bank‑grade Ledger” ≈ 32 h

*Quick‑Start*

```bash
docker compose -f stacks/ledger.yml up -d
cargo run -p ledger_api
python simulate_transfers.py
```

*Acceptance Criteria* funds conserved under chaos · batch vs stream diff ≤ \$0.01 · no mis‑posted cents
*Debrief* 1 500‑word architecture report linking each DDIA chapter

### Module B PMPP 1 & 7‑23 Project “GPU Workbench” ≈ 48 h

*Quick‑Start*

```bash
mkdir gpu-workbench && cd $_
./bootstrap.sh
./run_all_bench.sh > results.md
```

*Acceptance Criteria* ILP profiler, SparseSuite, TensorCore trainer all produce GFLOPS tables · README badge with benchmarks
*Debrief* blog post per tool summarizing optimizations

### Module C ml‑eng Extras Project “Prod‑Ready MLOps” ≈ 20 h

*Quick‑Start*

```bash
gh workflow enable cd.yml
./infra/deploy_blue_green.sh
feast apply
```

*Acceptance Criteria* blue‑green deploy < 3 min · ZAP scan 0 critical vulns · cost alert at \$5/day
*Debrief* 300‑word prod‑hardening lessons
