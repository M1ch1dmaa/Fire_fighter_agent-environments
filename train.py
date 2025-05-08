from ppo_trainer import train_ppo, load_and_test

print(">>> Training script started <<<")

if __name__ == "__main__":
    print("Training PPO Agent...")
    train_ppo()

    print("\nTesting trained agent...")
    load_and_test()
