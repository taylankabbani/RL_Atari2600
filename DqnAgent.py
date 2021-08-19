""" Building an agent that will use DQN algorithm to play atari games """

from os import stat
import gym
import random
from gym import envs
from keras.backend_config import epsilon
from keras.optimizer_v2.rmsprop import RMSProp
import numpy as np
import flappy_bird_gym
from collections import deque
import utils



class DQNAgent:
    def __init__(self, env: str, memory_size: int, discount_factor: float, learning_rate:float, episodes: int):
        # Environment Variables
        self._env = self._set_env(env)
        self.state_space = self._env.observation_space.shape[0]
        self.action_space = self._env.action_space.n
        self.memory = deque(maxlen=memory_size)
        self.episodes = episodes
        self.train_start = 1000
        self.batch_size = 64

        # Learning hyperparameters
        self.gamma = discount_factor
        self.alpha = learning_rate 

        # Exploring parameters
        self.epsilon = 1 # start with 0.99 exploration rate
        self.epsilon_decay = 0.9999
        self.epsilon_min = 0.01
        self.jump_prob = 0.01
        
        # state-action approximation function
        self.model = self._build_deep_model()



    def _set_env(self, env:str):
        if env == "FlappyBird":
            return flappy_bird_gym.make("FlappyBird-v0")
        else:
            return gym.make(env)
        

    def _build_deep_model(self):
        """Building the NN network"""
        state_shape = self._env.observation_space.shape
        num_action = self._env.action_space.n
        model = utils.build_DenseNet(nn_input= state_shape, nn_output=(num_action))
        """Compile the network"""
        model.compile(optimizer= RMSProp(learning_rate=0.0001, rho=0.95, epsilon=0.01), loss = 'mse', 
            metrics=['accuracy'])
        return model

    def _get_q_value(self, state):
        """ using the action-value function Q (neural network) to get action values for the given state"""
        # reshaping state to be fed to the neural network
        state = np.reshape(state, (1, self.state_space))
        action_values = np.array(self.model(state))
        return action_values


    def actor(self, state):
        """The actor which is responsible of taking actions and exploring the env"""
        
        action_values = self._get_q_value(state)
        if np.random.random() > self.epsilon:
            return np.argmax(action_values)
        else:
            return 1 if np.random.random() < self.jump_prob else 0

    def _agent_start(self):
        state = self._env.reset()
        action = self.actor(state)
        return state, action
    
    def learn(self):
        # Make sure we have enough data
        if len(self.memory) < self.train_start:
            return
        
        # draw random samples from memory to train the neural network
        mini_batch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        #Variables to store minibatch info
        state = 

    def _agent_step(self):
        for i in range(self.episodes):
            state, action = self._agent_start()
            done = False
            score = 0
            self.epsilon = self.epsilon * self.epsilon_decay if self.epsilon * self.epsilon_decay > self.epsilon_min else self.epsilon_min

            # till the end of the episode
            while not done:
                self._env.render()
                next_state, reward, done, info = self._env.step(action)

                score += 1 # because in flappyBird if you are still alive you get a score
                
                # If we loss punish the agent
                if done:
                    reward -= 100
                    print("Episode: {}\nScore: {}\nEpsilon: {:.2}".format(i, score, self.epsilon))
                    #save model
                    
                # we save SARSA to make the updates
                self.memory.append(state, action, reward, next_state, done)
                state = next_state
                
                # Update weighs and TD  

            






        # print(height, width, channels)
        # nn_model = Sequential([
        #     Conv2D(filters=32, kernel_size=(8, 8), strides=(4, 4), activation="relu",
        #            input_shape=(self.batch_size, height, width, channels)),
        #     Conv2D(filters=64, kernel_size=(4, 4), strides=(2, 2), activation="relu"),
        #     Flatten(),
        #     Dense(units=512, activation="relu"),
        #     Dense(units=256, activation="relu"),
        #     Dense(units=self.actions, activation="linear")
        # ])
        # return nn_model

    # def _build_agent(self):
    #     """The policies the RL agent will follow to learn Q-value,  as it's off-policy, the agent will use one greedy
    #     policy to always choose the greedy action (Q-value) and another policy that will break the greedy action
    #     selection by rate of epsilon
    #     """
    #     pass

if __name__ == "__main__":
    test = DQNAgent(env='FlappyBird', memory_size=2000, discount_factor=0.99, learning_rate=0.5, episodes=1000)
    print(test._agent_start())
    print(test._agent_start())
    print(test._agent_start())