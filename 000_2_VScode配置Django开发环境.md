## 1. 环境说明

- os: windows 10
- python: 3.6.4
- django: 1.11.27 LTS
- commander: powershell (下面命令行均使用 powershell)
- code editor: vscode

> [django LTS版本周期](https://www.djangoproject.com/download/)：1.11:2017.12-2020.4  2.2:2019.12-2022.4。

## 2. python 环境

### 2.1 创建虚拟环境

此处使用 virtualenv 来创建虚拟的 python 环境：

```powershell
pip install virtualenv  # 安装 virtualenv 工具
virtualenv envName
```

此虚拟环境默认使用与原环境相同的 pip 源，更详细见其官网 [virtualenv](https://virtualenv.pypa.io/en/latest/userguide/#usage) 。

### 2.2 激活虚拟环境

推荐使用 powershell ，其有语法高亮、支持部分 unix shell 命令。

如果使用 powershell 激活，首次使用时需要允许权限，管理员打开并输入以下（官网说明: [activators](https://virtualenv.pypa.io/en/stable/user_guide.html#activators)）：

```powershell
Set-ExecutionPolicy RemoteSigned
# 输入: A
```

powershell 启动此虚拟环境，建议先到虚拟环境目标的 Scripts 文件夹下 `activate` 后再 cd 到程序路径，否则可能会无法启动虚拟环境(我的电脑是这样)：代码如下:

```powershell
$mypwd=pwd; cd \path\to\Scripts; .\activate; cd $mypwd
```

为了方便每次激活虚拟环境，我推荐将上面的放到 powershell 脚本(ps1 格式)，再放入环境变量中，每次可以在任意位置调用脚本进行激活。如我新建文件 `pydjango.ps1`，写入上面的内容，然后放到系统环境变量中，每次 powershell 输入 `pydj<tab>` 自动补全，再回车即可完成虚拟环境激活。下面总结的例子也是在此脚本激活。

虚拟环境激活后，当前 powershell 下就可以直接使用 pip 等操作虚拟环境了，如：

```powershell
pip install django==1.11.27
```

>如果未激活虚拟环境，可通过追加解释器路径使用 pip 等，如：
>
>```powershell
>\path\to\Scripts\python.exe -m pip install django==1.11.27
>```

## 3. vscode

### 3.1 vscode 设置

其他插件以及设置见上篇 [VScode Python环境配置]()。除了那些插件之外，还需要针对 Django 的插件：

[Django](https://github.com/rbtsolis/django-vscode): 高亮、 提示 django 模板语法，插件 ID 为:

```
bigonesystems.django;
```

django 模板中保留 Emmet 生成 html 代码以及插件 Beautify 的格式化方法：打开全局的 `settings`，追加下面内容即可:

```json
"[django-html]": {
    "editor.defaultFormatter": "HookyQR.beautify"
},
"emmet.includeLanguages": { "django-html": "html" },
```

另外由于 django 的部分对象是程序运行时动态生成，而代码格式检查和格式化工具 flake8 会存在部分误判，此处推荐 django 项目使用 vscode 默认的 pylint，并使用额外的模块即可，在项目目录 *.vscode* 的 `settings` 中追加:

```json
"python.linting.enabled": true,
"python.linting.pylintEnabled": true,
"python.linting.flake8Enabled": false,
"python.linting.pylintArgs": [
   "--load-plugins", "pylint_django"
],
```

### 3.2 创建项目

1. 如果是虚拟环境，且需要使用python解释器或者django命令行，则需要先激活虚拟环境，上面设置过 powershell 脚本并放入环境变量，则 `pydj<tab>` 回车即可完成激活。

2. 按 *Ctrl + Shift + P*，输入 *select*，选择 *Python: Select Workspace Interpreter*，在出现的选项中将 Python 解析器指向 env 文件夹中的python，或者在当前项目的 `.vscode/settings.json` 文件内追加，如：

   ```json
   {
   "python.pythonPath": "E:\\django_note\\python36_django\\Scripts\\python.exe"
   }
   ```

3. *launch.json* 可由插件自动生成，如果需要修改 ip 和 端口号等，在 *args* 字段内增改即可，如:

   ```json
   {
      "version": "0.2.0",
      "configurations": [
         {
               "name": "Python: Django",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}\\manage.py",
               "args": [
                  "runserver",
                  "--noreload"
               ],
               "django": true,
               "justMyCode": false,
         }
      ]
   }
   ```

4. 创建 django 项目到当前目录下(项目名后加 `.` 路径参数表示不创建项目外层的文件夹，直接在当前文件夹下创建项目文件)：

   ```powershell
   django-admin.exe startproject projectName .
   ```

5. 在编写视图函数时，给视图函数加 Type Hint，否则 vscode 无法代码提示，如:

   ```python
   from django.http import HttpResponse, HttpRequest
   
   def index(request: HttpRequest):
       print(f'path: {request.path}\n')
       return HttpResponse('index')
   ```

6. 如果正确配置了 *settings.json* 和 *launch.json* 则直接可以 debug，如 *F5* 快捷键等方式。
