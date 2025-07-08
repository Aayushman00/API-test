import argparse
import requests
import json
import time
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich import box

HISTORY_FILE = os.path.expanduser("~/.apitest_history.json")
MAX_HISTORY = 5
console = Console()

def save_to_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    history.insert(0, entry)
    history = history[:MAX_HISTORY]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_curl(method, url, headers=None, data=None):
    cmd = f"curl -X {method} \"{url}\""
    if headers:
        for k, v in headers.items():
            cmd += f" -H \"{k}: {v}\""
    if data:
        cmd += f" -d '{json.dumps(data)}'"
    return cmd

def pretty_print_response(response):
    table = Table(title="API Response", box=box.SIMPLE, show_lines=True)
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Status Code", str(response.status_code))
    table.add_row("Time Taken", f"{response.elapsed.total_seconds() * 1000:.2f} ms")
    table.add_row("Content Length", f"{len(response.content)} bytes")
    table.add_row("Content Type", response.headers.get('Content-Type', 'Unknown'))
    console.print(table)

    console.print("\n[bold]Response Body:[/bold]")
    try:
        parsed = json.loads(response.text)
        pretty_json = json.dumps(parsed, indent=4)
        syntax = Syntax(pretty_json, "json", theme="monokai", line_numbers=True)
        console.print(syntax)
    except:
        console.print(response.text)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def main():
    parser = argparse.ArgumentParser(description='🧪 API Tester CLI Tool')
    parser.add_argument('--method', type=str, help='HTTP method: GET, POST, PUT, DELETE')
    parser.add_argument('--url', type=str, help='API endpoint URL')
    parser.add_argument('--headers', type=str, help='Optional JSON headers')
    parser.add_argument('--data', type=str, help='Optional JSON body data')
    parser.add_argument('--auth', type=str, help='Basic auth in user:pass format')
    parser.add_argument('--bearer', type=str, help='Bearer token auth')
    parser.add_argument('--history', action='store_true', help='Show last 5 requests')
    args = parser.parse_args()

    if args.history:
        history = load_history()
        if not history:
            console.print("[yellow]No history found.[/yellow]")
            return
        console.print("[bold]Request History:[/bold]")
        for i, h in enumerate(history):
            console.print(f"[{i+1}] {h['method']} {h['url']} ({h['status_code']}) at {h['timestamp']}")
        return

    if not (args.method and args.url):
        console.print("[red]❌ --method and --url are required unless using --history[/red]")
        return

    method = args.method.upper()
    url = args.url

    try:
        headers = json.loads(args.headers) if args.headers else {}
        data = json.loads(args.data) if args.data else None
    except json.JSONDecodeError:
        console.print("[red]❌ Invalid JSON format in headers or data[/red]")
        return

    if args.auth:
        user, pw = args.auth.split(":")
        response = requests.request(method, url, headers=headers, json=data, auth=(user, pw))
    else:
        if args.bearer:
            headers['Authorization'] = f"Bearer {args.bearer}"
        try:
            start = time.time()
            response = requests.request(method, url, headers=headers, json=data)
            end = time.time()

            pretty_print_response(response)

            curl_cmd = generate_curl(method, url, headers, data)
            console.print("\n[bold green]Curl Command:[/bold green]", curl_cmd)

            entry = {
                "timestamp": datetime.now().isoformat(),
                "method": method,
                "url": url,
                "headers": headers,
                "data": data,
                "status_code": response.status_code
            }
            save_to_history(entry)

        except requests.exceptions.RequestException as e:
            console.print(f"[red]❌ Request failed: {e}[/red]")

if __name__ == '__main__':
    main()
