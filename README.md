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
