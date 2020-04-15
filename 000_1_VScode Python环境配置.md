## 1. windows鼠标右键打开项

vscode windows鼠标右键打开项，新建 reg 文件并写入以下内容（修改 `D:\\vscode` 为自己安装路径）后双击添加到注册表:

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\Open with VScode]

[HKEY_CLASSES_ROOT\*\shell\Open with VScode\command]
@="D:\\vscode\\Code.exe \"%1\""


[HKEY_CLASSES_ROOT\Directory\shell\VScode]
@="Open Folder in VScode"
"Icon"="D:\\vscode\\Code.exe"

[HKEY_CLASSES_ROOT\Directory\shell\VScode\command]
@="\"D:\\vscode\\Code.exe\" \"%1\""
```

## 2. 插件推荐

1. [Python](https://github.com/Microsoft/vscode-python): 提示、调试 Python；
2. [Visual Studio Intellicode](https://github.com/MicrosoftDocs/intellicode): Python 代码 AI 提示；
3. [Setting Sync](https://github.com/shanalikhan/code-settings-sync.git): 同步 vscode 插件以及设置到 github gist；
4. [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint): markdown 格式检查与格式化；
5. [Markdown Preview Enhanced](https://github.com/shd101wyy/vscode-markdown-preview-enhanced): markdown 预览插件，支持目录、公式等;
6. [Beautify](https://github.com/HookyQR/VSCodeBeautify): 美化 js、css、html、json；
7. [MySQL](https://github.com/formulahendry/vscode-mysql.git): 连接 mysql 数据库；
8. [MySQL Syntax](https://github.com/jakebathman/mysql-syntax): mysql 语法提示；
9. [Monokai Pro](https://marketplace.visualstudio.com/items?itemName=monokai.theme-monokai-pro-vscode): Monokai 主题。

为了复制方便，此处把上面插件的 id 放在一起，粘贴到 vscode 插件搜索框:

```
ms-python.python;
visualstudioexptteam.vscodeintellicode;
shan.code-settings-sync;
davidanson.vscode-markdownlint;
shd101wyy.markdown-preview-enhanced;
hookyqr.beautify;
formulahendry.vscode-mysql;
jakebathman.mysql-syntax;
monokai.theme-monokai-pro-vscode;
```

## 3. 编辑器其他全局设置

以下的对 *settings* 的更改均为**全局设置**（而不是项目设置），以 json 打开全局 `settings` 的快捷方法: `ctrl+shift+p` 打开命令搜索窗口，搜索 *settings*，点击 *Open Settings (JSON)*。

如果是开发 Django 项目，还需要其他插件和设置，见下篇 [VScode配置Django开发环境](https://www.brothereye.cn/python/754/)

> 项目设置是针对当前项目的设置，每个项目创建时都要生成，其会覆盖同字段的全局设置，目录为 *.vscode/settings.json*，对于 python 项目通常只设置 python 解释器路径以及其他针对某些特定项目的设置。

### 3.1 代码格式检查及格式化

vscode 中 默认的 Python 代码格式检查工具为 pylint，此处更改为 flake8，格式化工具使用 autopep8。`settings` 中追加下面即可:

```json
"python.linting.enabled": true,
"python.linting.pylintEnabled": false,
"python.linting.flake8Enabled": true,
// "python.linting.flake8Path": "{python installed path}\\Scripts\\flake8.exe",

"python.formatting.autopep8Path": "autopep8",
//"python.formatting.autopep8Path": "{python installed path}\\Scripts\\autopep8.exe",
```

完成更改后，再后续使用代码格式化时 vscode 会自动提示下载缺失的 python 库，如果是虚拟环境，可指定 flake8Path 和 autopep8Path（上面注释的两行），从其他环境的安装路径中引入即可，这样可避免每个虚拟环境都下载安装 flake8 和 autopep8。

> pylint vs flake8: pylint 格式太过严格，比如要求函数的说明文档等等。

### 3.2 代码提示

Visual Studio Intellicode 智能提示可以 AI 预测开发者需要的 api，代码提示中加星号的就是推荐的 api。
Python 智能提示需要基于 MicroSoft 的 Python language server，故需要关闭静态分析的 Jedi，`settings` 中添加:

```json
"python.jediEnabled": false,
```

如果上面设置后仍然无法出现带星号的推荐，检查设置(菜单：'File' -> 'preference' -> 'settings')中 `"python.languageServer"` 是否为 `"Microsoft"`。

### 3.3 markdownlint 忽略规则

如果自己需要忽略什么规则，在 `settings` 中添加配置即可，如忽略 MD041 规则(规则为: first-line-heading/first-line-h1 - First line in file should be a top level heading)，则 `settings` 中添加如下:

```json
"markdownlint.config": {
    "MD041": false
},
```

### 3.4 代码调试

如果调试时需要对库函数也加断点或捕获错误，需要在项目目录 *.vscode* 下 `launch.json` 的 *configurations* 后加 `"justMyCode": false,`，如:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File (Integrated Terminal)",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false,
        },
    ]
}
```
