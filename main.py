import pygame

from Planet import Planet

def main():
    run = True
    while run:
        clock.tick(60)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i, planet in enumerate(planets):
            if i > 0:
                # drawing orbit
                for i in range(len(planet.orbit) - 1):
                    e = planet.orbit[i]
                    e2 = planet.orbit[i + 1]
                    x1, y1= map(int, ((e[0] * Planet.SCALE) + WIDTH//2, (e[1] * Planet.SCALE) + HEIGHT//2))
                    x2, y2 = map(int, ((e2[0] * Planet.SCALE) + WIDTH // 2, (e2[1] * Planet.SCALE) + HEIGHT // 2))
                    pygame.gfxdraw.line(screen, x1, y1, x2, y2, (220, 220, 220))

                sun_distance_text = font.render(f"{planet.sun_distance}", True, (255, 255, 255))
                font_x, font_y = planet.converted_pos(screen)
                font_y += planet.radius + 1
                screen.blit(sun_distance_text, (font_x, font_y))
                update_pos(planet)

            planet.draw(screen)

        pygame.display.update()
    pygame.quit()

def update_pos(planet):
    total_x_force = total_y_force = 0
    for planet2 in planets:
        if planet is planet2:
            continue
        x_force, y_force = planet.gravitational_force(planet2)
        total_x_force += x_force
        total_y_force += y_force

    planet.x_vel += total_x_force / planet.mass * TIMESTEP
    planet.y_vel += total_y_force / planet.mass * TIMESTEP
    planet.x += planet.x_vel * TIMESTEP
    planet.y += planet.y_vel * TIMESTEP
    planet.add_orbit((planet.x, planet.y))

pygame.init()

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
TIMESTEP = 86400 # ONE DAY in seconds

# Colors
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (125, 125, 125)
VENUS_COLOR = (255, 181, 104)

# Planets and Sun
images = [f"images/{e}.png" for e in ["sun", "mercury", "venus", "earth", "mars"]]

sun = Planet(0, 0, 20, YELLOW, 1.989*10**30)
sun.is_sun = True

mercury = Planet(0, -0.387 * Planet.AU, 2.439, GREY, 3.285*10**23)
mercury.x_vel = 47.4 * 1000

venus = Planet(0, -0.723 * Planet.AU, 6.051, VENUS_COLOR, 4.867*10**24)
venus.x_vel = -35.02 * 1000

earth = Planet(0, -1 * Planet.AU, 6.371 , BLUE, 5.972*10**24)
earth.x_vel = 29.783 * 1000

mars = Planet(0, -1.524 * Planet.AU, 3.389, RED, 6.39*10**23)
mars.x_vel = 24.077 * 1000

planets = [sun, mercury, venus, earth, mars]
for i in range(len(planets)):
    p = planets[i]
    p.image = pygame.image.load(images[i])
    p.image = pygame.transform.scale(p.image, (p.radius*2, p.radius*2))

# Text
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

main()