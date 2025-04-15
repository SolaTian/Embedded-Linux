#!/usr/bin/env python3
"""
protocol_http.conf 到 nginx.conf 转换脚本

功能特性：
1. 解析自定义配置格式
2. 生成符合Nginx语法的配置
3. 自动处理路径差异和参数映射
"""

import configparser
from pathlib import Path

def load_config(config_path):
    """加载自定义配置文件"""
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    return cfg

def generate_nginx_config(cfg):
    """生成Nginx配置"""
    output = []
    
    # ===== 基础配置 =====
    output.append(f"worker_processes {cfg.get('performance', 'worker_processes')};")
    output.append("events {")
    output.append(f"    worker_connections {cfg.get('performance', 'max_connections')};")
    output.append("}\n")
    
    output.append("http {")
    output.append("    include       mime.types;")
    output.append("    default_type  application/octet-stream;\n")
    
    # ===== 日志配置 =====
    log_format = cfg.get('logging', 'log_format').replace('%t', '$time_local') \
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
    output.append(f"    client_max_body_size {cfg.get('request', 'max_body_size')};")
    output.append(f"    client_body_buffer_size {cfg.get('request', 'body_buffer_size')};\n")
    
    # ===== 服务配置 =====
    output.append("    server {")
    output.append(f"        listen {cfg.get('Application', 'listen_port')};")
    output.append(f"        server_name {cfg.get('Application', 'server_ip')};\n")
    
    # ===== 路由配置 =====
    routes = cfg.items('routes')
    for path, rule in routes:
        parts = rule.split()
        handler_type, target = parts[0].split('|')
        params = dict(p.split('=') for p in parts[1:])
        
        output.append(f"\n        # 路由规则: {path}")
        output.append(f"        location ~ ^{path.replace('*', '.*')}$ {{")
        
        # 处理方法限制
        if 'methods' in params:
            methods = params['methods'].upper().split(',')
            output.append(f"            if ($request_method !~ ^({'|'.join(methods)}) {{")
            output.append("                return 405;")
            output.append("            }")
        
        # 处理静态资源
        if handler_type == 'static':
            output.append(f"            root {target};")
            if 'max_age' in params:
                output.append(f"            expires {params['max_age']}s;")
        
        # 处理动态路由
        elif handler_type == 'dynamic':
            output.append(f"            proxy_pass http://{target};")
            output.append("            proxy_set_header Host $host;")
        
        output.append("        }")
    
    # ===== HTTPS配置 =====
    if cfg.getboolean('Application', 'https_enabled'):
        output.append("\n        # HTTPS配置")
        output.append(f"        listen {cfg.get('Application', 'https_listen_port')} ssl;")
        output.append(f"        ssl_certificate {cfg.get('security', 'ssl_cert')};")
        output.append(f"        ssl_certificate_key {cfg.get('security', 'ssl_key')};")
    
    output.append("    }\n}")
    return '\n'.join(output)

if __name__ == '__main__':
    config = load_config('protocol_http.conf')
    nginx_conf = generate_nginx_config(config)
    
    output_path = Path(__file__).parent / 'nginx.conf'
    with open(output_path, 'w') as f:
        f.write(nginx_conf)
    
    print(f"配置文件已生成: {output_path}")