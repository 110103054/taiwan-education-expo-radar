#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import urllib.parse
from datetime import date, datetime
from pathlib import Path


API_BASE = "https://open.feishu.cn/open-apis"


def request_json(method, url, payload=None, token=None):
    command = ["curl", "--silent", "--show-error", "--fail-with-body", "--request", method]
    command += ["--header", "Content-Type: application/json; charset=utf-8"]
    if token:
        command += ["--header", f"Authorization: Bearer {token}"]
    input_data = None
    if payload is not None:
        command += ["--data-binary", "@-"]
        input_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    command.append(url)
    try:
        completed = subprocess.run(command, input=input_data, capture_output=True, check=True, timeout=30)
        result = json.loads(completed.stdout.decode("utf-8"))
    except subprocess.CalledProcessError as error:
        body = error.stdout.decode("utf-8", errors="replace") or error.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"飛書 API 連線錯誤: {body}") from error
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("飛書 API 連線逾時") from error
    if result.get("code", 0) != 0:
        raise RuntimeError(f"飛書 API 錯誤: {result}")
    return result


def tenant_token(app_id, app_secret):
    result = request_json(
        "POST",
        f"{API_BASE}/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    return result["tenant_access_token"]


def resolve_wiki_node(token, wiki_token):
    result = request_json(
        "GET",
        f"{API_BASE}/wiki/v2/spaces/get_node?token={urllib.parse.quote(wiki_token)}",
        token=token,
    )
    node = result.get("data", {}).get("node", {})
    if node.get("obj_type") != "sheet":
        raise RuntimeError(f"Wiki 節點不是試算表，類型為：{node.get('obj_type', '未知')}")
    return node.get("obj_token", "")


def find_sheet_id(token, spreadsheet_token, sheet_name):
    result = request_json(
        "GET",
        f"{API_BASE}/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query",
        token=token,
    )
    sheets = result.get("data", {}).get("sheets", [])
    for sheet in sheets:
        if sheet.get("title") == sheet_name:
            return sheet.get("sheet_id", "")
    if len(sheets) == 1:
        return sheets[0].get("sheet_id", "")
    names = ", ".join(sheet.get("title", "") for sheet in sheets)
    raise RuntimeError(f"找不到工作表「{sheet_name}」。目前分頁：{names or '無'}")


def read_values(token, spreadsheet_token, sheet_id, cell_range):
    encoded_range = urllib.parse.quote(f"{sheet_id}!{cell_range}", safe="!")
    result = request_json(
        "GET",
        f"{API_BASE}/sheets/v2/spreadsheets/{spreadsheet_token}/values/{encoded_range}",
        token=token,
    )
    return result.get("data", {}).get("valueRange", {}).get("values", [])


def write_values(token, spreadsheet_token, sheet_id, start_cell, values):
    range_end = excel_column(len(values[0])) + str(len(values))
    result = request_json(
        "PUT",
        f"{API_BASE}/sheets/v2/spreadsheets/{spreadsheet_token}/values",
        {
            "valueRange": {
                "range": f"{sheet_id}!{start_cell}:{range_end}",
                "values": values,
            }
        },
        token=token,
    )
    return result


def excel_column(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def normalize_cell(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%Y-%m-%d")
    if value is None:
        return ""
    return value


def merge_rows(headers, incoming_rows, existing_values, preserved_columns):
    existing_headers = existing_values[0] if existing_values else []
    existing_rows = existing_values[1:] if len(existing_values) > 1 else []
    existing_map = {}
    if existing_headers and "活動名稱" in existing_headers:
        name_index = existing_headers.index("活動名稱")
        for row in existing_rows:
            if len(row) > name_index and row[name_index]:
                existing_map[str(row[name_index]).strip()] = row

    incoming_header_index = {header: index for index, header in enumerate(headers)}
    existing_header_index = {header: index for index, header in enumerate(existing_headers)}
    output = [headers]
    for incoming in incoming_rows:
        normalized = [normalize_cell(value) for value in incoming]
        name = str(normalized[incoming_header_index["活動名稱"]]).strip()
        existing = existing_map.get(name)
        if existing:
            for column in preserved_columns:
                incoming_index = incoming_header_index.get(column)
                existing_index = existing_header_index.get(column)
                if incoming_index is not None and existing_index is not None and len(existing) > existing_index:
                    normalized[incoming_index] = existing[existing_index]
        output.append(normalized)
    return output


def send_webhook(webhook_url, title, lines):
    if not webhook_url:
        return
    request_json(
        "POST",
        webhook_url,
        {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": title}},
                "elements": [
                    {"tag": "markdown", "content": "\n".join(f"- {line}" for line in lines)}
                ],
            },
        },
    )


def load_config(path, require_credentials=True):
    with open(path, "r", encoding="utf-8") as file:
        config = json.load(file)
    config["app_id"] = os.getenv("FEISHU_APP_ID", config.get("app_id", ""))
    config["app_secret"] = os.getenv("FEISHU_APP_SECRET", config.get("app_secret", ""))
    config["webhook_url"] = os.getenv("FEISHU_WEBHOOK_URL", config.get("webhook_url", ""))
    if config.get("spreadsheet_url"):
        parsed = urllib.parse.urlparse(config["spreadsheet_url"])
        parts = [part for part in parsed.path.split("/") if part]
        if "sheets" in parts and parts.index("sheets") + 1 < len(parts):
            config["spreadsheet_token"] = config.get("spreadsheet_token") or parts[parts.index("sheets") + 1]
        if "wiki" in parts and parts.index("wiki") + 1 < len(parts):
            config["wiki_token"] = config.get("wiki_token") or parts[parts.index("wiki") + 1]
        query = urllib.parse.parse_qs(parsed.query)
        config["sheet_id"] = config.get("sheet_id") or (query.get("sheet", [""])[0])
    if require_credentials:
        required = ["app_id", "app_secret"]
        missing = [key for key in required if not config.get(key)]
        if missing:
            raise RuntimeError(f"缺少設定：{', '.join(missing)}")
        if not config.get("spreadsheet_token") and not config.get("wiki_token"):
            raise RuntimeError("無法從網址辨識 spreadsheet_token 或 wiki_token")
    return config


def main():
    parser = argparse.ArgumentParser(description="同步兒童教育展會資料到飛書試算表")
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config, require_credentials=not args.dry_run)
    with open(args.data, "r", encoding="utf-8") as file:
        data = json.load(file)

    headers = data["headers"]
    rows = data["rows"]
    preserved = config.get("preserved_columns", [])
    if args.dry_run:
        print(json.dumps({"headers": headers, "row_count": len(rows), "preserved_columns": preserved}, ensure_ascii=False, indent=2))
        return

    token = tenant_token(config["app_id"], config["app_secret"])
    if not config.get("spreadsheet_token") and config.get("wiki_token"):
        config["spreadsheet_token"] = resolve_wiki_node(token, config["wiki_token"])
    if not config.get("sheet_id"):
        config["sheet_id"] = find_sheet_id(token, config["spreadsheet_token"], config.get("sheet_name", "展會追蹤"))
    existing = read_values(token, config["spreadsheet_token"], config["sheet_id"], config.get("read_range", "A1:AZ500"))
    merged = merge_rows(headers, rows, existing, preserved)
    clear_row_count = max(len(existing), len(merged))
    clear_col_count = max(len(headers), max((len(row) for row in existing), default=0))
    if clear_row_count and clear_col_count:
        write_values(
            token,
            config["spreadsheet_token"],
            config["sheet_id"],
            "A1",
            [[""] * clear_col_count for _ in range(clear_row_count)],
        )
    write_values(token, config["spreadsheet_token"], config["sheet_id"], "A1", merged)
    send_webhook(
        config.get("webhook_url"),
        "台灣兒童教育展會雷達已更新",
        [f"同步展會：{len(rows)} 筆", f"更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}"],
    )
    print(f"已同步 {len(rows)} 筆展會資料到飛書。")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
