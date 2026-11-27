# yt-dlp 网易云电台音质插件

用 `yt-dlp -F` 查看部分网易云电台节目时，列表里只有 128 kbps，但这些节目可能还有 192 或 320 kbps 的版本。原因是网易云有时只返回音频链接，没带上标明音质档位的 `level` 字段。遇到这种情况，yt-dlp 拿到 128 kbps 的链接就停了。 [yt-dlp Issue #16169](https://github.com/yt-dlp/yt-dlp/issues/16169)

直接改源码的话，更新 yt-dlp 后可能得再改一遍。装上这个插件就省了这一步。插件会接着查 192 和 320 kbps，按网易云实际返回的码率列出可用格式。如果不同档位拿到的是同一份音频，列表里只显示一次。

## 1. 安装插件（Windows）

1. 打开本仓库的 **Releases** 页面，在最新版本的 **Assets**（附件）里找到并下载 `netease-program-quality.zip`。
2. 找到存放 `yt-dlp.exe` 的文件夹，在里面新建一个名为 `yt-dlp-plugins` 的文件夹。
3. 把 ZIP 放进 `yt-dlp-plugins` 文件夹，保持压缩包原样。放好后，目录如下。

```text
yt-dlp.exe
yt-dlp-plugins/
└── netease-program-quality.zip
```

[yt-dlp 官方插件安装说明](https://github.com/yt-dlp/yt-dlp#installing-plugins)

## 2. 确认插件已加载

在资源管理器里打开 `yt-dlp.exe` 所在的文件夹。在地址栏输入 `powershell`，按回车，然后运行下面的命令。它会显示调试日志和音质列表，不会下载音频。

```powershell
.\yt-dlp.exe --no-playlist -v -F 'https://music.163.com/#/program?id=2541901866'
```

日志出现下面这一行，就表示 yt-dlp 已加载插件。

```text
[debug] Extractor Plugins: netease-program-quality (NetEaseMusicProgramIE)
```

如果没看到插件名称，先检查 `yt-dlp-plugins` 文件夹是不是就在 `yt-dlp.exe` 旁边，再确认 ZIP 放进了这个文件夹。

## 3. 用 `-F` 检查音质

看上面那条命令最后输出的表格。**ABR** 是音频码率，**ID** 是下载时用来选档位的值。在 Windows 上用 yt-dlp `2026.11.23` 测试这期节目时，免费账号就能查到下面三档 MP3。

| ID | 格式 | ABR |
| --- | --- | --- |
| `abr-128` | MP3 | 128 kbps |
| `abr-192` | MP3 | 192 kbps |
| `abr-320` | MP3 | 320 kbps |

换成你要下载的节目链接，就能看到那一期有哪些档位。如果网易云没返回 `level`，这个版本最多查到 320 kbps。

## 4. 下载音频

把示例链接换成你要下载的节目。下面的命令会选这期节目码率最高的一档，把音频存到当前文件夹。

```powershell
.\yt-dlp.exe --no-playlist -f ba -S abr 'https://music.163.com/#/program?id=2541901866'
```

如果格式表里有 `abr-320`，也可以将 `-f ba -S abr` 换成 `-f abr-320`，固定下载这一档。

## 从源码打包

在仓库根目录运行下面的命令。生成的 ZIP 可以按上面的安装步骤使用。

```powershell
python -m zipfile -c netease-program-quality.zip yt_dlp_plugins
```

这个插件基于 yt-dlp 的网易云节目提取器，借助 AI 编写，并在 Windows 上实际试用过。
