#!/usr/bin/env python3
"""
protocol_http.conf 到 nginx.conf 转换脚本 (稳定版 + 分号修复 + 注释兼容)
"""

import configparser
from pathlib import Path

def load_config(config_path):
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(config_path)
    return cfg

def clean_value(raw_val):
    return raw_val.split('#')[0].strip()

def generate_nginx_config(cfg):
    output = []

    # === global: worker_processes ===
    worker_procs = clean_value(cfg.get('performance', 'worker_processes', fallback='auto'))
    output.append(f"worker_processes {worker_procs};")
    output.append("")  # 空行

    # === events 块 ===
    output.append("events {")
    max_conn = clean_value(cfg.get('performance', 'max_connections', fallback='1024'))
    output.append(f"    worker_connections {max_conn};")
    output.append("}")
    output.append("")

    # === http 块 ===
    output.append("http {")
    output.append("    include       mime.types;")
    output.append("    default_type  application/octet-stream;")
    output.append("")

    # === 日志配置 ===
    raw_log_fmt = clean_value(cfg.get('logging', 'log_format', fallback='%t %a %m %U %s %B %D'))
    log_fmt = raw_log_fmt \
        .replace('%t', '$time_local') \
        .replace('%a', '$remote_addr') \
        .replace('%m', '$request_method') \
        .replace('%U', '$uri') \
        .replace('%s', '$status') \
        .replace('%B', '$body_bytes_sent') \
        .replace('%D', '$request_time')
    output.append(f"    log_format custom_format '{log_fmt}';")
    output.append(f"    access_log {clean_value(cfg.get('logging', 'access_log'))} custom_format;")
    output.append(f"    error_log {clean_value(cfg.get('logging', 'error_log'))};")
    output.append("")

    # === 请求体配置 ===
    max_body = clean_value(cfg.get('request', 'max_body_size', fallback='1M'))
    buf_size = clean_value(cfg.get('request', 'body_buffer_size', fallback='16K'))
    output.append(f"    client_max_body_size {max_body};")
    output.append(f"    client_body_buffer_size {buf_size};")
    output.append("")

    # === Server 块 ===
    server_ip = clean_value(cfg.get('Application', 'server_ip', fallback='0.0.0.0'))
    listen_port = clean_value(cfg.get('Application', 'listen_port', fallback='80'))

    output.append("    server {")
    output.append(f"        listen {server_ip}:{listen_port};")
    output.append("        server_name localhost;")
    output.append("")

    # === 路由配置 ===
    routes = cfg.items('routes')
    for path, rule in routes:
        path = path.strip('"')
        main_part, *params_part = rule.split(' ', 1)
        handler_type, target = main_part.split('|', 1)

        params = {}
        if params_part:
            for param in params_part[0].split():
                if '=' in param:
                    key, val = param.split('=', 1)
                    params[key.strip()] = val.strip().upper().replace(',', ' ')

        output.append(f"        # 路由: {path}")
        output.append(f"        location = {path} {{")

        if 'methods' in params:
            methods = params['methods'].split()
            output.append(f"            limit_except {' '.join(methods)} {{")
            output.append("                deny all;")
            output.append("            }")

        output.append(f"            if ($request_uri != {path}) {{")
        output.append("                return 400;")
        output.append("            }")

        require_cl_raw = cfg.get('request', 'require_content_length', fallback='false')
        require_cl = clean_value(require_cl_raw).lower() in ('true', 'on', '1', 'yes')
        if require_cl:
            output.append("            if ($http_content_length = '') {")
            output.append("                return 411;")
            output.append("            }")

        allowed_types = clean_value(cfg.get('request', 'allowed_content_types', fallback='')).replace(' ', '').split(',')
        if allowed_types and allowed_types != ['']:
            output.append(f"            if ($content_type !~* \"{'|'.join(allowed_types)}\") {{")
            output.append("                return 415;")
            output.append("            }")

        output.append("            add_header Content-Type application/json;")
        output.append("            return 200 '{\"status\": \"success\"}';")
        output.append("        }")
        output.append("")

    # === 错误页面 ===
    output.append("        error_page 400 411 415 /error;")
    output.append("        location = /error {")
    output.append("            internal;")
    output.append("            return 200 '{\"error\": \"$status\"}';")
    output.append("        }")
    output.append("    }")  # server
    output.append("}")      # http

    return '\n'.join(output)

# === 主程序入口 ===
if __name__ == '__main__':
    try:
        config = load_config('protocol_http.conf')
        nginx_conf = generate_nginx_config(config)

        output_path = Path(__file__).parent / 'nginx.conf'
        with open(output_path, 'w') as f:
            f.write(nginx_conf)

        print(f"\n 配置文件已生成: {output_path}")
        print(" 可运行以下命令测试语法:")
        print(f"   sudo nginx -t -c {output_path.resolve()}\n")

    except Exception as e:
        print(f"\n 转换失败: {str(e)}\n")
        exit(1)
