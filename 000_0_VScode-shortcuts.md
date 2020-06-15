目前常用的快捷键，有其他新的频繁使用的快捷键后再添加。

## 1. 代码选择快捷键

- 列选择：`ctrl+shift+鼠标左击` 或者 按压鼠标滚轮滚动
- 选择下一个匹配：`ctrl+d` ，首次使用是选择相邻对象
- 选择所有匹配：`ctrl+shift+L` 选择所有匹配

`ctrl+left/right`: 向左/右以对象间隔移动光标
`shift+left/right`：向左/右继续选择字符，可以随时再按 `ctrl` 以选择对象。

## 2. 其他快捷键

- 代码格式化：`shift+alt+f`
- 复制当前代码：`shift+alt+up` 或 `shift+alt+down`
- 打开终端：``ctrl+` ``
- 命令面板：`ctrl+shift+p`
- 同步设置：`ctrl+shift+p --> sync`。(插件 *Settings Sync*)
  上传配置：`shift+alt+u`，下载配置：`shift+alt+d`
- 编辑器视图滚动：上: `ctrl+up`, 下: `ctrl+down`, 左右
- 折叠代码：`ctrl+k ctrl+0`
  展开折叠：`ctrl+k ctrl+j`

## 3. 快捷键更改

1. 互换 *Go forward/back* (`alt+left/right`) 与 *open previous/next editor* (`ctrl+pgup/pgdown`) 的快捷键，以方便使用 `alt+left/right` 切换编辑器组内文件。

    ```json
    {
        "key": "alt+right",
        "command": "workbench.action.nextEditor"
    },
    {
        "key": "ctrl+pagedown",
        "command": "-workbench.action.nextEditor"
    },
    {
        "key": "alt+left",
        "command": "workbench.action.previousEditor"
    },
    {
        "key": "ctrl+pageup",
        "command": "-workbench.action.previousEditor"
    },
    {
        "key": "ctrl+pageup",
        "command": "workbench.action.navigateBack"
    },
    {
        "key": "alt+left",
        "command": "-workbench.action.navigateBack"
    },
    {
        "key": "ctrl+pagedown",
        "command": "workbench.action.navigateForward"
    },
    {
        "key": "alt+right",
        "command": "-workbench.action.navigateForward"
    },
    ```

2. 更改代码提示，将原本的 `ctrl+space` 修改为 `alt+/`：

   ```json
   {
       "key": "alt+oem_2",
       "command": "editor.action.triggerSuggest",
       "when": "editorHasCompletionItemProvider && textInputFocus && !editorReadonly"
   },
   {
       "key": "ctrl+space",
       "command": "-editor.action.triggerSuggest",
       "when": "editorHasCompletionItemProvider && textInputFocus && !editorReadonly"
   },
   ```
