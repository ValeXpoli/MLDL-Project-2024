"""Train an RL agent on the OpenAI Gym Hopper environment using
    REINFORCE and Actor-critic algorithms
"""
import argparse

import torch
import gym

from env.custom_hopper import *
from reinforce_agent import Agent, Policy
from torch.utils.tensorboard import SummaryWriter
import tensorflow as tf


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n-episodes", default=100000, type=int, help="Number of training episodes"
    )
    parser.add_argument(
        "--print-every", default=20000, type=int, help="Print info every <> episodes"
    )
    parser.add_argument(
        "--device", default="cpu", type=str, help="network device [cpu, cuda]"
    )
    parser.add_argument(
        "--outName",
        default="model.mdl",
        type=str,
        help="name of the output filename",
    )
    parser.add_argument("--log", default="./logs", type=str, help="tensorboard dir")
    return parser.parse_args()


args = parse_args()


def main():
    env = gym.make("CustomHopper-source-v0")
    # env = gym.make('CustomHopper-target-v0')

    print("Action space:", env.action_space)
    print("State space:", env.observation_space)
    print("Dynamics parameters:", env.get_parameters())

    """
        Training
    """
    observation_space_dim = env.observation_space.shape[-1]
    action_space_dim = env.action_space.shape[-1]

    policy = Policy(observation_space_dim, action_space_dim)
    agent = Agent(policy, device=args.device)

    #
    # TASK 2 and 3: interleave data collection to policy updates
    #
    writer = SummaryWriter(log_dir=args.log)

    for episode in range(args.n_episodes):
        done = False
        train_reward = 0
        state = env.reset()  # Reset the environment and observe the initial state
        while not done:  # Loop until the episode is over
            action, action_probabilities = agent.get_action(state)
            previous_state = state

            state, reward, done, info = env.step(action.detach().cpu().numpy())

            agent.store_outcome(
                previous_state, state, action_probabilities, reward, done
            )

            train_reward += reward

        if (episode + 1) % args.print_every == 0:
            print("Training episode:", episode)
            print("Episode return:", train_reward)

        agent.update_policy()
        writer.add_scalar('Reward/Episode', train_reward, episode)

    torch.save(agent.policy.state_dict(), args.outName)


if __name__ == "__main__":
    main()
