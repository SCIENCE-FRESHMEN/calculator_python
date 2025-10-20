儿童益智计算器
一款专为儿童设计的集计算功能与数学游戏于一体的益智工具，让孩子在玩乐中提升数学能力特色亮点：

🧮 多功能计算：支持基础数学运算，配备输入验证确保计算准确

🎮 趣味数学游戏：包含俄罗斯方块、贪吃蛇、二十四点和速算挑战

🏆 成就系统：通过完成任务解锁成就，激发学习动力

🎨 儿童友好界面：生动的动画效果和简洁设计，适合儿童操作

💾 学习记录：自动保存计算历史和游戏成绩，跟踪学习进度

✨ 特性
基础计算功能：提供加、减、乘、除等基本运算，配备输入验证机制，帮助孩子养成正确的计算习惯。

多样化数学游戏：

二十四点：通过组合数字计算出24，锻炼四则运算能力

速算挑战：限时答题，提升计算速度和准确性

贪吃蛇：在游戏中融入数字元素，增强反应能力

俄罗斯方块：培养空间思维和逻辑能力

成就激励系统：设置多种成就目标，孩子完成后可获得反馈和奖励，增强学习动力。

历史记录追踪：自动保存计算过程和游戏成绩，方便家长了解孩子的学习进展。

自定义配置：可调整游戏难度、界面大小等参数，适应不同年龄段儿童的需求。

前置要求
Python 3.8 或更高版本

pip（Python包管理工具）

安装

bash
# 克隆仓库
git clone https://github.com/your-username/children-calculator.git
cd children-calculator

# 安装依赖
pip install -r requirements.txt


#基本用法

bash
# 运行程序
python main.py


启动后，你将看到主界面，可选择计算器功能或各类数学游戏。首次使用时，程序会自动创建必要的数据目录，用于存储计算历史和成就信息。

#📁 项目结构


children_calculator/
├── core/                  # 核心功能模块
│   ├── calculator_engine.py  # 计算器引擎
│   ├── validator.py          # 输入验证
│   ├── history_manager.py    # 历史记录管理
│   └── achievement_system.py # 成就系统
├── games/                 # 游戏模块
│   ├── tetris_game.py      # 俄罗斯方块
│   ├── twenty_four_game.py # 二十四点
│   ├── snake_game.py       # 贪吃蛇
│   └── quick_math.py       # 速算挑战
├── view/                  # 视图模块
│   ├── main_window.py      # 主窗口
│   ├── calculator_widget.py # 计算器界面
│   ├── game_widgets.py     # 游戏界面
│   └── components/         # UI组件
├── viewmodel/             # 视图模型
├── data/                  # 数据存储
│   ├── history.json        # 计算历史
│   └── achievements.json   # 成就数据
├── tests/                 # 测试代码
├── resources/             # 资源文件
│   ├── images/
│   └── sounds/
├── config.py              # 配置文件
├── main.py                # 入口文件
└── requirements.txt       # 依赖列表
```

🛠️ 配置

程序配置可通过 'config.py' 文件进行调整：
窗口大小：修改 'MIN_WIDTH' 和 'MIN_HEIGHT'
游戏难度：调整 'SNAKE_INITIAL_SPEED'、'QUICK_MATH_TIME_LIMIT'等参数
资源路径：设置图片和声音文件的存储位置

修改配置后，重启程序即可生效。

 🧪 高级用法

#打包成可执行文件

如需将程序打包为独立可执行文件（适用于没有安装Python的电脑）：

bash
# 使用PyInstaller打包
python setup.py


打包后的文件将生成在 `dist` 目录下。

# 运行测试

bash
# 运行所有测试
python -m unittest discover -s tests


🙏 致谢

感谢 [PyQt5](https://pypi.org/project/PyQt5/) 提供的GUI框架
感谢 [PyInstaller](https://pypi.org/project/pyinstaller/) 提供的打包功能
感谢所有为本项目做出贡献的开发者
