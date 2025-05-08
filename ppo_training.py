from stable_baselines3 import PPO
from environments.fire_env import FireExtinguisherEnv
import os

def train_ppo():
    env = FireExtinguisherEnv()
    tensorboard_log = os.path.join(os.getcwd(), "ppo_fire_extinguisher_tensorboard")
    os.makedirs(tensorboard_log, exist_ok=True)
    model = PPO("MlpPolicy",
                env, 
                verbose=1, 
                ent_coef=0.08, 
                n_steps=2048, 
                batch_size=64, 
                n_epochs=10, 
                learning_rate=3e-4,
                policy_kwargs=dict(net_arch=[256, 256]),
                clip_range=0.2,
                gamma=0.99,)
    model.learn(total_timesteps=10000000, tb_log_name="PPO")
    model.save("fire_extinguisher_model")
    print("Model saved!")


def load_and_test():
    env = FireExtinguisherEnv()
    model = PPO.load("fire_extinguisher_model")
    env = FireExtinguisherEnv(render_mode="human")
    obs, _ = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)
        env.render()
        if done or truncated:
            break
    env.close()
