# ZhiJi-Release

织记（ZhiJi）Android 安装包的更新发布仓库，**只放 APK 与更新说明**，源码与开发记录在 `youyoudezhuzhu/ZhiJi`（私有）。

## 下载最新版本

到 [Releases](https://github.com/youyoudezhuzhu/ZhiJi-Release/releases) 页面，下载最新版本的 `ZhiJi-v*.apk` 覆盖安装即可，数据会保留（升级前建议先做完整备份）。

- 包名：`com.buku.fabric`
- 签名：固定为原证书，可直接覆盖升级；如提示签名不一致，请先卸载旧包但会丢失数据
- 版本号规则：`1.2.1a1 → a9 → b1 → …`，向后递增；**`aN` 是正式版本序列，不是 alpha 测试版**。
- 临时测试包才用 GitHub Release 的 pre-release 标记：标记后工作流不会更新 `stable.json`/Pages，正式用户不受影响。

## 发布机制（维护者）

- Pages 使用 **GitHub Actions artifact 部署**（Settings → Pages → Source: GitHub Actions），
  站点固定地址 `https://youyoudezhuzhu.github.io/ZhiJi-Release/`，直链 `dl/latest.apk` 不变。
- `.github/workflows/sync-pages-apk.yml` 在 Release 发布后自动：
  下载 Release 中的 APK / `update-manifest.json` → 校验 SHA-256 → 生成 `docs/dl/latest.apk` 与校验文件 →
  只提交 `stable.json`、`index.html` 等小文件（**APK 永不进入 git**）→ 删除除当前 tag 外的旧 Release → 部署 Pages artifact。
- 清单：`updates/stable.json`（raw 读取）与 `docs/dl/stable.json`（Pages 读取）内容一致。
- 本地发布脚本（源码仓库 `zhiji/scripts/publish_update.py`）会先建 draft Release、上传资产后再发布，避免工作流抢跑。
- 不要在 git 中提交任何 `.apk`；它们只属于 Release 资产与 Pages artifact。
- **环境策略**：`Settings → Environments → github-pages` 需要允许 `main` 分支与 `v*` tag 部署；
  否则 release 事件触发的 workflow 会 sync 成功、但 deploy job 在环境规则处立即失败（0 个步骤）。
  当前已配置 `main`、`gh-pages`、`v*`（tag）三条策略。

## 说明

- 本仓库不保存源码、不接收 Issue；问题反馈请在 App 内「设置 → 数据与支持 → 问题反馈」记录并导出诊断包。
