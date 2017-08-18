# rundeck_history_purge_tool
Rundeck history purge tool with conditions

# Usage
```
usage: rd_purge_history.py [-h] [-j JOB_FILTER] -t ACCESS_TOKEN [-H HOST]
                           [-P PORT] [-k KEEP_HISTORY_SIZE]
                           [-m MAX_DELETE_SIZE] [-c CHUNK_SIZE] [-n]
                           [-p, PROJECT]
positional arguments:
  project

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
  -j JOB_FILTER, --job_filter JOB_FILTER
  -t ACCESS_TOKEN, --access_token ACCESS_TOKEN
  -H HOST, --host HOST
  -P PORT, --port PORT
  -k KEEP_HISTORY_SIZE, --keep_history_size KEEP_HISTORY_SIZE
  -m MAX_DELETE_SIZE, --max_delete_size MAX_DELETE_SIZE
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
  -n, --dry_run
```

## Example usage with cron for a project named 'main'
```
# The oldest 10 histories of 'job1' in 'main' project are purged everyday, but keep latest 20 histories
5 0 * * * python $PATH_TO_THIS_DIR/rundeck_history_purge_tool/rd_purge_history.py -p main -c 10 -k 20 -j job1 >> ~/cron.log
```

## Example usage with cron for ALL projects, ALL jobs
```
# The oldest 10 histories of all in each project are purged everyday, but keep latest 20 histories
5 0 * * * python $PATH_TO_THIS_DIR/rundeck_history_purge_tool/rd_purge_history.py -c 10 -k 20 >> ~/cron.log
```
