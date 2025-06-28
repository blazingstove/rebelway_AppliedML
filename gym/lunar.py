'''
lunar.py

Trains the LunarLander environment from ai gym, 
while periodically logging step data and video results

'''

import gym
import os
import wandb
from wandb.integration.sb3 import WandbCallback
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder
from stable_baselines3.common.evaluation import evaluate_policy

env_name = "LunarLander-v2"

def make_env():
    env = gym.make(env_name, render_mode="rgb_array")
    return env

def train_ppo(env_name=env_name, policy="MlpPolicy", time_steps=350000, eval_episodes=20):
    
    config = {
        "policy_type" : policy,
        "total_timesteps" : time_steps,
        "env_name" : env_name}

    run = wandb.init(
        project=f"{env_name}_gym",
        config=config, 
        sync_tensorboard=True,
        monitor_gym=True,
        save_code=True)
    
    env = gym.make(config["env_name"], render_mode="rgb_array")
    env = DummyVecEnv([make_env])
    env = VecVideoRecorder(env, f"videos/{run.id}", record_video_trigger=lambda x:x % 200==0, video_length=200)
    
    model = PPO(config['policy_type'], env, verbose=1, tensorboard_log=f"runs/{run.id}")
    model.learn(
        total_timesteps=config["total_timesteps"],
        callback=WandbCallback(gradient_save_freq=100, model_save_path=f"models/{run.id}", verbose=2),
    )

    PPO_path = os.path.join('Training', 'Saved Models', f'PPO_{env_name.replace("-","_")}_{time_steps}')
    model.save(PPO_path)

    evaluate_policy(model, env, n_eval_episodes=eval_episodes, render=True)
    
    run.finish()

if __name__ == "__main__":
    train_ppo()






