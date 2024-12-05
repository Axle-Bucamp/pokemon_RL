# 🎮 Pokémon Showdown Reinforcement Learning Agent

## 🚀 Project Overview

This project implements a reinforcement learning approach to playing Pokémon battles using a custom AI agent that learns and improves its strategy through interactions with the Pokémon Showdown battle simulator.

## ✨ Features

- Multi-agent reinforcement learning
- WebSocket-based battle interaction
- Dynamic action selection
- Adaptive learning strategy
- Penalty mechanisms for invalid actions

## 🛠️ Technical Components

### Key Technologies
- TensorFlow for neural network modeling
- WebSocket for real-time battle communication
- Custom preprocessing for battle state representation

### Learning Approach
- Stochastic action selection
- Reward-based training
- Error and switching action penalties

## 📋 Prerequisites

### Dependencies
- Python 3.8+
- TensorFlow
- NumPy
- Pandas
- WebSocket-client

### Installation
```bash
pip install tensorflow numpy pandas websocket-client
```

## 🎲 Configuration

### Battle Parameters
- Episodes: 10
- Maximum Turns per Battle: 100
- Number of Agents: 4
- Battle Format: Gen 7 Random Battle

### Possible Actions
- Move actions: "move 1", "move 2", "move 3", "move 4"
- Switch actions: "switch 1" to "switch 6"

## 🤖 How It Works

1. Initialize multiple AI models
2. Connect to Pokémon Showdown WebSocket
3. Preprocess initial battle state
4. Select and execute actions using trained models
5. Calculate rewards and penalties
6. Train models based on battle outcomes

## 🧪 Running the Program

```bash
python pokemon_showdown_rl.py
```

## 🔍 Key Functions

- `get_players_data()`: Extract battle state
- `preprocess_to_stochastic()`: Convert game state to ML-compatible format
- `train_p1/train_p2()`: Model training functions

## 🚧 Current Limitations

- Fixed number of episodes
- Potential action selection issues
- Limited error handling

## 📊 Performance Metrics

The agent learns by:
- Minimizing action errors
- Penalizing unnecessary switches
- Maximizing total life preservation

## 🔮 Future Improvements

- Enhanced error handling
- More sophisticated reward mechanism
- Support for different battle formats
- Improved state representation

## 🤝 Contributing

Contributions are welcome! Please submit pull requests or open issues for discussion.

## 📄 License

[Specify your license]

## 👥 Contact

[Your contact information]

## 🙏 Acknowledgments

- Pokémon Showdown
- TensorFlow Team
- Open-source community

## todo
- easy install
- fix fainted bug
- save and load model
- multi-model training (Darwin tree or challenge between model)
- fix inversed player data
- clean and optimize the code (filthy there)
