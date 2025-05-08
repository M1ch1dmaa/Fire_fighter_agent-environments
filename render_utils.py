import pygame

class GridRenderer:
    def __init__(self, grid_size=20, cell_size=40):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.screen = None
        self.clock = None
        self.is_initialized = False

    def init(self):
        if not self.is_initialized:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (self.grid_size * self.cell_size, self.grid_size * self.cell_size)
            )
            self.clock = pygame.time.Clock()
            self.is_initialized = True

    def render_grid(self):
        self.screen.fill((255, 255, 255))  # White background

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def render_fires(self, fires, extinguished_fires_list=None):
        """
        fires: идэвхтэй галын жагсаалт [[x1,y1], [x2,y2], ...]
        extinguished_fires: унтраасан галын жагсаалт [[x3,y3], ...]
        """
        if extinguished_fires_list is None:
            extinguished_fires_list = []

        # Идэвхтэй гал - улаан
        for fx, fy in fires:
            rect = pygame.Rect(fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (255, 87, 34), rect)  # Deep Orange

        # Унтраасан гал - цэнхэр
        for fx, fy in extinguished_fires_list:
            rect = pygame.Rect(fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (100, 100, 255), rect)  # Light Blue

    def render_drones(self, drones):
        for i, (x, y) in enumerate(drones):
            center = (int((x + 0.5) * self.cell_size), int((y + 0.5) * self.cell_size))
            pygame.draw.circle(self.screen, (33, 150, 243), center, self.cell_size // 3)  # Blue color

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(10)

    def close(self):
        if self.is_initialized:
            pygame.quit()
            self.is_initialized = False
