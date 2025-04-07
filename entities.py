import pygame
import utils


class Entity:
    def __init__(self, game, entity_type, position, size):
        self.game = game
        self.type = entity_type
        self.position = list(position)
        self.size = size

        self.action = ""  # default action
        self.set_action("idle/idle")  # set the default action to idle
        self.flip = False  # default flip
        self.speed = 50  # default speed

    def rectangle(self, offset=(0, 0)):
        return pygame.Rect(
            self.position[0] - offset[0],
            self.position[1] - offset[1],
            self.size[0],
            self.size[1],
        )

    def set_action(self, action):
        if action != self.action:
            # set the action to the new action
            self.action = action
            # get the new animation from the game files
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def get_action(self):
        action_copy = self.action.split("/")
        print(action_copy)
        return action_copy[-1]

    def update(self, movement=(0, 0, 0, 0)):
        if (movement[0] and (movement[2] or movement[3])) or (
            movement[1] and (movement[2] or movement[3])
        ):
            # moving the player diagonally makes him move faster due to the pythagorean theorem
            self.position[0] += (
                (movement[3] - movement[2]) * self.game.delta_time * self.speed * 0.7071
            )
            self.position[1] += (
                (movement[1] - movement[0]) * self.game.delta_time * self.speed * 0.7071
            )
        else:
            self.position[0] += (
                (movement[3] - movement[2]) * self.game.delta_time * self.speed
            )
            self.position[1] += (
                (movement[1] - movement[0]) * self.game.delta_time * self.speed
            )

        entity_rectangle = self.rectangle()
        if movement[3] == True:
            self.flip = False
        elif movement[2] == True:
            self.flip = True

    def render(self, surface, offset=(0, 0)):

        surface.blit(
            pygame.transform.flip(self.animation.get_frame(), self.flip, False),
            (self.position[0] - offset[0], self.position[1] - offset[1]),
        )
        # Draw the entity rectangle for debugging
        pygame.draw.rect(surface, (255, 0, 0), self.rectangle(offset), 1)


class Player(Entity):
    def __init__(self, game, entity_type, position, size):
        super().__init__(game, entity_type, position, size)
        self.idle_up = False
        self.idle_down = False
        self.idle = True
        self.running = False
        self.stamina = utils.Stamina_Bar(
            game, (10, 10), (100, 10)
        )  # create a stamina bar for the player
        self.counter = 0

    def update_idle_up(self):
        self.idle_up = True
        self.idle_down = False
        self.idle = False

    def update_idle_down(self):
        self.idle_down = True
        self.idle_up = False
        self.idle = False

    def update_idle(self):
        self.idle = True
        self.idle_up = False
        self.idle_down = False

    def not_moving(self, movement=(0, 0, 0, 0)):
        if not movement[0] and not movement[1] and not movement[2] and not movement[3]:
            if self.idle_up:
                self.set_action("idle/idle_up")
            elif self.idle_down:
                self.set_action("idle/idle_down")
            else:
                self.set_action("idle/idle")

    def update(self, movement=(0, 0, 0, 0)):
        super().update(movement)
        # Add any player-specific update logic here
        # For example, you can handle player-specific actions or states
        if self.running and self.stamina.current_stamina > 0:

            self.stamina.stamina_deplete()
            self.stamina.render()

            self.speed = 75  # increase the speed of the player
            if movement[0]:
                self.set_action("run/run_up")
                self.update_idle_up()
            elif movement[1]:
                self.set_action("run/run_down")
                self.update_idle_down()
            elif movement[3]:
                self.set_action("run/run")
                self.update_idle()
            elif movement[2]:
                self.set_action("run/run")
                self.update_idle()
            self.not_moving(movement)

        else:

            self.stamina.stamina_regen()
            self.stamina.render()

            self.speed = 50
            if movement[0]:  # Up
                self.set_action("walk/walk_up")
                self.update_idle_up()
            elif movement[1]:  # Down
                self.set_action("walk/walk_down")
                self.update_idle_down()
            elif movement[3]:  # Rights
                self.set_action("walk/walk")
                self.update_idle()
            elif movement[2]:
                self.set_action("walk/walk")
                self.update_idle()
            self.not_moving(movement)

        self.animation.animate()  # animate the player
