#Initialise pygame
import pygame, math, sys, random, copy
from pygame.locals import *

#Importing classes needed
from Classes.Button import Button
from Classes.CheckBox import CheckBox
from Classes.RandomButton import RandomButton
from Classes.InputBox import InputBox

pygame.init()

#Global parameters
BALL = pygame.image.load("ball.jpg")
Font = pygame.font.Font(None, 64) #Initialises Pygame's default font
SCREENWIDTH, SCREENHEIGHT = 900, 600 #Sets the screen's height & width
WHITE = (255, 255, 255)
GREEN = (124, 255,   0)
RED   = (255,   0,   0)
BLACK = (  0,   0,   0)
FPS = 30 #Frames per second
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Main screen that I will add stuff on
pygame.display.set_caption("Projectile Motion & Particle Rolling Down A Ramp In A 2D Plane") #Caption of the simulation

def MainMenu(): #Makes the main menu
    ProjMotion = False
    Running = True
    Title = Font.render("Main Menu", 1, RED) #'Main menu' title #Change to title later on
    ProjectileMotionButton = Button("Projectile Motion", 100, 450, 60, 200, DISPLAYSURF) #Instanciating proj_motion button
    RampButton = Button("Ramp Mode", 600, 450, 60, 200, DISPLAYSURF) #Instanciating ramp mode button
    while Running: #Main game loop that runs the animation
        DISPLAYSURF.fill(WHITE) #Initialises the screen by making it white
        DISPLAYSURF.blit(Title, (330,200)) #Displays title on screen
        ProjectileMotionButton.DisplayButton()
        RampButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT: #Allows user to exit program
                pygame.quit() #Stops pygame
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse click
                if ProjectileMotionButton.ClickInRange((PosX,PosY)) == True: #Checks if the click is in range of the button
                    ProjMotion = True
                    Running = False #Stops the animation loop
                elif RampButton.ClickInRange((PosX, PosY)) == True: #Checks if the click is in the range of the button
                    Running = False #Stops the animation loop
        pygame.display.update() #Updates display every frame
        fpsClock.tick(FPS)
    if ProjMotion == True:
        InputScreen_ProjMotion()
    else:
        InputScreen_Ramp() #So that you can access the input screen for a particle rolling down a ramp

def InputScreen_ProjMotion(): #Makes the input screen for projectile motion #Make sure you pass parameters
    Title = Font.render("Projectile Motion Input Screen", 1, RED) #Title
    DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass = MakeWidgets()
    Running = True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title,(120,60)) #Adds title to the top of the screen
        #Display All buttons, input boxes & checkbox
        DisplayWidgets(DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass)
        #If the above doesn't work, just copy & paste back here and it 100%. Done for sole purpose of making my code neater.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Can check multiple things at once as they'll never overlap
                (PosX,PosY)  = pygame.mouse.get_pos()
                #Checks if the box has been clicked on or not- Will cancel out the click if it's not the case
                InitialVBox.ClickInRange((PosX,PosY))
                DisplacementBox.ClickInRange((PosX,PosY))
                AngleBox.ClickInRange((PosX,PosY))
                MassBox.ClickInRange((PosX,PosY))
                #Allows you to check\uncheck the hide checkbox
                HideCheck.ClickInRange((PosX,PosY))
                if SubmitButton.ClickInRange((PosX,PosY)) == True: #Checks if submit button has been clicked
                    Running = False #Stops the animation loop
                elif RandomDisplacement.ClickInRange((PosX,PosY)):
                    DisplacementBox.Variable = RandomDisplacement.GetNumInRange()
                elif RandomInitialV.ClickInRange((PosX,PosY)):
                    InitialVBox.Variable = RandomInitialV.GetNumInRange()
                elif RandomAngle.ClickInRange((PosX,PosY)):
                    AngleBox.Variable = RandomAngle.GetNumInRange()
                elif RandomMass.ClickInRange((PosX,PosY)):
                    MassBox.Variable = RandomMass.GetNumInRange()
            elif (event.type == KEYDOWN) and (DisplacementBox.Clicked == True):
                DisplacementBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (InitialVBox.Clicked == True): #Adds values to the initial velocity
                InitialVBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (AngleBox.Clicked == True): #Adds values to the angle
                AngleBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (MassBox.Clicked == True): #Adds characters to the mass
                MassBox.AddCharacter(event.key)
        #Updates event every 1/30th of a second
        pygame.display.update()
        fpsClock.tick(FPS)

    s, u, Angle = Convert(DisplacementBox.Variable,InitialVBox.Variable,AngleBox.Variable) #Tries to convert the inputs to real numbers
    if (u!="") and ((Angle!="") or (s!="")):
        s, u, v, t, Angle,Mode = Solve_ProjMotion(s,u,Angle) #Solves remaining parameters using SUVAT equations
        ProjMotionSimulation(s,u,v,t,Angle,HideCheck.Clicked,Mode)#Simulation for Proj_Motion
    else:
        ErrorMsg_NotEnough_Proj() #Function which shows the user that not enough inputs were entered

def ProjMotionSimulation(s,u,v,t,Angle,Hide,Mode):
    #Making Widgets
    InputButton = Button("Inputs", 600, 400, 35,200,DISPLAYSURF)
    RampButton = Button("Ramp Mode", 600, 470, 35, 200,DISPLAYSURF)
    ExplainButton = Button("Explain", 600, 540, 35, 200, DISPLAYSURF)
    HIDE = CheckBox(500,400,30,DISPLAYSURF,"Hide Parameters:",160)
    HIDE.Clicked = Hide
    Input = False
    Ramp = False
    Explain = False
    GROUNDLEVEL = 350
    s = s
    PosX = 50
    PosY = GROUNDLEVEL #As the particle will start at the ground
    g = -9.8
    ANGLEDEGREES = round(Angle,1)
    ANGLERADIANS = math.radians(ANGLEDEGREES)
    u = u
    i = u * round(math.cos(ANGLERADIANS), 1) #Gives horizontal velocity#round(degrees, 1) rounds to 1dp
    j = u * round(math.sin(ANGLERADIANS), 1) #Gives vertical velocity
    SCALEFACTOR = 1.3 #Has to be >=1 #Makes the animation fit to screen more appropriately
    CoordinatesList = GetLists(i,j,PosX,PosY)
    TrailList = copy.deepcopy(CoordinatesList)
    TrailList = AdjustTrail(TrailList)
    Motion = True #So the ball moves whilst the ball is on the list #Used to stop the pointer from going out of the range of the list
    Pointer = 0
    DISPLAYSURF.fill(WHITE)
    Running = True
    while Running:
        DISPLAYSURF.fill(WHITE)
        InputButton.DisplayButton()
        RampButton.DisplayButton()
        ExplainButton.DisplayButton()
        HIDE.MakeBox()
        if HIDE.Clicked == False:
            PrintParameters(s,u,v,t,ANGLEDEGREES)
        if Motion == True:
            PosX, PosY = CoordinatesList[Pointer][0], CoordinatesList[Pointer][1]
            DISPLAYSURF.blit(BALL, (PosX, PosY))
            if Pointer == (len(CoordinatesList)-1):
                Motion = False
            else:
                Pointer +=1

        if Motion == False:
            PosY = GROUNDLEVEL
            PosX = CoordinatesList[Pointer][0]
            DISPLAYSURF.blit(BALL, (PosX, PosY))
        #Makes trail
        if Pointer>1:
            pygame.draw.aalines(DISPLAYSURF, RED,False, TrailList[:Pointer],5)#MakeTrail(Pointer)
        #Makes ground by drawing a thick, green line
        pygame.draw.line(DISPLAYSURF, GREEN, (0,GROUNDLEVEL+25), (SCREENWIDTH,GROUNDLEVEL+25),8) #+25 makes simulation look better

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse click
                    HIDE.ClickInRange((PosX,PosY))
                    if InputButton.ClickInRange((PosX,PosY)) == True:
                        Input = True #It will be true which implies that that user must enter inputs again
                        Running = False
                    elif RampButton.ClickInRange((PosX,PosY)) == True:
                        Ramp = True
                        Running = False
                    elif ExplainButton.ClickInRange((PosX,PosY)) == True:
                        Explain = True
                        Running = False

        pygame.display.update()
        fpsClock.tick(FPS)
    if Input == True:
        InputScreen_ProjMotion()
    elif Ramp == True:
        InputScreen_Ramp()
    elif Explain == True:
        if Mode == 1:
            Explain_ProjMotion1(s,u,v,t,ANGLEDEGREES,HIDE.Clicked,Mode)
        elif Mode == 2:
            Explain_ProjMotion2(s,u,v,t,ANGLEDEGREES,HIDE.Clicked,Mode)

def InputScreen_Ramp(): #Makes the input screen for projectile motion #Make sure you pass parameters
    Title = Font.render("Ramp Mode Input Screen", 1, RED) #Title
    DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement,RandomInitialV, RandomAngle, RandomMass = MakeWidgets_Ramp()
    Running = True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title,(120,60)) #Adds title to the top of the screen
        #Display All buttons, input boxes & checkbox
        DisplayWidgets(DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Can check multiple things at once as they'll never overlap
                (PosX,PosY)  = pygame.mouse.get_pos()
                #Checks if the box has been clicked on or not- Will cancel out the click if it's not the case
                InitialVBox.ClickInRange((PosX,PosY))
                DisplacementBox.ClickInRange((PosX,PosY))
                AngleBox.ClickInRange((PosX,PosY))
                MassBox.ClickInRange((PosX,PosY))
                #Allows you to check\uncheck the hide checkbox
                HideCheck.ClickInRange((PosX,PosY))
                if SubmitButton.ClickInRange((PosX,PosY)) == True: #Checks if submit button has been clicked
                    Running = False #Stops the animation loop
                elif RandomDisplacement.ClickInRange((PosX,PosY)):
                    DisplacementBox.Variable = RandomDisplacement.GetNumInRange()
                elif RandomInitialV.ClickInRange((PosX,PosY)):
                    InitialVBox.Variable = RandomInitialV.GetNumInRange()
                elif RandomAngle.ClickInRange((PosX,PosY)):
                    AngleBox.Variable = RandomAngle.GetNumInRange()
                elif RandomMass.ClickInRange((PosX,PosY)):
                    MassBox.Variable = RandomMass.GetNumInRange()
            elif (event.type == KEYDOWN) and (DisplacementBox.Clicked == True):
                DisplacementBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (InitialVBox.Clicked == True): #Adds values to the initial velocity
                InitialVBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (AngleBox.Clicked == True): #Adds values to the angle
                AngleBox.AddCharacter(event.key)
            elif (event.type == KEYDOWN) and (MassBox.Clicked == True): #Adds characters to the mass
                MassBox.AddCharacter(event.key)
        #Updates event every 1/30th of a second
        pygame.display.update()
        fpsClock.tick(FPS)

    s, u, Angle = Convert(DisplacementBox.Variable,InitialVBox.Variable,AngleBox.Variable) #Tries to convert the inputs to real numbers
    if (u!="") and (Angle!="") and (s!=""):
        s, u, v, t, Angle = Solve_Ramp(s,u,9.8,Angle) #Solves remaining parameters using SUVAT equations
        RampSimulation(s,u,v,t,Angle,HideCheck.Clicked)#Simulation for Proj_Motion
    else:
        ErrorMsg_Ramp() #Function which shows the user that not enough inputs were entered

def RampSimulation(s,u,v,t,Angle,Hide):
    #HIDE = Hide
    g = 9.8
    s, u, v,TotalTime,ANGLEDEGREES = s,u,v,t,math.degrees(Angle)
    InputButton = Button("Inputs", 600, 380, 40,200,DISPLAYSURF) #Button which allows the user to re-enter inputs
    ProjMotionButton = Button("Projectile Motion", 600, 450, 40, 200,DISPLAYSURF) #Button which allows the user to simulate projectile motion
    ExplainButton = Button("Explain", 600, 520, 40, 200,DISPLAYSURF) #Button which leads the user to a screen which explains how parameters are worked out
    HIDE = CheckBox(500,380,30,DISPLAYSURF,"Hide Parameters:",150)
    HIDE.Clicked = Hide
    SCALEFACTOR = 4.3 #Adjusts visuals => makes the program prettier #Must be >0
    RAMPSTART = 500
    GROUNDLEVEL = 350
    ANGLERADIANS = math.radians(ANGLEDEGREES) #Have to use this: PyGame works in radians not degrees
    SimulationTime = 1/FPS #Initialises time
    y = GROUNDLEVEL - SCALEFACTOR * round(s * math.sin(ANGLERADIANS),1) - 25 #Initialise the the y coordinate
    #Decides which page to navigate to next
    Input = False
    ProjectileMotion = False
    Explain = False
    Running = True #Allows the program to run

    while Running:
        #Display the widgets
        DISPLAYSURF.fill(WHITE)
        InputButton.DisplayButton()
        ProjMotionButton.DisplayButton()
        ExplainButton.DisplayButton()
        HIDE.MakeBox()
        if HIDE.Clicked == False: #Will only show it if the user has chosen not to hide the details
            PrintParameters_Ramp(s,u,v,t,ANGLEDEGREES)

        #Gets the current x,y  position of the ball on the ramp
        x, y = GetPos(s,u,g,SimulationTime, ANGLERADIANS,SCALEFACTOR,GROUNDLEVEL,RAMPSTART)

        if (y < GROUNDLEVEL) and (SimulationTime<=TotalTime): #Just in case...
            DISPLAYSURF.blit(BALL, (x,y))
            SimulationTime += 1/FPS #So that the time is updated
        else:
            DISPLAYSURF.blit(BALL, (RAMPSTART,GROUNDLEVEL-30)) #Just so that it doesn't disappear after being changing
        #Add these at end so that the ball is underneath the ramp & ground
        MakeRamp(GROUNDLEVEL,RAMPSTART,ANGLERADIANS,SCALEFACTOR)
        MakeGround(GROUNDLEVEL)

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse click
                    HIDE.ClickInRange((PosX,PosY))
                    if InputButton.ClickInRange((PosX,PosY)) == True:
                        Input = True #It will be true which implies that that user must enter inputs again
                        Running = False
                    elif ProjMotionButton.ClickInRange((PosX,PosY)) == True:
                        ProjectileMotion = True
                        Running = False
                    elif ExplainButton.ClickInRange((PosX,PosY)) == True:
                        Explain = True
                        Running = False
        pygame.display.update()
        fpsClock.tick(FPS)
    #Where the next page will be
    if Input == True:
        InputScreen_Ramp()
    elif ProjectileMotion == True:
        InputScreen_ProjMotion()
    elif Explain == True:
        Explain_Ramp(s,u,v,t,ANGLERADIANS,HIDE.Clicked)


#Functions Needed
def Explain_ProjMotion1(s,u,v,t,Angle,Hide,Method):
    ExplainFont = pygame.font.Font(None,32) #Initialises PyGame's initial font of size 32
    Running = True
    VExplain1 = ExplainFont.render("v = -u",1,BLACK)
    VExplain2 = ExplainFont.render("v = -{0}".format(str(u)),1,BLACK)
    AngleExplain1 = ExplainFont.render("Rearrange v^2 =u^2 + 2as where v = 0",1,BLACK)
    AngleExplain2 = ExplainFont.render("=> usinθ = √(2gs) => θ = arcsin((√2gs))/u",1,BLACK)
    AngleExplain3 = ExplainFont.render("=> θ = arcsin(√(2*g*{0}))/{1}".format(str(s),str(u)),1,BLACK)
    TimeExplain1 = ExplainFont.render("Rearrange s = ut + 0.5at^2 where s = 0",1,BLACK)
    TimeExplain2 = ExplainFont.render("=> t = usinθ/4.9",1,BLACK)
    TimeExplain3 = ExplainFont.render("=> t = {0}sin({1})/4.9".format("%.1f"%u,"%.1f"%Angle),1,BLACK)
    OKButton = Button("OK",400,500,35,100,DISPLAYSURF) #(Label, PosXStart, PosYStart, Width, Length, Surface)
    while Running:
            DisplayExplainProjMotion(VExplain1, VExplain2,AngleExplain1, AngleExplain2, AngleExplain3, TimeExplain1, TimeExplain2, TimeExplain3, OKButton)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse
                    if OKButton.ClickInRange((PosX,PosY)) == True:
                        Running = False
            pygame.display.update()
            fpsClock.tick(FPS)
    ProjMotionSimulation(s,u,v,t,Angle,Hide,Method)

def Explain_ProjMotion2(s,u,v,t,Angle,Hide,Method):
    ExplainFont = pygame.font.Font(None,32) #Initialises PyGame's initial font of size 32
    Running = True
    VExplain1 = ExplainFont.render("v = -u",1,BLACK)
    VExplain2 = ExplainFont.render("v = -{0}".format("%.1f"%u),1,BLACK)
    TimeExplain1 = ExplainFont.render("Rearrange s = ut + 0.5at^2 where s = 0",1,BLACK)
    TimeExplain2 = ExplainFont.render("=> t = usinθ/4.9",1,BLACK)
    TimeExplain3 = ExplainFont.render("=> t = {0}sin({1})/4.9".format("%.1f"%u,"%.1f"%Angle),1,BLACK)
    DisplacementExplain1 = ExplainFont.render("At time, t/2, height is at a max => using s = ut + 0.5at^2",1,BLACK)
    DisplacementExplain2 = ExplainFont.render("=> s = usinθ(t/2) - 4.9(t/2)^2",1,BLACK)
    DisplacementExplain3 = ExplainFont.render("=> s = {0}sin({1})({2}/2) - 4.9({2}/2)^2".format("%.1f"%u,"%.1f"%Angle,"%.1f"%t),1,BLACK)
    OKButton = Button("OK",400,500,35,100,DISPLAYSURF) #(Label, PosXStart, PosYStart, Width, Length, Surface)
    while Running:
            DisplayExplainProjMotion(VExplain1,VExplain2, TimeExplain1,TimeExplain2,TimeExplain3,DisplacementExplain1,DisplacementExplain2,DisplacementExplain3,OKButton)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse
                    if OKButton.ClickInRange((PosX,PosY)) == True:
                        Running = False
            pygame.display.update()
            fpsClock.tick(FPS)
    ProjMotionSimulation(s,u,v,t,Angle,Hide,Method)

def DisplayExplainProjMotion(a,b,c,d,e,f,g,h,Button): #Made to display the process of finding the answer. #Used as there was repeating code
     DISPLAYSURF.fill(WHITE)
     DISPLAYSURF.blit(a,(40,30))
     DISPLAYSURF.blit(b,(40,70))
     DISPLAYSURF.blit(c,(40,120))
     DISPLAYSURF.blit(d,(40,170))
     DISPLAYSURF.blit(e,(40,220))
     DISPLAYSURF.blit(f,(40,270))
     DISPLAYSURF.blit(g,(40,320))
     DISPLAYSURF.blit(h,(40,370))
     Button.DisplayButton()

def Explain_Ramp(s,u,v,t,Angle,Hide): #Function which takes user to new page which shows how the variables were solved for the ramp
    ExplainFont = pygame.font.Font(None, 32) #Initialises Pygame's default font this time a size smaller to fit onto screen
    Running = True
    VExplain1 = ExplainFont.render("Re-arrange the SUVAT formula (v^2 = u^2 + 2as) into the form:", 1, BLACK)
    VExplain2 = ExplainFont.render("=> v = √u^2 + 2sgsinθ",1,BLACK)
    VExplain3 = ExplainFont.render("=> v = √{0}^2 + 2*{1}*g*sin({2})".format("%.1f"%u,"%.1f"%s,"%.1f"%(math.degrees(Angle))),1,BLACK)
    TExplain1 = ExplainFont.render("Re-arrange (s = ut + 0.5at^2) into quadratic form:",1,BLACK)
    TExplain2 = ExplainFont.render("=> t = (-u + √u^2 + 19.6s*sinθ) /gsin(θ)",1,BLACK)
    TExplain3 = ExplainFont.render("=> t = (-{0} + √{0}^2 + 19.6*{1}*sin({2}))/gsin({2})".format(("%.1f"%u),("%.1f"%s),("%.1f"%(math.degrees(Angle)))),1,BLACK)
    OKButton = Button("OK",400,500,35,100,DISPLAYSURF)
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(VExplain1,(40,70))
        DISPLAYSURF.blit(VExplain2,(40,120))
        DISPLAYSURF.blit(VExplain3,(40,170))
        DISPLAYSURF.blit(TExplain1,(40,270))
        DISPLAYSURF.blit(TExplain2,(40,320))
        DISPLAYSURF.blit(TExplain3,(40,370))
        OKButton.DisplayButton()
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (PosX, PosY) = pygame.mouse.get_pos() #Get position of mouse
                    if OKButton.ClickInRange((PosX,PosY)) == True:
                        Running = False
        pygame.display.update()
        fpsClock.tick(FPS)
    RampSimulation(s,u,v,t,Angle,Hide)


def MakeRamp(GROUNDLEVEL, RAMPSTART, Angle,SCALEFACTOR):
    EndRampX = RAMPSTART - (SCALEFACTOR * 100 * math.cos(Angle))
    EndRampY = GROUNDLEVEL - (SCALEFACTOR * 100 * math.sin(Angle))
    return pygame.draw.line(DISPLAYSURF, GREEN, (RAMPSTART,GROUNDLEVEL),(EndRampX,EndRampY), 10)

def MakeGround(GROUNDLEVEL):
    return pygame.draw.line(DISPLAYSURF, GREEN, (0,GROUNDLEVEL), (SCREENWIDTH,GROUNDLEVEL),8)

def GetPos(s,u,g,Time,Angle,SCALEFACTOR,GROUNDLEVEL,RAMPSTART):
    s_difference = (u * Time) + (0.5 * abs(g) * math.sin(Angle) * (Time**2)) #Using formula s=ut+0.5at**2 to get displacement at time t
    s_new  = s - s_difference
    x_new = SCALEFACTOR * s_new * math.cos(Angle) #New x coordinate
    y_new = SCALEFACTOR * s_new * math.sin(Angle) #New y coordinate
    if (GROUNDLEVEL - y_new) - 25 <= GROUNDLEVEL:
        x = (RAMPSTART - x_new) - 5#Adjusted or Pygame #The '-5' makes it prettier
        y = (GROUNDLEVEL - y_new) - 25#Adjusted for Pygame #The '-25' is to make the system look better
        return x,y
    else:
        return RAMPSTART, GROUNDLEVEL- y_new-40

def Solve_Ramp(s,u, g, Angle): #Returns the final velocity and total time of the simulation
    v = math.sqrt(u**2 + (2*g*math.sin(Angle)*s)) #Rearranging the formula v**2 = u**2 + 2as
    t = round((-u + math.sqrt(u**2 + (19.6*math.sin(Angle)*s)))/(g * math.sin(Angle)),1) #Rearranging s=ut+0.5at^2
    return s,u,v, t,Angle

def MakeWidgets_Ramp(): #Makes all neccassary input widgets needed for Ramp input
    DisplacementBox = InputBox(310, 150, "Displacement (m):", 160, 6, (0.1,100))
    InitialVBox = InputBox(310, 210, "Initial Velocity (ms^-1):", 205, 5, (0,20))
    AngleBox = InputBox(310, 270, "Angle Of Inclination (°):", 210, 4,(0.1,89.9))
    MassBox = InputBox(310,330, "Mass (kg):", 90, 4, (0.1,10))
    HideCheck = CheckBox(430, 400, 30, DISPLAYSURF, "Hide Variables:",140)#Checkbox which hides variables #(PosX, PosY, Width,Surface,Label):
    SubmitButton = Button("Submit", 380, 470, 40, 100,DISPLAYSURF)
    RandomDisplacement = RandomButton("Random", 640, 150, 30, 115, DISPLAYSURF, (0.1,100))
    RandomInitialV = RandomButton("Random", 640, 210, 30, 115, DISPLAYSURF, (0,20))
    RandomAngle = RandomButton("Random", 640, 270, 30, 115, DISPLAYSURF, (0.1,89.9))
    RandomMass = RandomButton("Random", 640, 330, 30, 115, DISPLAYSURF, (0.1,10))
    return DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass

def MakeWidgets(): #Makes all neccassary input widgets needed for the Projectile Motion input screen
    DisplacementBox = InputBox(310, 150, "Displacement (m):", 163, 6, (0.1,100))
    InitialVBox = InputBox(310, 210, "Initial Velocity (ms^-1):", 213, 6, (0.1,100))
    AngleBox = InputBox(310, 270, "Angle Of Projection (°):", 213, 4,(0.1,90))
    MassBox = InputBox(310,330, "Mass (kg):", 90, 4, (0.1,10))
    HideCheck = CheckBox(430, 400, 30, DISPLAYSURF, "Hide Variables:",140)
    SubmitButton = Button("Submit", 380, 470, 40, 100,DISPLAYSURF)
    RandomDisplacement = RandomButton("Random", 640, 150, 30, 115, DISPLAYSURF, (0.1,100))
    RandomInitialV = RandomButton("Random", 640, 210, 30, 115, DISPLAYSURF, (0.1,100))
    RandomAngle = RandomButton("Random", 640, 270, 30, 115, DISPLAYSURF, (0.1,90))
    RandomMass = RandomButton("Random", 640, 330, 30, 115, DISPLAYSURF, (0.1,10))
    return DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass

def DisplayWidgets(DisplacementBox, InitialVBox, AngleBox, MassBox, HideCheck, SubmitButton, RandomDisplacement, RandomInitialV, RandomAngle, RandomMass):
        return DisplacementBox.MakeBox() , InitialVBox.MakeBox(), AngleBox.MakeBox(),MassBox.MakeBox(), HideCheck.MakeBox(), SubmitButton.DisplayButton() ,RandomDisplacement.DisplayButton(), RandomInitialV.DisplayButton(),RandomAngle.DisplayButton(),RandomMass.DisplayButton()

def VerticalCoordinates(j, g, PosY, UP, DOWN): #Generates vertical coordinates for projectile motion using recursion
    SCALEFACTOR = 2 #Makes simulation prettier
    GROUNDLEVEL = 350
    if UP == True:
        PosY = PosY - (SCALEFACTOR*(j/FPS))
        j = j + (g/FPS)
        if j<=0:
            UP = False
            DOWN = True
            return [PosY] + VerticalCoordinates(j, g, PosY, False, True)
        return [PosY] + VerticalCoordinates(j, g, PosY, True, False)

    elif DOWN == True:
        PosY = PosY - (SCALEFACTOR*(j/FPS))
        j = j + (g/FPS) #Have to add 'g' as it's negative
        if PosY >= GROUNDLEVEL:
            PosY = GROUNDLEVEL
            return [PosY]
        return [PosY] + VerticalCoordinates(j, g, PosY,False, True)

def RoundAllValues(List):
    for count in range(len(List)):
        List[count][0] = round(List[count][0],1)
        List[count][1] = round(List[count][1],1)
    return List

def HorizontalCoordinates(i,PosX, LengthOfVertList):
    SCALEFACTOR = 2
    List = []
    for count in range(LengthOfVertList):
        PosX += (SCALEFACTOR*(i/FPS))
        List.append(PosX)
    return List

def Convert(List):
    if List[-1]<0:
        List[-1] = 0
    return List[-1]

def JoinLists(ListX, ListY):
    ListXY = [] #Returns coordinates of projectile
    for count in range(len(ListX)):
        ListXY.append([ListX[count], ListY[count]])
    ListXY = RoundAllValues(ListXY)
    return ListXY

def GetLists(i,j,PosX,PosY):
    g = -9.8 #Defining as negative- the acceleration is downwards
    VerticalList= VerticalCoordinates(j,g,PosY, True, False)
    HorizontalList = HorizontalCoordinates(i,PosX, len(VerticalList))
    MainList = JoinLists(HorizontalList, VerticalList)
    return MainList

def AdjustTrail(Trail): #Function used to adjust trail to make it more aesthetically pleasing
    for index in range(len(Trail)):
        Trail[index][0],Trail[index][1] = Trail[index][0]+2, Trail[index][1]+13 #Arbitary values are there to adjust trail position
    return Trail

def PrintParameters(s,u,v,t,Angle):
    ParameterFont = pygame.font.Font(None, 30) #Initialises Pygame's default font this time a size smaller to fit onto screen
    S = ParameterFont.render("S = {0} m".format("%.1f"%s),1,BLACK)
    U = ParameterFont.render("U = {0} ms^-1".format("%.1f"%u),1,BLACK)
    V = ParameterFont.render("V = {0} ms^-1".format("%.1f"%v),1,BLACK)
    A = ParameterFont.render("A = -g = -9.8 ms^-2",1,BLACK) #Ask if client wants '-g' as well
    T = ParameterFont.render("T = {0} s".format("%.1f"%t),1,BLACK)
    ANGLE = ParameterFont.render("θ = {0}°".format("%.1f"%Angle),1,BLACK)
    DISPLAYSURF.blit(S,(40, 400))
    DISPLAYSURF.blit(U,(40, 430))
    DISPLAYSURF.blit(V,(40, 460))
    DISPLAYSURF.blit(A,(40, 490))
    DISPLAYSURF.blit(T,(40, 520))
    DISPLAYSURF.blit(ANGLE,(40, 550))

def PrintParameters_Ramp(s,u,v,t,Angle):
    ParameterFont = pygame.font.Font(None, 30) #Initialises Pygame's default font this time a size smaller to fit onto screen
    S = ParameterFont.render("S = {0} m".format("%.1f"%s),1,BLACK)
    U = ParameterFont.render("U = {0} ms^-1".format("%.1f"%u),1,BLACK)
    V = ParameterFont.render("V = {0} ms^-1".format("%.1f"%v),1,BLACK)
    A = ParameterFont.render("A = gsin({0}) = {1} ms^-2".format("%.1f"%Angle,"%.1f"%(9.8*math.sin(math.radians(Angle)))),1,BLACK) #Ask if client wants '-gsinθ'
    T = ParameterFont.render("T = {0} s".format("%.1f"%t),1,BLACK)
    ANGLE = ParameterFont.render("θ = {0}°".format("%.1f"%Angle),1,BLACK)
    DISPLAYSURF.blit(S,(40, 380))
    DISPLAYSURF.blit(U,(40, 410))
    DISPLAYSURF.blit(V,(40, 440))
    DISPLAYSURF.blit(A,(40, 470))
    DISPLAYSURF.blit(T,(40, 500))
    DISPLAYSURF.blit(ANGLE,(40, 530))

def ErrorMsg_NotEnough_Proj():
    Title1 = Font.render("Please Enter The Initial Velocity &", 1, RED)
    Title2 = Font.render("EITHER The Angle Of Projection",1,RED)
    Title3 = Font.render("OR The Displacement",1,RED)
    OKButton =  Button("OK", 380, 450, 40, 100,DISPLAYSURF)
    Running =True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(85,100))
        DISPLAYSURF.blit(Title2,(100,200))
        DISPLAYSURF.blit(Title3,(170,300))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True: #Know you get to go to the input screen
                    Running = False
        pygame.display.update()
        fpsClock.tick(FPS)
    InputScreen_ProjMotion() #Goes back to the input screen

def ErrorMsg_Ramp(): #Makes error message for Ramp Mode which tells the user to enter Dispacement & Initial Velocity & Angle
    Line1 = Font.render("ERROR!", 1, RED)
    Line2 = Font.render("Please Enter ALL Of The Following:",1,RED)
    Line3 = Font.render("- Displacement",1,RED)
    Line4 = Font.render("- Initial Velocity", 1, RED)
    Line5 = Font.render("- Angle Of Inclination",1,RED)
    OKButton =  Button("OK", 320, 470, 40, 100,DISPLAYSURF)
    Running = True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Line1, (270,50))
        DISPLAYSURF.blit(Line2,(60,120))
        DISPLAYSURF.blit(Line3,(190,220))
        DISPLAYSURF.blit(Line4,(190,290))
        DISPLAYSURF.blit(Line5, (190,360))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Can check multiple things at once as they'll never overlap
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True:
                    Running = False #So once the 'OK' button has been clicked, the user is sent back to the input screen
        pygame.display.update()
        fpsClock.tick(FPS)
    InputScreen_Ramp()

def Solve_ProjMotion(s,u,Angle): #Solves remaining parameters using SUVAT equations
    #Actually solve other parameters
    g = 9.8 #Numerical value of acceleration due to gravity
    if (s!="") and (Angle==""): #i.e. when the angle is unknown
        if math.sqrt(2*g*s)/u>1: #To prevent otherwise impossible situations #-1<=Sin(x)<=1
            NotPossible()
        else:
            Mode = 1
            v = -u
            Angle = math.asin(math.sqrt(2*g*s)/u) #Rearranging v**2 = u**2 + 2as where v = 0
            t = (u*math.sin(Angle))/4.9 #Using s=ut+0.5at**2 where s=0
            return s, u, v, t, math.degrees(Angle), Mode
    elif (s=="") and (Angle!=""): #i.e. when the vertical maximum displacement is unknown
        Mode = 2
        v = -u
        t = (u*math.sin(Angle))/4.9 #Gives total time for the projectile
        s = (u*math.sin(Angle)*(t/2)) - (4.9 * (t/2)**2) #Gives maximum vertical height of projectile
        return s, u, v, t, math.degrees(Angle), Mode
    elif (s!="") and (Angle!="") and (u!=""): #i.e. When all parameters are given
        ErrorMsg_NotEnough_Proj() #Entering all 3 can lead to impossible situations

def NotPossible(): #Displays an error message which tells the user that the inputs entered are not feasible
    Title1 = Font.render("The inputs are not valid.", 1, RED) #Error message
    Title2 = Font.render("The value for Displacement is too high", 1, RED) #Error message
    Title3 = Font.render("for the given velocity.", 1, RED)
    Title4 = Font.render("Such a situation shouldn't occur.", 1, RED) #Error message
    Title5 = Font.render("Please Try Again.", 1, RED)
    OKButton =  Button("OK", 350, 500, 40, 100,DISPLAYSURF)
    Running =True
    while Running:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(Title1,(150,50))
        DISPLAYSURF.blit(Title2,(40,130))
        DISPLAYSURF.blit(Title3,(175,210))
        DISPLAYSURF.blit(Title4,(70,290))
        DISPLAYSURF.blit(Title5,(230,370))
        OKButton.DisplayButton()
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Can check multiple things at once as they'll never overlap
                (PosX,PosY)  = pygame.mouse.get_pos()
                if OKButton.ClickInRange((PosX,PosY)) == True:
                    Running = False
                    #InputScreen_ProjMotion()
        pygame.display.update()
        fpsClock.tick(FPS)
    InputScreen_ProjMotion()


def Convert(s,u,Angle): #Function that attempts to convert the varaibles-s,u,Angle to floats
                                     #If it's anything but a number, like '.' or ' ', it will treat the input as " "
    try:
        s = float(s)
    except:
        s = ""
    try:
        u = float(u)
    except:
        u = ""
    try:
        Angle = float(Angle)
        Angle = math.radians(Angle) #As pygame works in radians not degrees
    except:
        Angle = ""
    return s, u, Angle

if __name__ == "__main__": #The program starts from here
    MainMenu()
