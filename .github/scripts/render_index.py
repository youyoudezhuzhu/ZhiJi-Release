#!/usr/bin/env python3
"""Render docs/index.html from the release update-manifest.json."""
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
size_mb = int(sys.argv[2]) / (1024.0 * 1024.0)
output = sys.argv[3]

def esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;")

html = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>织记 · APK 下载</title>
<style>
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f6f2ea;color:#3d3a34;margin:0;padding:32px 20px;line-height:1.7}
main{max-width:560px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}
p{color:#6f6a61;margin:6px 0}
.card{background:#fffdf8;border-radius:16px;padding:20px;margin:20px 0;box-shadow:0 2px 10px rgba(80,60,30,.06)}
a.btn{display:block;text-align:center;background:#6f7f5a;color:#fff;text-decoration:none;border-radius:12px;padding:14px;font-weight:600}
code{background:#efe9de;border-radius:6px;padding:2px 6px;word-break:break-all;font-size:12px}
pre{white-space:pre-wrap;color:#6f6a61;font-size:13px;margin:0}
.foot{color:#a39b8f;font-size:12px}
</style>
</head>
<body>
<main>
<h1>织记 · 自然</h1>
<p>本地优先的手作记录应用 · Android 8.0+</p>
<div class="card">
<p><strong>最新版本 %s（versionCode %d）</strong></p>
<a class="btn" href="dl/latest.apk">下载最新 APK（%.1f MB）</a>
<p>下载后请覆盖安装，数据会保留；升级前建议先在 App 内做完整备份。</p>
</div>
<div class="card">
<p>SHA-256：<code>%s</code></p>
<p>签名证书：<code>%s</code></p>
<p>构建提交：<code>%s</code></p>
<p>发布时间：%s</p>
</div>
<div class="card">
<p><strong>更新说明</strong></p>
<pre>%s</pre>
</div>
<p class="foot">更新清单：<a href="dl/stable.json">dl/stable.json</a> · 历史版本见 <a href="https://github.com/youyoudezhuzhu/ZhiJi-Release/releases">GitHub Releases</a></p>
<p class="foot">所有文件通过 HTTPS 分发；App 下载后会校验 SHA-256 与 APK 签名。</p>
</main>
</body>
</html>
""" % (
    esc(manifest.get("version_name", "")),
    int(manifest.get("version_code") or 0),
    size_mb,
    esc(manifest.get("sha256", "")),
    esc(manifest.get("signer_sha256", "")),
    esc(manifest.get("source_commit", "")),
    esc(manifest.get("published_at", "")),
    esc(manifest.get("notes", "")),
)
with open(output, "w", encoding="utf-8") as handle:
    handle.write(html)
print("rendered", output)
