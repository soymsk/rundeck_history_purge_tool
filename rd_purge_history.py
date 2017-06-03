#! /usr/bin/env python
import argparse
import requests
import sys
import time
import xml.etree.ElementTree as etree

RUNDECK_HOST = 'http://localhost:4440/api'
API_VERSION = 18
ACCESS_TOKEN = 'OCTQsSsvVFDeH64sFCuNf4XRo0W9OHap'

root = '{host}/{version}'.format(host=RUNDECK_HOST, version=API_VERSION)

def search_history(client, project, job_filter=None, offset=0, hmax=0):
    request = 'history?project={p}&offset={o}&max={m}'.format(
        p=project,
        o=offset,
        m=hmax,
    )

    if job_filter:
        request += '&jobFilter=' + job_filter

    res = client.get(request)
    return etree.fromstring(res.text)


def get_execution_ids(client, project, job_filter, offset, hmax):
    root = search_history(client, project, job_filter, offset, hmax)
    return [event.find('./execution').get('id')  for event in root]


def delete_executions(client, ids):
    res = client.post('executions/delete', data={"ids": ids})


def get_history_total(client, project, job_filter):
    history = search_history(client, project, job_filter)
    return int(history.get('total'))


def purge_history(
        client,
        project,
        job_filter,
        preserve_history_size,
        chunk_size,
        max_delete_size,
        dry_run
):
    total = get_history_total(client, project, job_filter)
    print("Total: ", total)
    max_delete_size = min(max_delete_size, total)
    deleted = 0
    remains = total - deleted - preserve_history_size

    while remains > 0:
        offset = total - remains

        ids = get_execution_ids(client, project, job_filter, offset, chunk_size)
        delete_size = min(len(ids), max_delete_size - deleted)
        if delete_size == 0:
            break

        ids = ids[-delete_size:]
        print("Purge {} entries: {}".format(delete_size, ids))

        if not dry_run:
            delete_executions(client, ids)
        deleted += len(ids)
        time.sleep(0.1)

        remains = total - deleted - preserve_history_size

    return deleted


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--job_filter', type=str, default=None)
    parser.add_argument('-t', '--access_token', type=str, default=None, required=True)
    parser.add_argument('-H', '--host', type=str, default='localhost')
    parser.add_argument('-P', '--port', type=int, default=4440)
    parser.add_argument('-p', '--preserve_history_size', type=int, default=20)
    parser.add_argument('-m', '--max_delete_size', type=int, default=sys.maxsize)
    parser.add_argument('-c', '--chunk_size', type=int, default=20)
    parser.add_argument('-n', '--dry_run', action='store_true', default=False)
    parser.add_argument('project', type=str)

    return parser.parse_args()


class Client():
    def __init__(self, host, port, access_token):
        self.host = host
        self.port = port
        self.access_token = access_token

    def get(self, path):
        headers = {'X-Rundeck-Auth-Token': self.access_token}
        res = requests.get('{}/{}'.format(root, path), headers=headers)
        res.raise_for_status()
        return res

    def post(self, path, **kwargs):
        headers = {'X-Rundeck-Auth-Token': self.access_token}
        res = requests.post('{}/{}'.format(root, path), headers=headers, **kwargs)
        res.raise_for_status()
        return res


if __name__ == '__main__':
    args = parse_args()

    print("Args:")
    print("\n".join([
        "\t{}: {}".format(name, getattr(args, name)) for name in vars(args) if name != 'access_token'
    ]))

    deleted = purge_history(
        Client(args.host, args.port, args.access_token),
        args.project,
        args.job_filter,
        args.preserve_history_size,
        args.chunk_size,
        args.max_delete_size,
        args.dry_run
    )
    print("Total deleted: ", deleted)

