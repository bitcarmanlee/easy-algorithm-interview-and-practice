登录到Redis服务器上以后，输入info命令，在Stats部分会看到如下数据  

```
# Stats
total_connections_received:7429663
total_commands_processed:5927397034
instantaneous_ops_per_sec:1
total_net_input_bytes:1206431541918
total_net_output_bytes:1398071851083
instantaneous_input_kbps:0.12
instantaneous_output_kbps:25.19
rejected_connections:0
sync_full:1
sync_partial_ok:0
sync_partial_err:1
expired_keys:25055057
expired_stale_perc:0.00
expired_time_cap_reached_count:162215
evicted_keys:0
keyspace_hits:73592202
keyspace_misses:103528090
...
```  

其中  

```
keyspace_hits：命中的次数
keyspace_misses：没有命中的次数
```  

所以缓存命中率的计算方法  

```
keyspace_hits / (keyspace_hits + keyspace_misses)
```  

本例中，缓存命中率为  

```
73592202 / (73592202 + 103528090) = 0.41549277707830334
```
