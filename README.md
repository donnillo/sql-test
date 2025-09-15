### Usage

#### Run sql test for task #1

```bash
uv run sql.py --task 1
```

#### Example output for task #1

```bash
────────────────── employee_presence ───────────────────
╭───────────────┬────────────┬───────────┬─────────────╮
│   employee_id │ day        │ arrival   │ departure   │
├───────────────┼────────────┼───────────┼─────────────┤
│             1 │ 2025-09-11 │ 05:45:43  │ 20:07:44    │
│             2 │ 2025-09-11 │ 08:50:12  │ 17:07:03    │
│             3 │ 2025-09-11 │ 07:33:07  │ 18:32:35    │
│             4 │ 2025-09-11 │ 09:35:04  │ 21:49:16    │
│             5 │ 2025-09-11 │ 09:05:04  │ 19:52:04    │
│             6 │ 2025-09-11 │ 08:24:20  │ 18:22:07    │
│             7 │ 2025-09-11 │ 09:14:15  │ 19:18:02    │
│             8 │ 2025-09-11 │ 11:14:45  │ 17:53:59    │
│             9 │ 2025-09-11 │ 07:34:24  │ 21:39:11    │
│            10 │ 2025-09-11 │ 12:04:33  │ 22:58:46    │
│            11 │ 2025-09-11 │ 10:41:57  │ 20:31:10    │
│            12 │ 2025-09-11 │ 12:49:52  │ 19:26:11    │
╰───────────────┴────────────┴───────────┴─────────────╯
```

```sql
select distinct on (hours.hour) hours.hour,
                   coalesce(sum(case
                                    when (arrival.arrival is not null) then 1
                                    else 0
                                end + case
                                          when (departure.departure is not null) then -1
                                          else 0
                                      end) over (
                                                 order by hours.hour, arrival.arrival, departure.departure rows between unbounded preceding and 1 preceding), 0) as num_persons
from
  (select hours.hour as hour
   from generate_series(0, 23) as hours(hour)) as hours
left outer join employee_presence as arrival on hours.hour = extract(hour
                                                                     from arrival.arrival)
left outer join employee_presence as departure on hours.hour = extract(hour
                                                                       from departure.departure)
order by hours.hour asc
```

```bash
────── query_result ──────
╭────────┬───────────────╮
│   hour │   num_persons │
├────────┼───────────────┤
│      0 │             0 │
│      1 │             0 │
│      2 │             0 │
│      3 │             0 │
│      4 │             0 │
│      5 │             0 │
│      6 │             1 │
│      7 │             1 │
│      8 │             3 │
│      9 │             5 │
│     10 │             8 │
│     11 │             9 │
│     12 │            10 │
│     13 │            12 │
│     14 │            12 │
│     15 │            12 │
│     16 │            12 │
│     17 │            12 │
│     18 │            10 │
│     19 │             8 │
│     20 │             5 │
│     21 │             3 │
│     22 │             1 │
│     23 │             0 │
╰────────┴───────────────╯
```


#### Run sql test for task #2

```bash
uv run sql.py --task 2
```

#### Example output for task #2

```bash
──────────── client_balance ─────────────
╭─────────────┬────────────┬────────────╮
│   client_id │ day        │    balance │
├─────────────┼────────────┼────────────┤
│           1 │ 2025-08-11 │ 186,000.00 │
│           1 │ 2025-08-12 │  29,000.00 │
│           1 │ 2025-08-13 │ 100,000.00 │
│           1 │ 2025-08-14 │       0.00 │
│           1 │ 2025-08-15 │  21,666.50 │
│           1 │ 2025-08-16 │ 121,000.00 │
│           1 │ 2025-08-17 │  98,200.00 │
│           1 │ 2025-08-18 │ 178,900.00 │
│           1 │ 2025-08-19 │ 588,576.38 │
│           1 │ 2025-08-20 │ 296,358.25 │
│           1 │ 2025-08-21 │  62,950.00 │
│           1 │ 2025-08-22 │  84,700.00 │
│           1 │ 2025-08-23 │ 592,678.00 │
│           1 │ 2025-08-24 │ 173,000.00 │
│           1 │ 2025-08-25 │ 200,000.00 │
│           1 │ 2025-08-26 │ 173,600.00 │
│           1 │ 2025-08-27 │ 163,000.00 │
│           1 │ 2025-08-28 │  68,000.00 │
│           1 │ 2025-08-29 │       0.00 │
│           1 │ 2025-08-30 │ 107,420.00 │
│           1 │ 2025-08-31 │  53,225.27 │
│           1 │ 2025-09-01 │ 130,546.00 │
│           1 │ 2025-09-02 │ 208,700.00 │
│           1 │ 2025-09-03 │ 406,980.00 │
│           1 │ 2025-09-04 │ 186,161.91 │
│           1 │ 2025-09-05 │       0.00 │
│           1 │ 2025-09-06 │ 199,000.00 │
│           1 │ 2025-09-07 │ 221,166.00 │
│           1 │ 2025-09-08 │       0.00 │
│           1 │ 2025-09-09 │ 245,176.00 │
│           1 │ 2025-09-10 │ 218,880.00 │
│           1 │ 2025-09-11 │  92,555.00 │
╰─────────────┴────────────┴────────────╯
```

```sql
select distinct on (periodized.client_id,
                    periodized.period) periodized.client_id,
                   first_value(periodized.day) over (partition by periodized.period) as period_start,
                   last_value(periodized.day) over (partition by periodized.period) as period_end,
                   avg(periodized.balance) over (partition by periodized.period) as avg_balance_within_period
from
  (select client_balance.client_id as client_id,
          client_balance.day as day,
          client_balance.balance as balance,
          sum(case
                  when (client_balance.balance = 0) then 1
                  else 0
              end) over (
                         order by client_balance.client_id, client_balance.day) as period
   from client_balance
   order by client_balance.client_id,
            client_balance.day) as periodized
where periodized.balance > 0
order by periodized.client_id,
         periodized.period,
         periodized.day
```

```bash
─────────────────────────────── query_result ────────────────────────────────
╭─────────────┬────────────────┬──────────────┬─────────────────────────────╮
│   client_id │ period_start   │ period_end   │   avg_balance_within_period │
├─────────────┼────────────────┼──────────────┼─────────────────────────────┤
│           1 │ 2025-08-11     │ 2025-08-13   │                  105,000.00 │
│           1 │ 2025-08-15     │ 2025-08-28   │                  201,616.37 │
│           1 │ 2025-08-30     │ 2025-09-04   │                  182,172.20 │
│           1 │ 2025-09-06     │ 2025-09-07   │                  210,083.00 │
│           1 │ 2025-09-09     │ 2025-09-11   │                  185,537.00 │
╰─────────────┴────────────────┴──────────────┴─────────────────────────────╯
```
