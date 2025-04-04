# Nginx 

## 1、Nginx 基本概念

> Nginx 是一个高性能的 HTTP 和反向代理的 Web 服务器。特点是占有内存小，并发能力强。


### 1.1、正向代理与反向代理

> 代理服务器：介于客户端和服务器之间的中间服务器，用来转发请求。


|代理分类|概念|特点|应用场景|
|-|-|-|-|
|正向代理|代表客户端向服务器发送请求，客户端主动配置代理地址|<li>隐藏客户端身份：服务器仅看到代理的 IP，而非真实客户端。<li>访问控制：限制或监控客户端访问特定资源（如企业网络管理）<li>绕过限制：突破地域或网络封锁（如访问被屏蔽的网站）<li>正向代理关注客户端隐私和控制|<li>公司内网通过代理访问外网。<li>用户通过 VPN 或科学上网工具访问受限内容|
|反向代理|代表服务器接收客户端请求，在服务端配置，对客户端透明|<li>隐藏服务器身份：客户端仅接触代理，无法直接访问后端服务器<li>负载均衡：将请求分发到多个后端服务器<li>安全防护：作为安全层抵御 DDoS 攻击、过滤恶意流量<li>SSL终端：处理 HTTPS 加密/解密，减轻后端压力<li>反向代理侧重服务端的负载与安全|<li>高流量网站使用 Nginx 处理并发请求|
