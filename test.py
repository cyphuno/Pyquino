# pyODE example 2: Connecting bodies with joints

import os, sys
import pygame
from pygame.locals import *
import ode


if not pygame.font: print ('Warning, fonts disabled... this isnt going to be pretty')

def coord(x,y):
    "Convert world coordinates to pixel coordinates."
    return 320+170*x, 400-170*y


# Initialize pygame
pygame.init()

# Open a display
srf = pygame.display.set_mode((640,480))

# Create a world object
world = ode.World()
world.setGravity((0,-9.81,0))

# Create two bodies
body1 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body1.setMass(M)
body1.setPosition((1,1,0))

body2 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body2.setMass(M)
body2.setPosition((2,1,0))

# Connect body1 with the static environment
#j1 = ode.BallJoint(world)
#j1.attach(body1, ode.environment)
#j1.setAnchor( (0,2,0) )
j1 = ode.HingeJoint(world)
j1.attach(body1, ode.environment)
j1.setAnchor( (0,1,0) )
j1.setAxis( (0,0,1) )

j1.setParam(ode.ParamVel, 0)
j1.setParam(ode.ParamFMax, 20)

# Connect body2 with body1
j2 = ode.BallJoint(world)
j2.attach(body1, body2)
j2.setAnchor( (1,1,0) )


# Simulation loop...

fps = 50
dt = 1.0/fps
loopFlag = True
clk = pygame.time.Clock()

while loopFlag:
    events = pygame.event.get()
    for e in events:
        if e.type==QUIT:
            loopFlag=False
        if e.type==KEYDOWN:
            loopFlag=False

    # Clear the screen
    srf.fill((255,255,255))

    # Control system (bang-bang)
    a = j1.getAngle() * 180 / 3.145
    a_err = 90 - a
    P_const = 0.02
        
    command_vel = P_const * a_err


    # give some visual feedback
    if a > 90:
        joint_color = (255,0,0) # red
    else:
        joint_color = (0,255,0) # green

    # draw the current angle to the screen
    if pygame.font:
        font = pygame.font.Font(None,24)
        text_angle = font.render("angle: " + str(round(a,3)), 1, (0,0,0) )
        textpos_angle = text_angle.get_rect(topleft=(0,0))
        srf.blit(text_angle, textpos_angle)
        # also draw the error
        text_error = font.render("error: " + str(round(a_err,3)), 1, (0,0,0) )
        textpos_error = text_error.get_rect(topleft=textpos_angle.bottomleft)
        srf.blit(text_error, textpos_error)
        # also draw the command velocity
        text_cmdvel = font.render("cmd_vel: " + str(round(command_vel,3)), 1, (0,0,0))
        textpos_cmdvel = text_cmdvel.get_rect(topleft=textpos_error.bottomleft)
        srf.blit(text_cmdvel, textpos_cmdvel)
    
    # set the velocity
    j1.setParam(ode.ParamVel, command_vel)


    # Draw the two bodies
    x1,y1,z1 = body1.getPosition()
    x2,y2,z2 = body2.getPosition()
    #pygame.draw.circle(srf, (55,0,200), coord(x1,y1), 20, 0)
    pygame.draw.line(srf, joint_color, coord(0,1), coord(x1,y1), 2)
    #pygame.draw.circle(srf, (55,0,200), coord(x2,y2), 20, 0)
    pygame.draw.line(srf, (55,0,200), coord(x1,y1), coord(x2,y2), 2)

    pygame.display.flip()

    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate    
    clk.tick(fps)
