#!/usr/bin/env python3
"""
protocol_http.conf 到 nginx.conf 转换脚本 (改进版)
"""

import configparser
from pathlib import Path

def load_config(config_path):
    """加载自定义配置文件"""
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(config_path)
    return cfg

def generate_nginx_config(cfg):
    """生成Nginx配置"""
    output = []
    
    # ===== 基础配置 =====
    output.append(f"worker_processes {cfg.get('performance', 'worker_processes', fallback='auto')};")
    output.append("events {")
    output.append(f"    worker_connections {cfg.get('performance', 'max_connections', fallback='1024')};")
    output.append("}\n")
    
    output.append("http {")
    output.append("    include       mime.types;")
    output.append("    default_type  application/octet-stream;\n")
    
    # ===== 日志配置 =====
    log_format = cfg.get('logging', 'log_format', fallback='%t %a %m %U %s %B %D') \
        .replace('%t', '$time_local') \
        .replace('%a', '$remote_addr') \
        .replace('%m', '$request_method') \
        .replace('%U', '$uri') \
        .replace('%s', '$status') \
        .replace('%B', '$body_bytes_sent') \
        .replace('%D', '$request_time')
    output.append(f'    log_format custom_format "{log_format}";')
    output.append(f'    access_log {cfg.get("logging", "access_log")} custom_format;')
    output.append(f'    error_log {cfg.get("logging", "error_log")};\n')
    
    # ===== 请求处理配置 =====
    output.append(f"    client_max_body_size {cfg.get('request', 'max_body_size', fallback='1M')};")
    output.append(f"    client_body_buffer_size {cfg.get('request', 'body_buffer_size', fallback='16K')};\n")
    
    # ===== 主服务配置 =====
    output.append("    server {")
    output.append(f"        listen {cfg.get('Application', 'server_ip')}:{cfg.get('Application', 'listen_port')};")
    output.append("        server_name localhost;\n")
    
    # ===== 核心路由处理 =====
    routes = cfg.items('routes')
    for path, rule in routes:
        path = path.strip('"')  # 去除引号
        parts = [p.strip() for p in rule.split('|')]
        handler_type, target = parts[0].split('|')
        params = {}
        
        # 解析参数 (如 methods=GET,POST,PUT)
        for param in parts[1:]:
            if '=' in param:
                key, value = param.split('=', 1)
                params[key.strip()] = value.strip().upper().replace(',', ' ')
        
        output.append(f"\n        # 路由: {path}")
        output.append(f"        location = {path} {{")
        
        # 方法限制
        if 'methods' in params:
            methods = params['methods'].split()
            output.append(f"            limit_except {' '.join(methods)} {{")
            output.append("                deny all;")
            output.append("            }")
        
        # 必要校验规则
        output.append("\n            # === 请求头校验 ===")
        
        # URI 校验
        output.append(f"            if ($request_uri != {path}) {{")
        output.append("                return 400;")
        output.append("            }")
        
        # Content-Length 校验
        if cfg.getboolean('request', 'require_content_length', fallback=False):
            output.append("            if ($http_content_length = '') {")
            output.append("                return 411;")
            output.append("            }")
        
        # Content-Type 校验
        allowed_types = cfg.get('request', 'allowed_content_types', fallback='').replace(' ', '').split(',')
        if allowed_types and allowed_types != ['']:
            output.append(f"            if ($content_type !~* \"{'|'.join(allowed_types)}\") {{")
            output.append("                return 415;")
            output.append("            }")
        
        # 动态处理器响应
        output.append("\n            # === 响应处理 ===")
        output.append("            add_header Content-Type application/json;")
        output.append("            return 200 '{\"status\": \"success\"}';")
        
        output.append("        }")
    
    # ===== 错误页面配置 =====
    output.append("\n        # 错误处理")
    output.append("        error_page 400 411 415 /error;")
    output.append("        location = /error {")
    output.append("            internal;")
    output.append("            return 200 '{\"error\": \"$status\"}';")
    output.append("        }")
    
    output.append("    }\n}")
    return '\n'.join(output)

if __name__ == '__main__':
    try:
        config = load_config('protocol_http.conf')
        
        # 必要配置项验证
        if not config.has_section('Application'):
            raise ValueError("缺少 [Application] 配置段")
        
        nginx_conf = generate_nginx_config(config)
        
        output_path = Path(__file__).parent / 'nginx.conf'
        with open(output_path, 'w') as f:
            f.write(nginx_conf)
        
        print(f"配置文件已生成: {output_path}")
        print("请执行以下命令验证配置:")
        print("sudo nginx -t -c", output_path.resolve())
        
    except Exception as e:
        print(f"配置转换失败: {str(e)}")
        exit(1)