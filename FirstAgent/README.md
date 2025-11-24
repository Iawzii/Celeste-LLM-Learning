# FirstAgent 使用说明


**注意**：不要分享你的私人密钥。


**安装与启动**

- **安装依赖**: 在 `FirstAgent` 目录下执行以下命令来引入包依赖：

```powershell
uv sync
```

- **配置密钥**: 在 `.env` 文件中添加你的私人密钥，例如：

```
PRIVATE_KEY=your_private_key_here
```


- **启动项目**: 在 `FirstAgent` 目录下运行：

```powershell
uv run main.py
```


