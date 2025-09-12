#### Usage

```bash
kiselevda@DONNILL0:~/workspace/hh.ru/sql_test$ uv run sql.py 1
```

#### Example output for task #1

```bash
────────────────── employee_presence ───────────────────
╭───────────────┬────────────┬───────────┬─────────────╮
│   employee_id │ day        │ arrival   │ departure   │
├───────────────┼────────────┼───────────┼─────────────┤
│             1 │ 2025-09-11 │ 08:27:58  │ 19:07:30    │
│             2 │ 2025-09-11 │ 08:45:32  │ 22:46:40    │
│             3 │ 2025-09-11 │ 10:19:33  │ 17:50:08    │
│             4 │ 2025-09-11 │ 11:09:53  │ 19:07:33    │
│             5 │ 2025-09-11 │ 05:00:18  │ 19:49:59    │
│             6 │ 2025-09-11 │ 09:22:06  │ 19:15:06    │
│             7 │ 2025-09-11 │ 08:07:58  │ 18:30:13    │
│             8 │ 2025-09-11 │ 09:50:55  │ 17:43:43    │
│             9 │ 2025-09-11 │ 16:59:13  │ 19:51:54    │
╰───────────────┴────────────┴───────────┴─────────────╯
```

```sql
select hourly.hour,
        sum(hourly.count) over (
                                order by hourly.hour) as num_persons
from
  (select hours.hour as hour,
          sum(coalesce(arrival.count_in, 0) + coalesce(departure.count_out, 0)) as count
    from
      (select hours.hour as hour
      from generate_series(1, 23) as hours(hour)) as hours
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
│      5 │             1 │
│      6 │             1 │
│      7 │             1 │
│      8 │             4 │
│      9 │             6 │
│     10 │             7 │
│     11 │             8 │
│     12 │             8 │
│     13 │             8 │
│     14 │             8 │
│     15 │             8 │
│     16 │             9 │
│     17 │             7 │
│     18 │             6 │
│     19 │             1 │
│     20 │             1 │
│     21 │             1 │
│     22 │             0 │
│     23 │             0 │
╰────────┴───────────────╯
```
