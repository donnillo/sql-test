### Usage

#### Run sql test for task #1

```bash
uv run sql.py 1
```

#### Example output for task #1

```bash
────────────────── employee_presence ───────────────────
╭───────────────┬────────────┬───────────┬─────────────╮
│   employee_id │ day        │ arrival   │ departure   │
├───────────────┼────────────┼───────────┼─────────────┤
│             1 │ 2025-09-11 │ 08:09:57  │ 18:21:03    │
│             2 │ 2025-09-11 │ 12:07:00  │ 14:56:57    │
│             3 │ 2025-09-11 │ 11:19:24  │ 17:11:45    │
│             4 │ 2025-09-11 │ 09:58:14  │ 20:30:59    │
│             5 │ 2025-09-11 │ 08:56:52  │ 18:04:22    │
│             6 │ 2025-09-11 │ 07:10:01  │ 17:21:20    │
│             7 │ 2025-09-11 │ 08:26:06  │ 16:56:44    │
│             8 │ 2025-09-11 │ 10:01:15  │ 16:46:28    │
│             9 │ 2025-09-11 │ 15:58:39  │ 16:30:48    │
╰───────────────┴────────────┴───────────┴─────────────╯
```

```sql
select hourly.hour,
       coalesce(sum(hourly.count) over (
                                        order by hourly.hour rows between unbounded preceding and 1 preceding), 0) as num_persons
from
  (select hours.hour as hour,
          sum(coalesce(arrival.count_in, 0) + coalesce(departure.count_out, 0)) as count
   from
     (select hours.hour as hour
      from generate_series(0, 23) as hours(hour)) as hours
   left outer join
     (select extract(hour
                     from employee_presence.arrival) as hour,
             1 as count_in
      from employee_presence) as arrival on hours.hour = arrival.hour
   left outer join
     (select extract(hour
                     from employee_presence.departure) as hour,
             -1 as count_out
      from employee_presence) as departure on hours.hour = departure.hour
   group by hours.hour
   order by hours.hour asc) as hourly
where hourly.hour > 0
```

```bash
────── query_result ──────
╭────────┬───────────────╮
│   hour │   num_persons │
├────────┼───────────────┤
│      1 │             0 │
│      2 │             0 │
│      3 │             0 │
│      4 │             0 │
│      5 │             0 │
│      6 │             0 │
│      7 │             0 │
│      8 │             1 │
│      9 │             4 │
│     10 │             5 │
│     11 │             6 │
│     12 │             7 │
│     13 │             8 │
│     14 │             8 │
│     15 │             7 │
│     16 │             8 │
│     17 │             5 │
│     18 │             3 │
│     19 │             1 │
│     20 │             1 │
│     21 │             0 │
│     22 │             0 │
│     23 │             0 │
╰────────┴───────────────╯
```


#### Run sql test for task #2

```bash
uv run sql.py 2
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
select distinct on (pre_periodized.client_id,
                    pre_periodized.period) pre_periodized.client_id,
                   first_value(pre_periodized.day) over (partition by pre_periodized.period) as period_start,
                   last_value(pre_periodized.day) over (partition by pre_periodized.period) as period_end,
                   avg(pre_periodized.balance) over (partition by pre_periodized.period) as avg_balance_within_period
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
            client_balance.day) as pre_periodized
where pre_periodized.balance > 0
order by pre_periodized.client_id,
         pre_periodized.period,
         pre_periodized.day
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
