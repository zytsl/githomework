# unit-converter

一个用于练习 **远程仓库 / 分支 / Pull Request / 代码评审 / 合并** 完整流程的极简 demo 项目。
A tiny demo project for practising the full remote-repo → branch → PR → review → merge workflow.

当前版本只做一件事：**单位换算**（长度、质量、体积、温度）。

## 支持的单位 / Supported units

| 类别 | 单位 |
| --- | --- |
| length | `um` `mm` `cm` `m` `km` `in` `ft` `yd` `mi` `nmi` |
| mass | `mg` `g` `kg` `t` `oz` `lb` `st` |
| volume | `ml` `l` `m3` `gal` |
| temp | `c` `f` `k` |

## 运行 / Usage

```bash
# 换算 / convert
python -m src.cli 3 km mi
python -m src.cli 100 c f
python -m src.cli 1 lb g
python -m src.cli 1 gal l

# 查看支持的单位 / list units
python -m src.cli --list
```

输出示例：

```text
$ python -m src.cli 3 km mi
3.0 km = 1.8641135767120018 mi
```

## 测试 / Tests

无需安装任何依赖 / No third-party dependency required:

```bash
python tests/test_converter.py
```

## 目录结构 / Layout

```text
unit-converter/
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── converter.py   # 换算核心逻辑
│   └── cli.py         # 命令行入口
└── tests/
    └── test_converter.py
```

## 参与贡献 / Contributing

1. 从 `main` 新建分支：`git switch -c feature/<你的名字>`
2. 小步提交，提交信息写清楚改了什么、为什么改
3. 推送到远程并开 Pull Request，指定 reviewer
4. 根据评审意见在原分支上追加提交，PR 会自动更新
5. reviewer 确认后合并到 `main`
