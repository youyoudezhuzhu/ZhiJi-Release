# 发布库使用指南（给发布者 / Agent）

本仓库是公开的 APK 发布库：GitHub Releases 存放安装包资产，GitHub Pages 提供下载页与更新清单。源码、开发和签名材料都不在这里。

> 两条硬规则：
> 1. **APK 和任何构建产物都不进 git**，只作为 Release 资产和 Pages artifact。
> 2. 这是公开仓库，**发布说明、清单、Release 描述里不能出现 Token、密钥、密码、本机路径、内部链接、用户数据或任何私有信息。**

---

## 1. 发布库的产出物

一次正式发布由三部分组成：

| 位置 | 内容 | 谁维护 |
| --- | --- | --- |
| GitHub Release | APK、校验文件、更新清单 | 发布者上传 |
| Pages | 下载首页、`dl/latest.apk` 直链、`dl/stable.json` 清单 | 工作流自动生成 |
| git | `updates/stable.json`、`docs/dl/stable.json`、`docs/index.html`、`docs/dl/SHA256SUMS-*.txt` | 工作流自动提交 |

APK 只存在于 Release 资产和 Pages artifact 中；`docs/dl/latest.apk` 被 `.gitignore` 忽略。

---

## 2. 版本与资产命名

- `versionCode` 必须**严格大于**线上版本；升级判断只看它。
- 版本名（`version_name`）按项目自己的序列递增即可，但必须与 APK 内一致。
- Release tag：`v<version_name>`。
- Release 标题：`织记 v<version_name>`。
- APK 资产名：`ZhiJi-v<version_name>-original-signed.apk`。
- 校验文件：`SHA256SUMS-<version_name>.txt`，每行 `<sha256>  <apk 文件名>`。
- 清单：`update-manifest.json`，与 Pages 的 `stable.json` 同构。

工作流按 `ZhiJi-v*-original-signed.apk` 匹配 APK，命名不符合会失败。

---

## 3. 发布前准备

1. 用与**线上已安装版本相同的签名**构建 APK。换签名会导致老用户无法覆盖升级。
2. 确认包名不变、`versionName`/`versionCode` 已更新。
3. 在本地验证 APK：能安装、启动、`aapt2 dump badging` 版本正确、`apksigner verify` 通过。
4. 计算 SHA-256、读取签名证书 SHA-256。
5. 准备发布说明（Markdown，面向用户，不含任何内部/隐私信息）。
6. 准备可操作本仓库的 GitHub 凭证（Token 或 `gh auth`），权限至少能创建 Release、触发 Actions。
   - 凭证只通过环境变量或 `gh auth login` 提供；
   - **不要写进命令历史、脚本、文档或仓库**。

---

## 4. 更新清单格式

`update-manifest.json` 示例（尖括号为占位符）：

```json
{
  "schema_version": 1,
  "channel": "stable",
  "version_name": "<version_name>",
  "version_code": <version_code>,
  "apk_url": "https://<owner>.github.io/<repo>/dl/latest.apk?v=<version_code>",
  "apk_url_alt": "https://github.com/<owner>/<repo>/releases/download/v<version_name>/ZhiJi-v<version_name>-original-signed.apk",
  "sha256": "<APK 的 SHA-256>",
  "signer_sha256": "<APK 签名证书 SHA-256>",
  "source_commit": "<构建提交，可留空>",
  "notes": "<发布说明 Markdown，与 Release 正文一致>",
  "published_at": "<UTC 时间，如 2026-01-01T00:00:00Z>"
}
```

要求：

- `version_name`、`version_code` 必须与 APK 内一致；
- `sha256` 必须与上传的 APK 字节一致；
- `notes` 与 Release 正文保持一致，便于更新器展示；它是 JSON 字符串，换行需要转义（`\n`），建议用脚本生成而不是手写；
- 不要放内部链接、私有仓库地址、构建机路径或用户信息。

生成校验文件：

```bash
# 先进入 APK 所在目录，保证校验文件里写的是资产文件名
sha256sum "ZhiJi-v<version_name>-original-signed.apk" > "SHA256SUMS-<version_name>.txt"
# 文件内容形如：<sha256>  ZhiJi-v<version_name>-original-signed.apk
```

一次 Release 只放一个匹配 `ZhiJi-v*-original-signed.apk` 的 APK；工作流只取匹配到的第一个。

读取签名证书 SHA-256：

```bash
apksigner verify --print-certs <apk> | grep 'SHA-256 digest'
```

---

## 5. 发布流程（推荐：gh CLI）

以下命令中的 `<owner>/<repo>` 替换为本仓库；`<tag>` 为 `v<version_name>`。

### 5.1 创建 Draft Release

先建草稿，避免资产未上传完就触发 Pages 工作流：

```bash
gh release create "<tag>" \
  --repo <owner>/<repo> \
  --target main \
  --title "织记 v<version_name>" \
  --notes-file release-notes.md \
  --draft
```

### 5.2 上传三个资产

```bash
gh release upload "<tag>" \
  --repo <owner>/<repo> \
  "ZhiJi-v<version_name>-original-signed.apk" \
  "SHA256SUMS-<version_name>.txt" \
  "update-manifest.json"
```

### 5.3 发布（触发 Pages 工作流）

```bash
# 取 Release id
REL_ID=$(gh api "repos/<owner>/<repo>/releases/tags/<tag>" --jq .id)
# draft -> published
gh api -X PATCH "repos/<owner>/<repo>/releases/$REL_ID" -F draft=false
```

发布后会自动触发 `Sync latest APK to GitHub Pages`。到 Actions 确认本次 run 成功。

### 5.4 也可以只在 GitHub 网页操作

1. Releases → Draft a new release；
2. 创建 tag `<tag>`，标题、说明填好；
3. 上传 3 个资产；
4. 确认资产齐全后点 Publish release；
5. 不要勾选 “Set as a pre-release”（pre-release 不会更新 Pages）。

---

## 6. Pages 是怎么更新的

`.github/workflows/sync-pages-apk.yml` 在 Release `published`（非 pre-release）或手动 dispatch 时运行：

1. 解析 Release tag，下载 `update-manifest.json`；
2. 校验清单字段，读取版本与 SHA-256；
3. 下载 Release 中的 APK，校验文件名与 SHA-256 是否和清单一致；
4. 生成 `docs/dl/latest.apk`、`docs/dl/SHA256SUMS-<版本>.txt`、两份 `stable.json`、`docs/index.html`；
5. 只在 Release 事件下删除除当前 tag 外的旧 Release 和 tag；
6. 提交很小的元数据文件（**不提交 APK**）；
7. 上传 `docs/` 为 Pages artifact，由 `actions/deploy-pages` 部署。

发布后：

- 下载页：`https://<owner>.github.io/<repo>/`
- APK 直链：`https://<owner>.github.io/<repo>/dl/latest.apk`
- Pages 清单：`https://<owner>.github.io/<repo>/dl/stable.json`
- raw 清单：`https://raw.githubusercontent.com/<owner>/<repo>/main/updates/stable.json`

两份清单内容一致，更新器会优先读 Pages，用 raw 作为兜底。

### 手动重跑 / 只刷新 Pages

```bash
# 用指定 Release 重新部署（不删除旧 Release）
gh workflow run sync-pages-apk.yml \
  --repo <owner>/<repo> \
  --ref main \
  -f tag=<tag>

# 不带 tag：同步最新非 pre-release
gh workflow run sync-pages-apk.yml \
  --repo <owner>/<repo> \
  --ref main
```

注意：手动 dispatch 只刷新 Pages，**不会**清理旧 Release。

---

## 7. 发布后核验

1. Release 只有当前版本，tag 正确，3 个资产齐全；
2. Pages 清单的 `version_name`、`version_code`、`sha256` 与 Release 一致；
3. 下载 `dl/latest.apk` 后 SHA-256 与清单一致；
4. 下载页显示的版本号正确；
5. 本次 Actions run 结论为成功；
6. `docs/dl/SHA256SUMS-*.txt` 只剩当前版本；
7. 仓库里没有任何 APK 被提交。

只读核验命令：

```bash
curl -fsSL https://<owner>.github.io/<repo>/dl/stable.json
curl -fsSL -o /tmp/latest.apk https://<owner>.github.io/<repo>/dl/latest.apk
sha256sum /tmp/latest.apk
```

Pages/CDN 刷新可能有几分钟延迟；超过约 10 分钟仍是旧内容，按下一节重试。

---

## 8. 常见问题

| 现象 | 处理 |
| --- | --- |
| 发布 Release 后 Actions 没触发 | 检查是否 draft 或 pre-release；检查工作流是否启用 |
| 工作流报 APK sha mismatch | `update-manifest.json` 的 `sha256` 与实际上传的 APK 不一致，重新生成后重传 |
| 工作流报清单/资产缺失 | 确认 3 个资产名完全符合第 2 节命名 |
| `deploy` 在 0 个步骤失败 | 仓库 `github-pages` 环境策略需允许 `main` 分支和 `v*` tag |
| Pages 仍是旧版 | 可能 CDN 延迟；或本次部署与上次 build version 相同被忽略，手动 dispatch 一次 |
| 旧 Release 没被删 | 自动清理只在 Release `published` 事件运行；手动 dispatch 不删除，需要手动删 |
| 下载页 404 | 确认 Pages Source 为 GitHub Actions，且 deploy job 成功 |
| 直链下载到旧 APK | 换带版本参数的 URL（`?v=<version_code>`）或稍后重试 |
| pre-release 后 Pages 没变 | 这是预期行为；正式发布请用非 pre-release |

---

## 9. 安全与保密

- 公开仓库，任何提交、Release 说明、清单、文件名都相当于公开：不要包含 Token、密码、密钥、私有仓库地址、内网地址、本机绝对路径、用户数据、内部待办。
- 发布说明只写用户能看懂的功能与验证结论；不要贴内部日志、代码路径、账号信息。
- APK 必须与线上版本同包名、同签名；签名材料只保存在构建方本地。
- 不提交任何 `.apk` 到 git；不改 `.gitignore` 里的 `docs/dl/latest.apk`。
- 需要凭证时只通过环境变量/`gh auth`，不要 `echo`、不要写入文件。
- 如果误传了敏感内容：立即删除/替换该 Release 资产或提交，并通知维护者轮换凭证。

---

## 10. 维护者配置（只需了解）

- Pages Source 必须是 **GitHub Actions**（不是分支 `/docs`）。
- `github-pages` 环境需允许 `main` 分支和 `v*` tag，否则 Release 触发的 deploy 会失败。
- 工作流所需权限：`contents: write`、`pages: write`、`id-token: write`。
- 不要手工修改 `docs/index.html`、`docs/dl/stable.json`、`updates/stable.json`；它们由工作流按 Release 内容生成。
- 删除旧 Release 的行为由工作流在 Release 事件中执行，保留策略以当前工作流为准。

---

## 11. 一页速查

```bash
# 构建、验证 APK（用自己的构建方式）
# 1) 建草稿
gh release create "v<版本>" --repo <owner>/<repo> --target main \
  --title "织记 v<版本>" --notes-file release-notes.md --draft
# 2) 传资产
gh release upload "v<版本>" --repo <owner>/<repo> \
  "ZhiJi-v<版本>-original-signed.apk" \
  "SHA256SUMS-<版本>.txt" "update-manifest.json"
# 3) 发布
REL_ID=$(gh api "repos/<owner>/<repo>/releases/tags/v<版本>" --jq .id)
gh api -X PATCH "repos/<owner>/<repo>/releases/$REL_ID" -F draft=false
# 4) 看工作流
gh run list --repo <owner>/<repo> --workflow sync-pages-apk.yml --limit 5
# 5) 核验
curl -fsSL https://<owner>.github.io/<repo>/dl/stable.json
```
