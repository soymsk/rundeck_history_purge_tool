# rundeck_history_purge_tool
Rundeck history purge tool with conditions

# Usage
```
usage: rd_purge_history.py [-h] [-j JOB_FILTER] -t ACCESS_TOKEN [-H HOST]
                           [-P PORT] [-p PRESERVE_HISTORY_SIZE]
                           [-m MAX_DELETE_SIZE] [-c CHUNK_SIZE] [-n]
                           project

positional arguments:
  project

optional arguments:
  -h, --help            show this help message and exit
  -j JOB_FILTER, --job_filter JOB_FILTER
  -t ACCESS_TOKEN, --access_token ACCESS_TOKEN
  -H HOST, --host HOST
  -P PORT, --port PORT
  -p PRESERVE_HISTORY_SIZE, --preserve_history_size PRESERVE_HISTORY_SIZE
  -m MAX_DELETE_SIZE, --max_delete_size MAX_DELETE_SIZE
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
  -n, --dry_run
```

## Example usage with cron
```
# The oldest 10 histories of 'job1' in 'main' project are purged everyday.
5 0 * * * python  /home/ryosuke/workspace/rundeck_history_purge_tool/rd_purge_history.py main -s 10 -j job1 >> ~/cron.log
```
