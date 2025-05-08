import numpy as np
from gym import Env
from gym.spaces import Box, Discrete
from utils.render_utils import GridRenderer


class FireExtinguisherEnv(Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, render_mode="human", num_drones=5):
        super().__init__()
        self.num_drones = num_drones
        self.grid_size = 20
        self.num_actions = 5
        self.action_space = Discrete(self.num_drones * self.num_actions)

        # Observation space: 5 дрон (x,y) + 3 гал (x,y) = 16
        self.observation_space = Box(
            low=0,
            high=self.grid_size,
            shape=(16,),
            dtype=np.int32
        )

        self.render_mode = render_mode
        self.renderer = GridRenderer(grid_size=self.grid_size) if render_mode == "human" else None
        self.extinguished_fires = []  # Унтраасан галын жагсаалт

    def _get_obs(self):
        drone_pos = self.drones.flatten()

        if len(self.fires) == 0:
            fire_pos = np.zeros(6)
        elif len(self.fires) < 3:
            fire_pos = np.zeros(6)
            fire_pos[:len(self.fires)*2] = self.fires.flatten()
        else:
            fire_pos = self.fires.flatten()

        return np.concatenate([drone_pos, fire_pos])

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.drones = np.random.randint(0, self.grid_size, (self.num_drones, 2))
        self.fires = np.random.randint(0, self.grid_size, (3, 2))  # 3 галтай
        self.extinguished_fires = []  # Reset extinguished fires
        self.step_count = 0
        return self._get_obs(), {}

    def step(self, action):
        drone_id = action // self.num_actions
        move = action % self.num_actions

        prev_distances = [np.linalg.norm(self.drones[drone_id] - fire) for fire in self.fires]
        reward = 0
        terminated = False

        # Move drone
        if move == 0:
            self.drones[drone_id][1] = min(self.grid_size - 1, self.drones[drone_id][1] + 1)
        elif move == 1:
            self.drones[drone_id][1] = max(0, self.drones[drone_id][1] - 1)
        elif move == 2:
            self.drones[drone_id][0] = max(0, self.drones[drone_id][0] - 1)
        elif move == 3:
            self.drones[drone_id][0] = min(self.grid_size - 1, self.drones[drone_id][0] + 1)

        new_distances = [np.linalg.norm(self.drones[drone_id] - fire) for fire in self.fires]

        # Reward заавал давтах ёстой
        for i in range(len(prev_distances)):
            if new_distances[i] < prev_distances[i]:
                reward += 1
            elif new_distances[i] > prev_distances[i]:
                reward -= 0.5

        # Мөргөлдөх шагнал
        positions = [tuple(pos) for pos in self.drones]
        if len(positions) != len(set(positions)):
            reward -= 2

        # Ус шүрших үед шагнал
        hit = False
        if move == 4:
            for fire in list(self.fires):
                if np.array_equal(self.drones[drone_id], fire):
                    reward += 100
                    self.fires = np.array([f for f in self.fires if not np.array_equal(f, fire)])
                    self.extinguished_fires.append(list(fire))
                    hit = True
                    break
            if not hit:
                reward -= 0.1

        # Time penalty
        reward -= 0.01

        if len(self.fires) == 0:
            reward += 200
            terminated = True

        return self._get_obs(), reward, terminated, False, {}

    def render(self):
        if self.render_mode != "human":
            return

        if self.renderer is None:
            self.renderer = GridRenderer(grid_size=self.grid_size)

        self.renderer.init()
        self.renderer.render_grid()
        
        # Идэвхтэй болон унтраасан галыг render хийх
        self.renderer.render_fires(self.fires, extinguished_fires=self.extinguished_fires)
        self.renderer.render_drones(self.drones)
        self.renderer.update_display()

    def close(self):
        if self.renderer:
            self.renderer.close()
            self.renderer = None
        super().close()
