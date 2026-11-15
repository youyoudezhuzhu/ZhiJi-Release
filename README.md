# ZhiJi-Release

织记（ZhiJi）Android 安装包的公开更新发布库：**只放 APK 发布资产、更新清单和 Pages 下载页**，不保存源码、开发记录或签名材料。

## 下载最新版本

到 [Releases](https://github.com/youyoudezhuzhu/ZhiJi-Release/releases) 页面，下载最新的 `ZhiJi-v*.apk` 覆盖安装即可，数据会保留（升级前建议先做完整备份）。

- 包名：`com.buku.fabric`
- 签名：固定为原证书，可直接覆盖升级；如提示签名不一致，请先卸载旧包，但会丢失数据
- 版本号规则：`1.2.1a1 → a9 → b1 → …`，向后递增；**`aN` 是正式版本序列，不是 alpha 测试版**
- 临时测试包才用 GitHub Release 的 pre-release 标记：标记后不会更新 `stable.json`/Pages，正式用户不受影响

## 发布者 / Agent 文档

如果你要发布新版本、更新 Pages 或排查发布问题，请先读：

**[docs/RELEASE_GUIDE.md](docs/RELEASE_GUIDE.md)**

里面包含：版本与资产命名、更新清单格式、草稿 Release 上传与发布步骤、Pages 自动更新机制、手动刷新、发布后核验、常见问题与安全红线。

## 仓库内容

- Release 资产：APK、`SHA256SUMS-<版本>.txt`、`update-manifest.json`
- Pages 站点文件：`docs/index.html`、`docs/dl/stable.json`、`docs/dl/SHA256SUMS-*.txt`
- 更新清单副本：`updates/stable.json`
- `docs/dl/latest.apk` 由 Pages artifact 提供，**不进入 git**

## 说明

- 本仓库不保存源码、不接收 Issue；问题反馈请在 App 内「设置 → 数据与支持 → 问题反馈」记录并导出诊断包。
- 这是公开仓库，请勿提交或发布任何 Token、密钥、密码、本机路径、私有链接或用户数据。
