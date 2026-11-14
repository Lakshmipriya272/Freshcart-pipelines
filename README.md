# freshcart-pipelines

Data Engineering (CS-8037) assignment — "From Git to Gold".

Four pieces of a modern data platform, end to end:

| Folder | Part | What it is |
|--------|------|------------|
| `elt/` | B | FreshCart ELT notebook: sample API data → Snowflake bronze → silver → quarantine → gold. |
| `iris_project/` | C | Mage ML pipeline: load Iris → validate → prepare → train → save/evaluate, with `@test` gates. |
| `stream/` | D | RabbitMQ food-order stream: topic-exchange dispatcher + drivers with ACK/NACK. |
| `tests/` | A | pytest test for the `prepare_data` block, run by CI. |
| `.github/workflows/ci.yml` | A | GitHub Actions: checkout → Python 3.12 → install → pytest on every push. |

## Part B — ELT

Open `elt/freshcart_elt.ipynb` (Google Colab or Jupyter), add your Snowflake
credentials, and run top to bottom. Final line should read:
`GOLD: 4 orders, revenue ₹7785.00, 126 loyalty points`.

## Part C — Mage

`mage run iris_project iris_classifier --test` runs the pipeline. Use
`--runtime-vars '{"max_depth": 1..5}'` to sweep the tree depth; depth 1 fails the
accuracy gate and `save_results` never runs.

## Part D — RabbitMQ stream

```bash
python stream/dispatcher.py
python stream/driver.py Ravi 'bangalore.koramangala.*'
python stream/driver.py Meena 'bangalore.*.food'
# ... more drivers with their own binding patterns
```

Set `RABBITMQ_URL` in a local `.env` (git-ignored) if not using localhost.
